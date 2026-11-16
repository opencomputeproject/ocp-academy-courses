#!/usr/bin/env python3
"""
check_svg_arrows.py - flag SVG arrow geometry mistakes.

Usage:
    python check_svg_arrows.py course.json --fail-on-flags
    python check_svg_arrows.py figures/ animations/
    python check_svg_arrows.py figures/example.svg --fail-on-flags

The check focuses on the common problematic pattern in Academy diagrams:
paths using a triangular marker whose reference point is not at the center of
the arrowhead's flat back side. Every arrow shaft must end at that flat-back
center, with the arrowhead extending forward from the endpoint. The checker
also scans inline SVG in animation HTML, verifies explicit polygons marked with
class="arrowhead" connect at their flat-back center, and catches arrowhead tips
that intrude into target rectangles.
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
INLINE_SVG_RE = re.compile(r"<svg\b[\s\S]*?</svg>", re.I)
PATH_TOKEN_RE = re.compile(
    r"[A-Za-z]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?"
)


@dataclass(frozen=True)
class MarkerShape:
    marker_id: str
    ref_x: float
    ref_y: float
    tip: tuple[float, float]
    back_center: tuple[float, float]
    is_back_attached: bool


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


@dataclass(frozen=True)
class ConnectorShape:
    start: tuple[float, float]
    previous: tuple[float, float]
    end: tuple[float, float]
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
        tip = arrowhead_tip(points)
        if tip is None:
            continue
        back_points = list(points)
        back_points.remove(tip)
        if len(back_points) != 2:
            continue

        ref_x = first_number(marker.get("refX"), default=0.0)
        ref_y = first_number(marker.get("refY"), default=0.0)
        back_center = (
            (back_points[0][0] + back_points[1][0]) / 2,
            (back_points[0][1] + back_points[1][1]) / 2,
        )
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        tolerance = max(0.75, max(max(xs) - min(xs), max(ys) - min(ys)) * 0.08)
        distance = ((ref_x - back_center[0]) ** 2 + (ref_y - back_center[1]) ** 2) ** 0.5
        shapes[marker_id] = MarkerShape(
            marker_id=marker_id,
            ref_x=ref_x,
            ref_y=ref_y,
            tip=tip,
            back_center=back_center,
            is_back_attached=distance <= tolerance,
        )
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


PATH_PARAM_COUNTS = {
    "M": 2,
    "L": 2,
    "H": 1,
    "V": 1,
    "C": 6,
    "S": 4,
    "Q": 4,
    "T": 2,
    "A": 7,
}


def path_terminal_segment(
    value: str | None,
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]] | None:
    """Return path start, last tangent/control point, and final endpoint."""
    if not value:
        return None
    tokens = PATH_TOKEN_RE.findall(value)
    index = 0
    command: str | None = None
    current = (0.0, 0.0)
    subpath_start = current
    start: tuple[float, float] | None = None
    previous = current
    end = current

    def point(x: float, y: float, relative: bool, origin: tuple[float, float]) -> tuple[float, float]:
        return (x + origin[0], y + origin[1]) if relative else (x, y)

    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command.upper() == "Z":
                previous = current
                current = subpath_start
                end = current
            continue
        if command is None:
            break

        upper = command.upper()
        count = PATH_PARAM_COUNTS.get(upper)
        if count is None or index + count > len(tokens):
            break
        raw = tokens[index : index + count]
        if any(item.isalpha() for item in raw):
            break
        values = [float(item) for item in raw]
        index += count
        relative = command.islower()
        origin = current

        if upper == "M":
            current = point(values[0], values[1], relative, origin)
            subpath_start = current
            if start is None:
                start = current
            previous = origin
            end = current
            command = "l" if relative else "L"
        elif upper in {"L", "T"}:
            previous = origin
            current = point(values[-2], values[-1], relative, origin)
            end = current
        elif upper == "H":
            previous = origin
            current = (values[0] + origin[0], origin[1]) if relative else (values[0], origin[1])
            end = current
        elif upper == "V":
            previous = origin
            current = (origin[0], values[0] + origin[1]) if relative else (origin[0], values[0])
            end = current
        elif upper == "C":
            previous = point(values[2], values[3], relative, origin)
            current = point(values[4], values[5], relative, origin)
            end = current
        elif upper in {"S", "Q"}:
            previous = point(values[0], values[1], relative, origin)
            current = point(values[2], values[3], relative, origin)
            end = current
        elif upper == "A":
            previous = origin
            current = point(values[5], values[6], relative, origin)
            end = current

    if start is None:
        return None
    return start, previous, end


def element_terminal_segment(
    element: ET.Element,
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]] | None:
    name = local_name(element.tag)
    if name == "path":
        return path_terminal_segment(element.get("d"))
    if name == "line":
        start = (first_number(element.get("x1")), first_number(element.get("y1")))
        end = (first_number(element.get("x2")), first_number(element.get("y2")))
        return start, start, end
    if name == "polyline":
        points = points_attr_pairs(element.get("points"))
        if len(points) >= 2:
            return points[0], points[-2], points[-1]
    return None


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


def collect_connectors(
    element: ET.Element,
    dx: float = 0.0,
    dy: float = 0.0,
    in_marker: bool = False,
) -> list[ConnectorShape]:
    local_dx, local_dy = parse_translate(element.get("transform"))
    dx += local_dx
    dy += local_dy
    in_marker = in_marker or local_name(element.tag) == "marker"
    connectors: list[ConnectorShape] = []

    if not in_marker:
        segment = element_terminal_segment(element)
        if segment is not None:
            start, previous, end = segment
            connectors.append(
                ConnectorShape(
                    start=(start[0] + dx, start[1] + dy),
                    previous=(previous[0] + dx, previous[1] + dy),
                    end=(end[0] + dx, end[1] + dy),
                    element=element,
                )
            )

    for child in list(element):
        connectors.extend(collect_connectors(child, dx=dx, dy=dy, in_marker=in_marker))
    return connectors


def arrowhead_tip(points: list[tuple[float, float]], tolerance: float = 0.5) -> tuple[float, float] | None:
    if len(points) != 3:
        return None

    edges = [
        (point_distance(points[0], points[1]), points[2]),
        (point_distance(points[1], points[2]), points[0]),
        (point_distance(points[2], points[0]), points[1]),
    ]
    edges.sort(key=lambda item: item[0])
    if edges[0][0] <= tolerance or edges[0][0] > edges[1][0] * 0.97:
        return None
    return edges[0][1]


def arrowhead_back_center(
    points: list[tuple[float, float]],
) -> tuple[tuple[float, float], tuple[float, float]] | None:
    tip = arrowhead_tip(points)
    if tip is None:
        return None
    back_points = list(points)
    back_points.remove(tip)
    if len(back_points) != 2:
        return None
    center = (
        (back_points[0][0] + back_points[1][0]) / 2,
        (back_points[0][1] + back_points[1][1]) / 2,
    )
    return tip, center


def point_distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def connector_aligns_with_arrowhead(
    connector: ConnectorShape,
    back_center: tuple[float, float],
    tip: tuple[float, float],
) -> bool:
    shaft = (
        connector.end[0] - connector.previous[0],
        connector.end[1] - connector.previous[1],
    )
    head = (tip[0] - back_center[0], tip[1] - back_center[1])
    shaft_length = (shaft[0] ** 2 + shaft[1] ** 2) ** 0.5
    head_length = (head[0] ** 2 + head[1] ** 2) ** 0.5
    if shaft_length == 0 or head_length == 0:
        return False
    cosine = (shaft[0] * head[0] + shaft[1] * head[1]) / (shaft_length * head_length)
    return cosine >= 0.9


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


def parse_svg_roots(artwork: Path, source: str) -> tuple[list[ET.Element], list[str]]:
    warnings: list[str] = []
    if artwork.suffix.lower() == ".svg":
        try:
            return [ET.fromstring(source)], warnings
        except ET.ParseError as exc:
            return [], [f"{artwork}: SVG XML parse failed: {exc}"]

    roots: list[ET.Element] = []
    matches = list(INLINE_SVG_RE.finditer(source))
    if not matches:
        return [], [f"{artwork}: no inline SVG found"]
    for index, match in enumerate(matches, start=1):
        try:
            roots.append(ET.fromstring(match.group(0)))
        except ET.ParseError as exc:
            warnings.append(f"{artwork}: inline SVG {index} XML parse failed: {exc}")
    return roots, warnings


def check_artwork(artwork: Path) -> tuple[list[Issue], list[str]]:
    warnings: list[str] = []
    issues: list[Issue] = []
    try:
        source = artwork.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [], [f"{artwork}: could not read as UTF-8 artwork: {exc}"]

    roots, parse_warnings = parse_svg_roots(artwork, source)
    warnings.extend(parse_warnings)
    for root in roots:
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
            if not shape or shape.is_back_attached:
                continue
            issues.append(
                Issue(
                    svg=artwork,
                    line=line_number_for_element(source, element),
                    marker_id=marker_id,
                    element=element_label(element),
                    detail=(
                        "arrow shaft attaches to a triangular marker away from the center "
                        "of its flat back side; set the marker reference to the flat-back "
                        "center or use an explicit class=\"arrowhead\" polygon"
                    ),
                )
            )

        root_area = viewbox_area(root)
        max_rect_area = root_area * 0.15 if root_area else None
        rects, polygons = collect_geometry(root, max_rect_area=max_rect_area)
        connectors = collect_connectors(root)
        for polygon in polygons:
            if not polygon_is_arrowhead(polygon):
                continue
            geometry = arrowhead_back_center(polygon.points)
            if geometry is None:
                continue
            tip, back_center = geometry
            for rect in rects:
                if not rect.contains_strict(tip):
                    continue
                issues.append(
                    Issue(
                        svg=artwork,
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

            class_names = polygon.element.get("class", "").split()
            if not any("arrowhead" in class_name for class_name in class_names):
                continue
            xs = [point[0] for point in polygon.points]
            ys = [point[1] for point in polygon.points]
            tolerance = max(1.5, max(max(xs) - min(xs), max(ys) - min(ys)) * 0.08)
            connected = [
                connector
                for connector in connectors
                if point_distance(connector.end, back_center) <= tolerance
            ]
            if not connected:
                issues.append(
                    Issue(
                        svg=artwork,
                        line=line_number_for_element(source, polygon.element),
                        marker_id="explicit-arrowhead",
                        element=element_label(polygon.element),
                        detail=(
                            "no arrow shaft ends at the midpoint of this arrowhead's flat "
                            "back side"
                        ),
                    )
                )
            elif not any(
                connector_aligns_with_arrowhead(connector, back_center, tip)
                for connector in connected
            ):
                issues.append(
                    Issue(
                        svg=artwork,
                        line=line_number_for_element(source, polygon.element),
                        marker_id="explicit-arrowhead",
                        element=element_label(polygon.element),
                        detail=(
                            "arrow shaft reaches the flat-back midpoint but its final "
                            "tangent does not align with the arrowhead direction"
                        ),
                    )
                )
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
    for animations_dir in (root / "animations", root.parent / "animations"):
        if not animations_dir.is_dir():
            continue
        found.extend(animations_dir.rglob("*.svg"))
        found.extend(animations_dir.rglob("*.html"))
        found.extend(animations_dir.rglob("*.htm"))
    return found


def collect_artwork_files(inputs: list[Path]) -> tuple[list[Path], list[str]]:
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
            collected.extend(search_root.rglob("*.html"))
            collected.extend(search_root.rglob("*.htm"))
        elif path.is_file() and path.suffix.lower() == ".json":
            collected.extend(collect_from_json(path))
        elif path.is_file() and path.suffix.lower() in {".svg", ".html", ".htm"}:
            collected.append(path)
        elif not path.exists():
            warnings.append(f"{path}: path does not exist")
        else:
            warnings.append(f"{path}: not SVG/HTML artwork, a JSON course file, or a directory")

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
        description="Flag SVG and inline-animation arrow geometry where shafts miss flat-back centers or arrowheads intrude into targets."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="course.json, SVG/HTML artwork files, or folders to scan",
    )
    parser.add_argument(
        "--fail-on-flags",
        action="store_true",
        help="exit with status 1 when arrow geometry issues are found",
    )
    args = parser.parse_args()

    artwork_files, warnings = collect_artwork_files(args.paths)
    if not artwork_files and not warnings:
        warnings.append("No SVG or inline-SVG animation files found to check")

    issues: list[Issue] = []
    for artwork in artwork_files:
        file_issues, file_warnings = check_artwork(artwork)
        issues.extend(file_issues)
        warnings.extend(file_warnings)

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for warning in warnings:
            print(f"  - {warning}")

    if issues:
        print(f"\n{len(issues)} arrow geometry issue(s):")
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

    print(f"\nOK - arrow geometry check passed for {len(artwork_files)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
