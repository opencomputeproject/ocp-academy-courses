#!/usr/bin/env python3
"""
check_svg_arrows.py - flag SVG arrow geometry mistakes.

Usage:
    python check_svg_arrows.py course.json --fail-on-flags
    python check_svg_arrows.py figures/
    python check_svg_arrows.py figures/example.svg --fail-on-flags

The check focuses on the common problematic pattern in Academy diagrams:
curved or diagonal paths using a triangular marker whose refX is near the
point of the arrowhead. For those arrows, the line should end at the center of
the flat back side of the arrowhead, with the arrowhead extending forward from
that endpoint. It also catches explicit arrowhead polygons whose point intrudes
into a target rectangle instead of stopping on the target boundary.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


NUMBER_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?")
MARKER_URL_RE = re.compile(r"url\(\s*['\"]?#([^'\"\)\s]+)['\"]?\s*\)")
CSS_MARKER_RE = re.compile(
    r"\.([A-Za-z0-9_-]+)\s*\{[^}]*?marker-end\s*:\s*url\(\s*#([^)'\"]+)\s*\)",
    re.S,
)
TRANSLATE_RE = re.compile(
    r"translate\(\s*([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?)"
    r"(?:[\s,]+([-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?))?\s*\)"
)


@dataclass(frozen=True)
class MarkerShape:
    marker_id: str
    ref_x: float
    min_x: float
    max_x: float
    is_tip_attached: bool


@dataclass(frozen=True)
class Issue:
    svg: Path
    line: int | None
    marker_id: str
    element: str
    detail: str


@dataclass(frozen=True)
class RectShape:
    x: float
    y: float
    width: float
    height: float
    element: ET.Element

    def contains_strict(self, point: tuple[float, float], tolerance: float = 0.5) -> bool:
        px, py = point
        return (
            self.x + tolerance < px < self.x + self.width - tolerance
            and self.y + tolerance < py < self.y + self.height - tolerance
        )


@dataclass(frozen=True)
class PolygonShape:
    points: list[tuple[float, float]]
    element: ET.Element


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def first_number(value: str | None, default: float = 0.0) -> float:
    if not value:
        return default
    match = NUMBER_RE.search(value)
    return float(match.group(0)) if match else default


def parse_translate(value: str | None) -> tuple[float, float]:
    if not value:
        return 0.0, 0.0
    dx = 0.0
    dy = 0.0
    for match in TRANSLATE_RE.finditer(value):
        dx += float(match.group(1))
        dy += float(match.group(2) or 0.0)
    return dx, dy


def coord_pairs(text: str | None) -> list[tuple[float, float]]:
    if not text:
        return []
    values = [float(n) for n in NUMBER_RE.findall(text)]
    return list(zip(values[0::2], values[1::2]))


def points_attr_pairs(text: str | None) -> list[tuple[float, float]]:
    return coord_pairs(text)


def translated_points(points: list[tuple[float, float]], dx: float, dy: float) -> list[tuple[float, float]]:
    return [(x + dx, y + dy) for x, y in points]


def marker_id_from_url(value: str | None) -> str | None:
    if not value:
        return None
    match = MARKER_URL_RE.search(value)
    return match.group(1) if match else None


def stylesheet_marker_map(root: ET.Element) -> dict[str, str]:
    style_text = "\n".join(
        element.text or "" for element in root.iter() if local_name(element.tag) == "style"
    )
    return {class_name: marker_id.strip() for class_name, marker_id in CSS_MARKER_RE.findall(style_text)}


def element_marker_id(element: ET.Element, class_markers: dict[str, str]) -> str | None:
    marker_id = marker_id_from_url(element.get("marker-end"))
    if marker_id:
        return marker_id

    style_marker = re.search(r"marker-end\s*:\s*url\(\s*#([^)'\"]+)\s*\)", element.get("style", ""))
    if style_marker:
        return style_marker.group(1).strip()

    for class_name in element.get("class", "").split():
        if class_name in class_markers:
            return class_markers[class_name]
    return None


def marker_points(marker: ET.Element) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for child in marker.iter():
        name = local_name(child.tag)
        if name == "path":
            points.extend(coord_pairs(child.get("d")))
        elif name in {"polygon", "polyline"}:
            points.extend(points_attr_pairs(child.get("points")))
    return points


def marker_shapes(root: ET.Element) -> dict[str, MarkerShape]:
    shapes: dict[str, MarkerShape] = {}
    for marker in root.iter():
        if local_name(marker.tag) != "marker":
            continue
        marker_id = marker.get("id")
        if not marker_id:
            continue
        points = marker_points(marker)
        if len(points) < 3:
            continue

        xs = [point[0] for point in points]
        min_x = min(xs)
        max_x = max(xs)
        width = max_x - min_x
        if width <= 0:
            continue

        ref_x = first_number(marker.get("refX"), default=0.0)
        tip_tolerance = max(0.75, width * 0.2)
        is_tip_attached = abs(ref_x - max_x) <= tip_tolerance
        shapes[marker_id] = MarkerShape(marker_id, ref_x, min_x, max_x, is_tip_attached)
    return shapes


def all_close(values: list[float], tolerance: float = 0.01) -> bool:
    if not values:
        return True
    first = values[0]
    return all(abs(value - first) <= tolerance for value in values)


def points_are_cardinal(points: list[tuple[float, float]]) -> bool:
    if len(points) < 2:
        return True
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return all_close(xs) or all_close(ys)


def element_points(element: ET.Element) -> list[tuple[float, float]]:
    name = local_name(element.tag)
    if name == "path":
        return coord_pairs(element.get("d"))
    if name == "line":
        return [
            (first_number(element.get("x1")), first_number(element.get("y1"))),
            (first_number(element.get("x2")), first_number(element.get("y2"))),
        ]
    if name in {"polyline", "polygon"}:
        return points_attr_pairs(element.get("points"))
    return []


def element_is_curved_or_diagonal(element: ET.Element) -> bool:
    points = element_points(element)
    if not points:
        return True
    return not points_are_cardinal(points)


def element_label(element: ET.Element) -> str:
    name = local_name(element.tag)
    bits = [f"<{name}"]
    class_name = element.get("class")
    if class_name:
        bits.append(f' class="{class_name}"')
    if element.get("d"):
        bits.append(f' d="{element.get("d")}"')
    elif name == "line":
        bits.append(
            f' x1="{element.get("x1")}" y1="{element.get("y1")}"'
            f' x2="{element.get("x2")}" y2="{element.get("y2")}"'
        )
    bits.append(">")
    return "".join(bits)


def viewbox_area(root: ET.Element) -> float | None:
    values = [float(n) for n in NUMBER_RE.findall(root.get("viewBox") or "")]
    if len(values) == 4 and values[2] > 0 and values[3] > 0:
        return values[2] * values[3]
    return None


def collect_geometry(
    element: ET.Element,
    dx: float = 0.0,
    dy: float = 0.0,
    in_marker: bool = False,
    max_rect_area: float | None = None,
) -> tuple[list[RectShape], list[PolygonShape]]:
    local_dx, local_dy = parse_translate(element.get("transform"))
    dx += local_dx
    dy += local_dy
    in_marker = in_marker or local_name(element.tag) == "marker"

    rects: list[RectShape] = []
    polygons: list[PolygonShape] = []
    name = local_name(element.tag)

    if not in_marker and name == "rect":
        width = first_number(element.get("width"))
        height = first_number(element.get("height"))
        area = width * height
        class_name = element.get("class", "")
        if (
            width > 0
            and height > 0
            and "bg" not in class_name.split()
            and "panel" not in class_name.split()
            and (max_rect_area is None or area <= max_rect_area)
        ):
            rects.append(
                RectShape(
                    x=first_number(element.get("x")) + dx,
                    y=first_number(element.get("y")) + dy,
                    width=width,
                    height=height,
                    element=element,
                )
            )
    elif not in_marker and name == "polygon":
        points = points_attr_pairs(element.get("points"))
        if points:
            polygons.append(PolygonShape(translated_points(points, dx, dy), element))

    for child in list(element):
        child_rects, child_polygons = collect_geometry(
            child,
            dx=dx,
            dy=dy,
            in_marker=in_marker,
            max_rect_area=max_rect_area,
        )
        rects.extend(child_rects)
        polygons.extend(child_polygons)

    return rects, polygons


def arrowhead_tip(points: list[tuple[float, float]], tolerance: float = 0.5) -> tuple[float, float] | None:
    if len(points) != 3:
        return None

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]

    max_x = max(xs)
    min_x = min(xs)
    max_y = max(ys)
    min_y = min(ys)

    right_tip = [point for point in points if abs(point[0] - max_x) <= tolerance]
    left_tip = [point for point in points if abs(point[0] - min_x) <= tolerance]
    down_tip = [point for point in points if abs(point[1] - max_y) <= tolerance]
    up_tip = [point for point in points if abs(point[1] - min_y) <= tolerance]

    if len(right_tip) == 1 and len(left_tip) == 2:
        return right_tip[0]
    if len(left_tip) == 1 and len(right_tip) == 2:
        return left_tip[0]
    if len(down_tip) == 1 and len(up_tip) == 2:
        return down_tip[0]
    if len(up_tip) == 1 and len(down_tip) == 2:
        return up_tip[0]
    return None


def polygon_is_arrowhead(polygon: PolygonShape) -> bool:
    class_names = polygon.element.get("class", "").split()
    if any("arrowhead" in class_name for class_name in class_names):
        return True
    return arrowhead_tip(polygon.points) is not None


def line_number_for_element(source: str, element: ET.Element) -> int | None:
    candidates = [
        element.get("d"),
        element.get("points"),
        element.get("class"),
        element.get("marker-end"),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        for index, line in enumerate(source.splitlines(), start=1):
            if candidate in line:
                return index
    return None


def check_svg(svg: Path) -> tuple[list[Issue], list[str]]:
    warnings: list[str] = []
    issues: list[Issue] = []
    try:
        source = svg.read_text(encoding="utf-8")
        root = ET.fromstring(source)
    except UnicodeDecodeError as exc:
        return [], [f"{svg}: could not read as UTF-8 SVG: {exc}"]
    except ET.ParseError as exc:
        return [], [f"{svg}: SVG XML parse failed: {exc}"]

    class_markers = stylesheet_marker_map(root)
    shapes = marker_shapes(root)
    checked_tags = {"path", "line", "polyline"}

    for element in root.iter():
        if local_name(element.tag) not in checked_tags:
            continue
        marker_id = element_marker_id(element, class_markers)
        if not marker_id:
            continue
        shape = shapes.get(marker_id)
        if not shape or not shape.is_tip_attached:
            continue
        if not element_is_curved_or_diagonal(element):
            continue

        issues.append(
            Issue(
                svg=svg,
                line=line_number_for_element(source, element),
                marker_id=marker_id,
                element=element_label(element),
                detail=(
                    "curved or diagonal arrow uses a triangular marker whose refX is near "
                    "the arrow point; end the line at the flat-back center or use an "
                    "explicit same-color arrowhead polygon"
                ),
            )
        )

    root_area = viewbox_area(root)
    max_rect_area = root_area * 0.35 if root_area else None
    rects, polygons = collect_geometry(root, max_rect_area=max_rect_area)
    for polygon in polygons:
        if not polygon_is_arrowhead(polygon):
            continue
        tip = arrowhead_tip(polygon.points)
        if tip is None:
            continue
        for rect in rects:
            if not rect.contains_strict(tip):
                continue
            issues.append(
                Issue(
                    svg=svg,
                    line=line_number_for_element(source, polygon.element),
                    marker_id="explicit-arrowhead",
                    element=element_label(polygon.element),
                    detail=(
                        "arrowhead tip is inside a rectangle; stop the point on the "
                        "target object's boundary line and keep the arrowhead outside "
                        "the target shape"
                    ),
                )
            )
            break
    return issues, warnings


def collect_from_json(course_json: Path) -> list[Path]:
    data = json.loads(course_json.read_text(encoding="utf-8"))
    root = course_json.parent
    found: list[Path] = []

    def walk(value):
        if isinstance(value, dict):
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, str) and value.lower().endswith(".svg"):
            path = Path(value)
            svg = path if path.is_absolute() else root / path
            if svg.exists():
                found.append(svg)

    walk(data)
    figures_dir = root / "figures"
    if figures_dir.is_dir():
        found.extend(figures_dir.glob("*.svg"))
    return found


def collect_svg_files(inputs: list[Path]) -> tuple[list[Path], list[str]]:
    if not inputs:
        if Path("course.json").exists():
            inputs = [Path("course.json")]
        elif Path("figures").is_dir():
            inputs = [Path("figures")]

    warnings: list[str] = []
    collected: list[Path] = []
    for item in inputs:
        path = item.expanduser()
        if path.is_dir():
            figures_dir = path / "figures"
            search_root = figures_dir if figures_dir.is_dir() else path
            collected.extend(search_root.rglob("*.svg"))
        elif path.is_file() and path.suffix.lower() == ".json":
            collected.extend(collect_from_json(path))
        elif path.is_file() and path.suffix.lower() == ".svg":
            collected.append(path)
        elif not path.exists():
            warnings.append(f"{path}: path does not exist")
        else:
            warnings.append(f"{path}: not an SVG, JSON course file, or directory")

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in collected:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Flag SVG arrow geometry where lines connect to arrowhead tips or arrowheads intrude into target shapes."
    )
    parser.add_argument("paths", nargs="*", type=Path, help="course.json, SVG files, or folders to scan")
    parser.add_argument(
        "--fail-on-flags",
        action="store_true",
        help="exit with status 1 when arrow geometry issues are found",
    )
    args = parser.parse_args()

    svg_files, warnings = collect_svg_files(args.paths)
    if not svg_files and not warnings:
        warnings.append("No SVG files found to check")

    issues: list[Issue] = []
    for svg in svg_files:
        file_issues, file_warnings = check_svg(svg)
        issues.extend(file_issues)
        warnings.extend(file_warnings)

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for warning in warnings:
            print(f"  - {warning}")

    if issues:
        print(f"\n{len(issues)} SVG arrow issue(s):")
        for issue in issues:
            location = f"{issue.svg}"
            if issue.line:
                location += f":{issue.line}"
            print(f"  - {location}: {issue.marker_id} on {issue.element}")
            print(f"    {issue.detail}")
        print(
            "\nFix: make the path endpoint the arrowhead's flat-back center, "
            "draw the head forward from that point, and place the tip on the "
            "target object's boundary line."
        )
        return 1 if args.fail_on_flags else 0

    print(f"\nOK - SVG arrow geometry check passed for {len(svg_files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
