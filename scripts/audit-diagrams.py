#!/usr/bin/env python3
"""Audit scenario Excalidraw diagrams for broken arrow geometry.

The lesson pages render PNGs generated from ``scenarios/*/diagrams/*.excalidraw``.
This checker catches geometry that is visibly bad in those renders:

- arrow endpoints inside shapes;
- arrows crossing through unrelated shapes;
- dangling arrow endpoints;
- overlapping shapes;
- text overflowing its container;
- broken element id references.

Unbound arrows are reported as warnings by default because some existing straight-line
flows render cleanly with explicit 2px gaps. Pass ``--strict-bindings`` to make missing
``startBinding``/``endBinding`` fail as well.
"""

from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


SHAPES = {"rectangle", "ellipse", "diamond"}
CRITICAL_KINDS = {
    "arrow-crosses-shape",
    "arrow-dangling",
    "arrow-penetrates",
    "broken-ref",
    "shape-overlap",
    "text-overflow",
}


def bbox(element: dict[str, Any]) -> tuple[float, float, float, float]:
    x = float(element.get("x", 0))
    y = float(element.get("y", 0))
    width = float(element.get("width", 0))
    height = float(element.get("height", 0))
    return (min(x, x + width), min(y, y + height), max(x, x + width), max(y, y + height))


def point_in_bbox(point: tuple[float, float], box: tuple[float, float, float, float], pad: float = 0) -> bool:
    return box[0] - pad <= point[0] <= box[2] + pad and box[1] - pad <= point[1] <= box[3] + pad


def point_in_shape(point: tuple[float, float], shape: dict[str, Any], pad: float = 0) -> bool:
    box = bbox(shape)
    if shape.get("type") == "ellipse":
        cx = (box[0] + box[2]) / 2
        cy = (box[1] + box[3]) / 2
        rx = max((box[2] - box[0]) / 2 + pad, 1)
        ry = max((box[3] - box[1]) / 2 + pad, 1)
        return ((point[0] - cx) / rx) ** 2 + ((point[1] - cy) / ry) ** 2 <= 1
    if shape.get("type") == "diamond":
        cx = (box[0] + box[2]) / 2
        cy = (box[1] + box[3]) / 2
        rx = max((box[2] - box[0]) / 2 + pad, 1)
        ry = max((box[3] - box[1]) / 2 + pad, 1)
        return abs(point[0] - cx) / rx + abs(point[1] - cy) / ry <= 1
    return point_in_bbox(point, box, pad)


def distance_to_bbox(point: tuple[float, float], box: tuple[float, float, float, float]) -> float:
    dx = max(box[0] - point[0], 0, point[0] - box[2])
    dy = max(box[1] - point[1], 0, point[1] - box[3])
    return math.hypot(dx, dy)


