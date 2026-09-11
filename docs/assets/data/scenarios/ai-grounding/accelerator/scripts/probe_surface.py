#!/usr/bin/env python3
"""Verify anonymous, authorized, and restricted access through a deployed HTTP surface.

The endpoint is deliberately supplied at runtime. The plan supplies the request shape and
the status and payload expectations, so the script does not assume a route or response schema.

Keep caller tokens in environment variables. This script never prints token values, request
headers, request bodies, or response bodies.
"""
from __future__ import annotations

import argparse
import json
import os
import socket
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from _shared import ACCELERATOR, check

DEFAULT_PLAN = ACCELERATOR / "surface-probe.json"
CALLERS = ("anonymous", "authorized", "restricted")


def load_plan(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"No surface probe plan at {path}.")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"Surface probe plan is not valid JSON: {error.msg}.") from error
    if not isinstance(payload, dict):
        raise ValueError("Surface probe plan must contain a JSON object.")
    return payload


def validate_plan(plan: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    request = plan.get("request")
    if not isinstance(request, dict):
        return ["missing object 'request'"]

    method = request.get("method")
    if not isinstance(method, str) or not method.strip():
        problems.append("request: missing non-empty string 'method'")

    headers = request.get("headers", {})
    if not isinstance(headers, dict) or not all(
        isinstance(name, str) and isinstance(value, str) for name, value in headers.items()
    ):
        problems.append("request.headers must be an object with string names and values")

    if "body" in request:
        try:
            json.dumps(request["body"])
        except (TypeError, ValueError):
            problems.append("request.body must be JSON serializable")

    callers = plan.get("callers")
    if not isinstance(callers, dict):
        return problems + ["missing object 'callers'"]

    for caller in CALLERS:
        expectation = callers.get(caller)
        if not isinstance(expectation, dict):
            problems.append(f"callers.{caller}: missing object")
            continue
        statuses = expectation.get("expected_statuses")
        if not isinstance(statuses, list) or not statuses or any(
            not isinstance(status, int) or not 100 <= status <= 599 for status in statuses
        ):
            problems.append(
                f"callers.{caller}.expected_statuses must be a non-empty list of HTTP status codes"
            )
        for field in ("response_must_contain", "response_must_not_contain"):
            values = expectation.get(field, [])
            if not isinstance(values, list) or any(
                not isinstance(value, str) or not value for value in values
            ):
                problems.append(f"callers.{caller}.{field} must be a list of non-empty strings")

    authorized = callers.get("authorized", {})
    restricted = callers.get("restricted", {})
    if isinstance(authorized, dict) and not authorized.get("response_must_contain"):
        problems.append("callers.authorized must declare response_must_contain")
    if isinstance(restricted, dict) and not restricted.get("response_must_not_contain"):
        problems.append("callers.restricted must declare response_must_not_contain")
    return problems


def token_from_environment(variable_name: str, caller: str) -> str:
    token = os.environ.get(variable_name)
    if not token:
        raise ValueError(
            f"{caller} caller token is missing. Set the environment variable named "
            f"by --{caller}-token-env."
        )
    return token


def caller_headers(args: argparse.Namespace, caller: str) -> dict[str, str]:
    if caller == "anonymous":
        return {}
    variable_name = getattr(args, f"{caller}_token_env")
    token = token_from_environment(variable_name, caller)
    value = f"{args.auth_scheme} {token}".strip()
    return {args.auth_header: value}


def send_request(
    endpoint: str,
    request_spec: dict[str, Any],
    authentication_headers: dict[str, str],
    timeout_seconds: float,
) -> tuple[int, str]:
    headers = dict(request_spec.get("headers", {}))
    headers.update(authentication_headers)
    body = request_spec.get("body")
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = Request(
        endpoint,
        data=data,
        headers=headers,
        method=request_spec["method"].upper(),
    )
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            return response.status, response.read().decode("utf-8", errors="replace").lower()
    except HTTPError as error:
        return error.code, error.read().decode("utf-8", errors="replace").lower()


def verify_caller(
    caller: str,
    expectation: dict[str, Any],
    endpoint: str,
    request_spec: dict[str, Any],
    args: argparse.Namespace,
    failures: list[str],
) -> None:
    try:
        status, payload = send_request(
            endpoint,
            request_spec,
            caller_headers(args, caller),
            args.timeout_seconds,
        )
    except (TimeoutError, socket.timeout):
        check(False, f"{caller}: request timed out after {args.timeout_seconds:g} seconds", failures)
        return
    except URLError as error:
        reason = getattr(error, "reason", error)
        check(False, f"{caller}: request failed: {reason}", failures)
        return

    expected_statuses = expectation["expected_statuses"]
    check(
        status in expected_statuses,
        f"{caller}: received expected HTTP status {status}",
        failures,
    )
    for expected in expectation.get("response_must_contain", []):
        check(
            expected.lower() in payload,
            f"{caller}: response contains required marker '{expected}'",
            failures,
        )
    for forbidden in expectation.get("response_must_not_contain", []):
        check(
            forbidden.lower() not in payload,
            f"{caller}: response does not expose restricted marker '{forbidden}'",
            failures,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", required=True, help="Full deployed HTTP endpoint, including its route.")
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN, help=f"Request and expectation plan (default: {DEFAULT_PLAN}).")
    parser.add_argument(
        "--authorized-token-env",
        required=True,
        help="Name of the environment variable that contains the authorized caller token.",
    )
    parser.add_argument(
        "--restricted-token-env",
        required=True,
        help="Name of the environment variable that contains the restricted caller token.",
    )
    parser.add_argument(
        "--auth-header",
        default="Authorization",
        help="Header used for caller credentials (default: Authorization).",
    )
    parser.add_argument(
        "--auth-scheme",
        default="Bearer",
        help="Credential scheme placed before each token; pass an empty string for none (default: Bearer).",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=20,
        help="Per-call timeout in seconds (default: 20).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    parsed_endpoint = urlparse(args.endpoint)
    if parsed_endpoint.scheme not in {"http", "https"} or not parsed_endpoint.netloc:
        print("FAIL  endpoint must be a full HTTP or HTTPS URL, including the route.")
        return 1
    if not args.auth_header.strip():
        print("FAIL  --auth-header must be non-empty.")
        return 1
    if args.timeout_seconds <= 0:
        print("FAIL  --timeout-seconds must be greater than zero.")
        return 1

    try:
        plan = load_plan(args.plan)
        problems = validate_plan(plan)
        for caller in ("authorized", "restricted"):
            token_from_environment(getattr(args, f"{caller}_token_env"), caller)
    except ValueError as error:
        print(f"FAIL  {error}")
        return 1

    if problems:
        print("FAIL  surface probe plan is not usable:")
        for problem in problems:
            print(f"FAIL  {problem}")
        return 1

    print(f"== Probing deployed surface with {args.timeout_seconds:g}-second request timeouts ==")
    failures: list[str] = []
    for caller in CALLERS:
        verify_caller(
            caller,
            plan["callers"][caller],
            args.endpoint,
            plan["request"],
            args,
            failures,
        )
    if failures:
        print(f"FAIL  surface verification failed ({len(failures)} assertion(s)).")
        return 1
    print("PASS  surface verification completed with no access-boundary failures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
