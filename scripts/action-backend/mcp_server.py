"""AI Starter Kit RVAS — Action Tools MCP server (FastMCP).

Wraps the FastAPI Action Tools backend (app.py) and exposes its operations as MCP
tools so a Foundry agent can attach them via `McpTool`. The agent calls these tools;
each tool forwards to the REST backend.

Env contract (matches .env.sample — AUTHORITATIVE for the Action Tools activity):
    ACTION_API_URL   base URL of the FastAPI backend   (default http://localhost:8080)
    ACTION_MCP_URL   the URL students attach as McpTool (default http://localhost:8765/mcp)
    ACTION_API_KEY   optional shared secret -> forwarded as x-api-key to the backend

Run (streamable-http transport on :8765/mcp):
    python mcp_server.py
    # or:  fastmcp run mcp_server.py --transport http --host 0.0.0.0 --port 8765

Attach in an agent (sketch):
    McpTool(server_label="northfield_actions", server_url=os.environ["ACTION_MCP_URL"])
"""
from __future__ import annotations

import os
from urllib.parse import urlparse

import httpx
from fastmcp import FastMCP

ACTION_API_URL = os.environ.get("ACTION_API_URL", "http://localhost:8080").rstrip("/")
ACTION_MCP_URL = os.environ.get("ACTION_MCP_URL", "http://localhost:8765/mcp")
ACTION_API_KEY = os.environ.get("ACTION_API_KEY", "").strip()

mcp = FastMCP("northfield-action-tools")


def _headers() -> dict:
    return {"x-api-key": ACTION_API_KEY} if ACTION_API_KEY else {}


def _post(path: str, payload: dict) -> dict:
    resp = httpx.post(f"{ACTION_API_URL}{path}", json=payload, headers=_headers(), timeout=30.0)
    resp.raise_for_status()
    return resp.json()


@mcp.tool
def create_it_ticket(
    student_id: str,
    summary: str,
    category: str = "other",
    priority: str = "normal",
) -> dict:
    """Create an IT support ticket for a student.

    category: one of wifi | account | hardware | software | other.
    priority: one of low | normal | high | urgent.
    Returns the created ticket including its ticket_id and status.
    """
    return _post(
        "/it-tickets",
        {"student_id": student_id, "summary": summary, "category": category, "priority": priority},
    )


@mcp.tool
def place_course_hold(student_id: str, course_code: str, reason: str) -> dict:
    """Place a registration hold on a course for a student.

    Returns the created hold including its hold_id and status.
    """
    return _post(
        "/course-holds",
        {"student_id": student_id, "course_code": course_code, "reason": reason},
    )


@mcp.tool
def book_advising_slot(
    student_id: str,
    advisor: str,
    iso_datetime: str,
    topic: str = "General advising",
) -> dict:
    """Book an academic advising slot for a student.

    iso_datetime: ISO 8601 timestamp, e.g. 2026-06-10T15:00:00Z.
    Returns the booking including its booking_id and status.
    """
    return _post(
        "/advising-slots",
        {"student_id": student_id, "advisor": advisor, "iso_datetime": iso_datetime, "topic": topic},
    )


if __name__ == "__main__":
    parsed = urlparse(ACTION_MCP_URL)
    host = parsed.hostname or "0.0.0.0"
    port = parsed.port or 8765
    path = parsed.path or "/mcp"
    print(f"Action Tools MCP server -> http://{host}:{port}{path}  (backend: {ACTION_API_URL})")
    mcp.run(transport="http", host=host, port=port, path=path)