def overlap_area(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> tuple[float, float, float]:
    width = min(first[2], second[2]) - max(first[0], second[0])
    height = min(first[3], second[3]) - max(first[1], second[1])
    return (width, height, width * height if width > 0 and height > 0 else 0)


def is_containment(first: tuple[float, float, float, float], second: tuple[float, float, float, float]) -> bool:
    return (
        (first[0] <= second[0] and first[1] <= second[1] and first[2] >= second[2] and first[3] >= second[3])
        or (second[0] <= first[0] and second[1] <= first[1] and second[2] >= first[2] and second[3] >= first[3])
    )


def absolute_points(arrow: dict[str, Any]) -> list[tuple[float, float]]:
    x = float(arrow.get("x", 0))
    y = float(arrow.get("y", 0))
    return [(x + float(point[0]), y + float(point[1])) for point in arrow.get("points", [])]


def segment_crosses_shape(
    start: tuple[float, float],
    end: tuple[float, float],
    shape: dict[str, Any],
) -> bool:
    """Sample a segment and detect whether it visibly travels through a shape body."""
    hits = 0
    for step in range(1, 20):
        t = step / 20
        point = (start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t)
        if point_in_shape(point, shape):
            hits += 1
    return hits > 2


def audit_file(path: Path) -> list[tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    elements = [element for element in data.get("elements", []) if not element.get("isDeleted")]
    by_id = {element["id"]: element for element in elements}
    shapes = [element for element in elements if element.get("type") in SHAPES]
    arrows = [element for element in elements if element.get("type") == "arrow"]
    issues: list[tuple[str, str]] = []

    for element in elements:
        for bound_element in element.get("boundElements") or []:
            target = bound_element.get("id")
            if target not in by_id:
                issues.append(("broken-ref", f"{element['id']}.boundElements -> missing {target}"))
        for key in ("startBinding", "endBinding"):
            binding = element.get(key)
            if binding and binding.get("elementId") not in by_id:
                issues.append(("broken-ref", f"{element['id']}.{key} -> missing {binding.get('elementId')}"))
        container_id = element.get("containerId")
        if container_id and container_id not in by_id:
            issues.append(("broken-ref", f"{element['id']}.containerId -> missing {container_id}"))

    for arrow in arrows:
        points = absolute_points(arrow)
        if len(points) < 2:
            issues.append(("arrow-dangling", f"{arrow['id']} has fewer than two points"))
            continue
        for label, point, key in (
            ("start", points[0], "startBinding"),
            ("end", points[-1], "endBinding"),
        ):
            nearest = sorted(
                ((distance_to_bbox(point, bbox(shape)), shape) for shape in shapes),
                key=lambda item: item[0],
            )
            if not nearest:
                continue
            distance, shape = nearest[0]
            inside = [candidate for candidate in shapes if point_in_shape(point, candidate)]
            if inside:
                issues.append(("arrow-penetrates", f"{arrow['id']} {label} inside {inside[0]['id']}"))
            elif not arrow.get(key) and distance <= 24:
                issues.append(
                    (
                        "arrow-unbound",
                        f"{arrow['id']} {label} touches {shape['id']} (gap {distance:.0f}) but {key} is null",
                    )
                )
            elif not arrow.get(key) and distance > 24:
                issues.append(("arrow-dangling", f"{arrow['id']} {label} nearest shape {shape['id']} is {distance:.0f}px away"))

    for index, first in enumerate(shapes):
        for second in shapes[index + 1 :]:
            first_box = bbox(first)
            second_box = bbox(second)
            width, height, area = overlap_area(first_box, second_box)
            if area > 0 and not is_containment(first_box, second_box):
                issues.append(("shape-overlap", f"{first['id']} x {second['id']} ({width:.0f}x{height:.0f}px)"))

    for arrow in arrows:
        points = absolute_points(arrow)
        if len(points) < 2:
            continue
        endpoint_ids = {
            (arrow.get("startBinding") or {}).get("elementId"),
            (arrow.get("endBinding") or {}).get("elementId"),
        }
        for shape in shapes:
            if shape["id"] in endpoint_ids:
                continue
            for start, end in zip(points, points[1:]):
                if segment_crosses_shape(start, end, shape):
                    issues.append(("arrow-crosses-shape", f"{arrow['id']} passes through {shape['id']}"))
                    break

    for element in elements:
        if element.get("type") != "text":
            continue
        container_id = element.get("containerId")
        if not container_id or container_id not in by_id:
            continue
        text_box = bbox(element)
        container_box = bbox(by_id[container_id])
        if (
            text_box[0] < container_box[0] - 1
            or text_box[1] < container_box[1] - 1
            or text_box[2] > container_box[2] + 1
            or text_box[3] > container_box[3] + 1
        ):
            issues.append(("text-overflow", f"{element['id']} out of {container_id}"))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=sorted(glob.glob("scenarios/*/diagrams/*.excalidraw")))
    parser.add_argument("--strict-bindings", action="store_true", help="treat unbound arrows as failures")
    args = parser.parse_args()

    total = Counter()
    failed = False
    for raw_path in args.paths:
        path = Path(raw_path)
        issues = audit_file(path)
        failures = [
            issue
            for issue in issues
            if issue[0] in CRITICAL_KINDS or (args.strict_bindings and issue[0] == "arrow-unbound")
        ]
        if failures:
            failed = True
            print(f"\n{path}")
            for kind, message in failures:
                print(f"  FAIL  {kind}: {message}")
                total[kind] += 1
        for kind, _message in issues:
            if kind == "arrow-unbound" and not args.strict_bindings:
                total[kind] += 1

    if total:
        print("\nDiagram audit totals:")
        for kind, count in sorted(total.items()):
            label = "warn" if kind == "arrow-unbound" and not args.strict_bindings else "fail"
            print(f"  {label:4} {count:4d} {kind}")
    else:
        print("Diagram audit passed: no issues found.")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
