#!/usr/bin/env python3
"""Render JSON Schema files into Starlight Markdown reference pages.

Consumes the `*.schema.json` produced by `symbolgraph-to-schema.py` (the
version-controlled source of truth) and writes one Markdown page per top-level
schema, with a property table, nested-type sections, and links between types.
This script knows nothing about Swift — it is a pure JSON Schema -> Markdown step.

Usage:
    schema-to-markdown.py <schemas-dir> <out-dir>

Each `<Type>.schema.json` becomes `<out-dir>/<type-slug>.md` with Starlight
front matter. Add the generated pages to the sidebar in `astro.config.mjs`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def slug(name: str) -> str:
    """CamelCase type name -> kebab-case slug (EntityDefinition -> entity-definition)."""
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    return s.lower()


def anchor(name: str) -> str:
    return slug(name)


def escape_cell(text: str) -> str:
    """Make a string safe for a single Markdown table cell."""
    return text.replace("|", "\\|").replace("\n\n", " ").replace("\n", " ").strip()


def file_to_type(filename: str) -> str:
    return filename.replace(".schema.json", "")


def render_type(entry: dict) -> str:
    """Human-readable type label (with links) for a property's schema fragment."""
    if "$ref" in entry:
        return render_ref(entry["$ref"])
    t = entry.get("type")
    if t == "array":
        items = entry.get("items", {})
        return f"Array&lt;{render_type(items)}&gt;"
    if t == "object":
        if entry.get("additionalProperties") not in (None, False):
            ap = entry["additionalProperties"]
            inner = render_type(ap) if isinstance(ap, dict) and ap else "Any"
            return f"Object&lt;{inner}&gt;" if inner != "Any" else "Object"
        return "Object"
    if "enum" in entry:
        base = t or "string"
        return f"{base} (enum)"
    if t:
        fmt = entry.get("format")
        return f"{t} ({fmt})" if fmt else t
    return "any"


def render_ref(ref: str) -> str:
    """Turn a $ref into a linked type label."""
    if ref == "#":
        return "(self)"
    if ref.startswith("#/$defs/"):
        name = ref.rsplit("/", 1)[-1]
        return f"[{name}](#{anchor(name)})"
    # cross-file: <Type>.schema.json  or  <Type>.schema.json#/$defs/Nested
    file_part, _, frag = ref.partition("#")
    type_name = file_to_type(file_part)
    page = slug(type_name)
    if frag.startswith("/$defs/"):
        nested = frag.rsplit("/", 1)[-1]
        return f"[{nested}](/reference/{page}/#{anchor(nested)})"
    return f"[{type_name}](/reference/{page}/)"


def property_table(schema: dict) -> list[str]:
    props = schema.get("properties", {})
    if not props:
        return ["_No properties._", ""]
    required = set(schema.get("required", []))
    lines = ["| Property | Type | Required | Description |",
             "| --- | --- | --- | --- |"]
    for name, entry in props.items():
        req = "Yes" if name in required else "No"
        desc = escape_cell(entry.get("description", ""))
        lines.append(f"| `{name}` | {render_type(entry)} | {req} | {desc} |")
    lines.append("")
    return lines


def render_def(name: str, schema: dict) -> list[str]:
    lines = [f"### {name}", ""]
    if schema.get("description"):
        lines += [schema["description"], ""]
    if "enum" in schema:
        base = schema.get("type", "string")
        lines += [f"Type: `{base}` — one of:", ""]
        lines += [f"- `{v}`" for v in schema["enum"]]
        lines += [""]
    else:
        lines += property_table(schema)
    return lines


def render_page(schema: dict) -> str:
    title = schema.get("title", file_to_type(schema.get("$id", "Type")))
    description = schema.get("description", "")
    # Front matter (description is the first line, summarized for the meta tag).
    summary = description.split("\n", 1)[0] if description else f"{title} reference."
    out = ["---", f"title: {title}", f"description: {escape_cell(summary)}", "---", ""]
    if description:
        out += [description, ""]
    out += ["## Properties", ""]
    out += property_table(schema)
    defs = schema.get("$defs")
    if defs:
        out += ["## Types", ""]
        for name, sub in defs.items():
            out += render_def(name, sub)
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("schemas", type=Path, help="Directory of *.schema.json files")
    parser.add_argument("out", type=Path, help="Output directory for .md pages")
    args = parser.parse_args()

    files = sorted(args.schemas.glob("*.schema.json"))
    if not files:
        print(f"no *.schema.json found in {args.schemas}", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    for f in files:
        schema = json.loads(f.read_text())
        page = render_page(schema)
        name = slug(file_to_type(f.name))
        (args.out / f"{name}.md").write_text(page)
        print(f"wrote {args.out / name}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
