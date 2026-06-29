#!/usr/bin/env python3
"""Extract a single icon from an SF Symbols template SVG.

SF Symbols exports contain notes, guides, and multiple weight/scale variants.
This script keeps one symbol group, removes template-only attributes/classes,
and writes a compact SVG that can be used in web documentation.
"""

from __future__ import annotations

import argparse
import copy
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_matrix_translate(transform: str) -> tuple[float, float] | None:
    match = re.fullmatch(
        r"\s*matrix\(\s*1(?:\.0+)?\s+0(?:\.0+)?\s+0(?:\.0+)?\s+1(?:\.0+)?\s+"
        r"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)\s*",
        transform,
    )
    if not match:
        return None
    return float(match.group(1)), float(match.group(2))


def find_group(root: ET.Element, group_id: str) -> ET.Element | None:
    for element in root.iter():
        if local_name(element.tag) == "g" and element.get("id") == group_id:
            return element
    return None


def symbol_group_ids(root: ET.Element) -> list[str]:
    symbols = find_group(root, "Symbols")
    if symbols is None:
        return []

    return [
        child.get("id", "")
        for child in list(symbols)
        if local_name(child.tag) == "g" and child.get("id")
    ]


def path_numbers(path_data: str) -> list[float]:
    return [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", path_data)]


def path_bounds(path_data: str) -> tuple[float, float, float, float]:
    values = path_numbers(path_data)
    if len(values) < 2:
        raise ValueError("Path has no coordinate data")

    xs = values[0::2]
    ys = values[1::2]
    return min(xs), min(ys), max(xs), max(ys)


def combined_bounds(paths: list[ET.Element]) -> tuple[float, float, float, float]:
    bounds = [path_bounds(path.get("d", "")) for path in paths]
    return (
        min(bound[0] for bound in bounds),
        min(bound[1] for bound in bounds),
        max(bound[2] for bound in bounds),
        max(bound[3] for bound in bounds),
    )


def clean_symbol_group(group: ET.Element, keep_transform: bool) -> ET.Element:
    symbol = copy.deepcopy(group)
    symbol.attrib.pop("id", None)

    if not keep_transform:
        symbol.attrib.pop("transform", None)
    elif transform := symbol.get("transform"):
        if translate := parse_matrix_translate(transform):
            symbol.set("transform", f"translate({translate[0]:g} {translate[1]:g})")

    for element in symbol.iter():
        element.attrib.pop("class", None)
        element.attrib.pop("style", None)
        element.attrib.pop("id", None)
        if local_name(element.tag) == "path":
            element.set("fill", "#666666")

    return symbol


def build_svg(group: ET.Element, view_box: str | None, keep_transform: bool) -> ET.Element:
    paths = [element for element in group.iter() if local_name(element.tag) == "path"]
    if not paths:
        raise ValueError("Selected symbol group does not contain any paths")

    if view_box is None:
        min_x, min_y, max_x, max_y = combined_bounds(paths)
        view_box = f"{min_x:g} {min_y:g} {max_x - min_x:g} {max_y - min_y:g}"

    svg = ET.Element(f"{{{SVG_NS}}}svg", {"viewBox": view_box})
    svg.append(clean_symbol_group(group, keep_transform))
    return svg


def indent_xml(element: ET.Element) -> None:
    ET.indent(element, space="  ")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract one weight/scale variant from an SF Symbols template SVG."
    )
    parser.add_argument("source", type=Path, help="SF Symbols template SVG to read")
    parser.add_argument("output", type=Path, help="Clean SVG file to write")
    parser.add_argument(
        "--group",
        default="Light-S",
        help="Symbol group id to extract (default: Light-S), e.g. Regular-S, Light-S, Light-M",
    )
    parser.add_argument(
        "--view-box",
        help="Override the generated viewBox, e.g. '0 0 100 100'",
    )
    parser.add_argument(
        "--keep-transform",
        action="store_true",
        help="Keep the selected symbol group's transform instead of cropping to its path bounds",
    )

    args = parser.parse_args()

    tree = ET.parse(args.source)
    root = tree.getroot()
    group = find_group(root, args.group)
    if group is None:
        available = ", ".join(symbol_group_ids(root)) or "none"
        print(
            f"Could not find symbol group {args.group!r}. Available groups: {available}",
            file=sys.stderr,
        )
        return 1

    svg = build_svg(group, args.view_box, args.keep_transform)
    indent_xml(svg)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(svg).write(args.output, encoding="utf-8", xml_declaration=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
