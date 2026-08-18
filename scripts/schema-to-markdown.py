#!/usr/bin/env python3
"""Render JSON Schema files into grouped Starlight Markdown reference pages.

Consumes the `*.schema.json` produced by `symbolgraph-to-schema.py` (the
version-controlled source of truth, flat files under `public/schemas/`) and
groups them into pages driven by each schema's `x-group` / `x-merge` tags. This
script knows nothing about Swift — it is a pure JSON Schema -> Markdown step.

Usage:
    schema-to-markdown.py <schemas-dir> <out-dir> [options]

Two independent tags decide layout:

    x-group   A single section name. It only places the type in the sidebar /
              landing-page taxonomy. A type with no `x-group` is folded into its
              merge page (below) but not listed on the landing page.
    x-merge   Optional. Every type sharing an `x-merge` value is concatenated
              onto ONE page (named after that value) as a `##` section. A type
              with no `x-merge` gets its OWN standalone page named after the type.

Pages are written FLAT (one file per page, named after the merge value or the
type) so a page's URL never encodes its group — re-grouping never breaks a link.
Flat slugs share one namespace, so a collision is a hard error. A merge page's
section is taken from its members' `x-group`; schemas with no `x-group` and no
`x-merge` fall back to a `Shared` page so the build never breaks.

`--base-path` is the route prefix the pages live under; it must match where
`<out-dir>` maps to on the site so cross-page `$ref` links resolve.

`--schema-url-base` (optional) adds a "View JSON Schema" link per type. Point the
input `<schemas-dir>` at `public/schemas` so the same files are served on the
docs origin and that link (and `$schema` validation) resolves.

`--sidebar-out` (optional) writes a Starlight sidebar fragment (JSON array of the
group tree) for `astro.config.mjs` to import and spread into the Reference group.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Route prefix the generated pages are served under; set from --base-path.
BASE_PATH = "/reference"

# URL prefix the raw *.schema.json files are served from, or None to omit the
# "View JSON Schema" link. Set from --schema-url-base.
SCHEMA_URL_BASE: str | None = None

# Tag used for schemas that carry no `x-group`.
FALLBACK_GROUP = "Shared"

# type name -> (page route, is the page a single-type "standalone" page).
# Built in pass 1, consumed by render_ref to resolve cross-type links.
INDEX: dict[str, tuple[str, bool]] = {}

# Render context for the type currently being emitted (so in-page `#` and
# `#/$defs/...` refs resolve against the right section).
CURRENT_TYPE = ""
CURRENT_ROUTE = ""
CURRENT_STANDALONE = False


def slug(name: str) -> str:
    """Type/segment name -> kebab-case URL slug (EntityDefinition -> entity-definition,
    "Game Systems" -> game-systems). Used for file paths and routes (which we control
    on both ends), so CamelCase splitting is safe here."""
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", name)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s)
    return s.strip("-").lower()


def github_slug(text: str) -> str:
    """Mirror github-slugger, which is what Astro uses to generate heading ids.

    Critically: it does NOT split CamelCase and replaces each space 1:1 with a
    hyphen (no collapsing). We must match it exactly or in-page `#anchor` links
    silently point at nothing. `EntityDefinition` -> `entitydefinition`,
    `Map.Marker` -> `mapmarker`."""
    s = text.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)  # keep word chars, hyphen, space
    return s.replace(" ", "-")


def escape_cell(text: str) -> str:
    """Make a string safe for a single Markdown table cell."""
    return text.replace("|", "\\|").replace("\n\n", " ").replace("\n", " ").strip()


def flatten_description(text: str) -> str:
    """Flatten a multi-line schema description into one table-cell-safe line.

    Descriptions follow a convention of a summary paragraph, optional elaboration
    paragraphs, and trailing bullet lists (`- ...`) or notes. Markdown tables hold
    no block content, so this folds everything inline: paragraphs/lines join with
    spaces, and each run of consecutive bullets collapses to a single `; `-joined
    clause — semicolons (not the naive newline→space) keep items whose own text
    contains commas distinguishable. Returns a pipe-escaped single line."""
    chunks: list[str] = []
    bullets: list[str] = []

    def flush() -> None:
        if bullets:
            chunks.append("; ".join(bullets))
            bullets.clear()

    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            flush()
            continue
        heading = re.match(r"#{1,6}\s+(.*)", line)
        if heading:
            # `## Examples` etc. become an inline `Examples:` lead-in for the
            # content that follows, rather than a stray `##` in the cell.
            flush()
            chunks.append("<br>**" + heading.group(1).strip().rstrip(":") + ":**")
            continue
        m = re.match(r"[-*]\s+(.*)", line)
        if m:
            bullets.append(m.group(1).strip())
        else:
            flush()
            chunks.append(line)
    flush()

    one_line = " ".join(chunks)
    return one_line.replace("|", "\\|").strip()


def yaml_str(text: str) -> str:
    """Double-quote a string for a YAML front-matter value.

    Required because plain scalars may not start with reserved indicators such
    as backtick or `@`, which schema descriptions often do."""
    one_line = text.replace("\n\n", " ").replace("\n", " ").strip()
    escaped = one_line.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def file_to_type(filename: str) -> str:
    return filename.replace(".schema.json", "")


# --------------------------------------------------------------------------- #
# Tag parsing / page model
# --------------------------------------------------------------------------- #

@dataclass
class Page:
    key: str                       # unique page identity (dedupes merged types)
    route: str                     # /reference/schema/<slug>/ — link & anchor base
    slug: str                      # flat page slug = the output file name
    label: str                     # page title / sidebar label = the host type name
    groups: list[str] = field(default_factory=list)  # [section]; set in pass 2
    types: list[tuple[str, dict]] = field(default_factory=list)  # (name, schema)


def page_identity(schema: dict, type_name: str):
    """Resolve a schema's page identity. `x-merge: X` folds this type INTO type
    X's page (X is the host type; its mergers append as `##` sections); without
    `x-merge`, the type hosts its own page. So the page is keyed by the target
    type name either way, and a host + its mergers share one page. Pages are FLAT
    — the route never encodes the section, so re-grouping never changes a URL.
    Returns (page_key, route, page_slug, label)."""
    target = (schema.get("x-merge") or "").strip() or type_name
    page_slug = slug(target)
    key = "page:" + target
    route = BASE_PATH + "/" + page_slug + "/"
    return key, route, page_slug, target


def build_pages(files: list[Path]) -> list[Page]:
    """Pass 1: load every schema and assign it to its (host) page."""
    pages: dict[str, Page] = {}
    for f in sorted(files):
        schema = json.loads(f.read_text())
        type_name = schema.get("title") or file_to_type(f.name)
        key, route, page_slug, label = page_identity(schema, type_name)
        page = pages.get(key)
        if page is None:
            page = Page(key, route, page_slug, label)
            pages[key] = page
        page.types.append((type_name, schema))

    # Pass 2: sort members, resolve the section, and index types. The host type
    # (name == page label) is rendered headingless — its name is already the page
    # title — so it acts as the page's "standalone" type and links resolve to the
    # page root; any merged types get their own `##` section + anchor. The section
    # comes from the members' `x-group` (warn on conflict, Shared if none).
    for page in pages.values():
        # Host type (same name as the page) first, then mergers alphabetically.
        page.types.sort(key=lambda t: (t[0] != page.label, t[0]))
        member_groups = sorted({s["x-group"] for _, s in page.types if s.get("x-group")})
        if len(member_groups) > 1:
            print(f"warning: page '{page.label}' has members in multiple sections "
                  f"{member_groups}; using '{member_groups[0]}'", file=sys.stderr)
        page.groups = [member_groups[0] if member_groups else FALLBACK_GROUP]
        for type_name, _ in page.types:
            INDEX[type_name] = (page.route, type_name == page.label)

    # Flat slugs share one namespace, so they must be unique. Folders used to
    # disambiguate; now a collision would silently overwrite a page.
    by_slug: dict[str, list[str]] = {}
    for p in pages.values():
        by_slug.setdefault(p.slug, []).append(p.key)
    clashes = {s: keys for s, keys in by_slug.items() if len(keys) > 1}
    if clashes:
        for s, keys in clashes.items():
            print(f"error: page slug '{s}' is claimed by multiple pages: "
                  f"{', '.join(keys)}", file=sys.stderr)
        raise SystemExit(1)

    return sorted(pages.values(), key=lambda p: p.route)


# --------------------------------------------------------------------------- #
# Reference resolution
# --------------------------------------------------------------------------- #

def render_ref(ref: str) -> str:
    """Turn a $ref into a linked type label, resolved against INDEX + context."""
    if ref == "#":  # the current type itself
        if CURRENT_STANDALONE:
            return CURRENT_TYPE
        return f"[{CURRENT_TYPE}](#{github_slug(CURRENT_TYPE)})"

    if ref.startswith("#/$defs/"):  # in-page nested type
        nested = ref.rsplit("/", 1)[-1]
        a = github_slug(nested if CURRENT_STANDALONE else f"{CURRENT_TYPE}.{nested}")
        return f"[{nested}](#{a})"

    file_part, _, frag = ref.partition("#")
    type_name = file_to_type(file_part)
    target = INDEX.get(type_name)
    if target is None:  # untagged / dropped / external — no page to link to
        return type_name
    route, standalone = target
    same_page = route == CURRENT_ROUTE

    if frag.startswith("/$defs/"):
        nested = frag.rsplit("/", 1)[-1]
        a = github_slug(nested if standalone else f"{type_name}.{nested}")
        href = f"#{a}" if same_page else f"{route}#{a}"
        return f"[{nested}]({href})"

    if standalone:
        return type_name if same_page else f"[{type_name}]({route})"
    a = github_slug(type_name)
    href = f"#{a}" if same_page else f"{route}#{a}"
    return f"[{type_name}]({href})"


def render_type(entry: dict) -> str:
    """Human-readable type label for a property's schema fragment.

    Leaf type names render as inline-code "chips" for at-a-glance scanning; refs
    stay as plain links (a code span can't hold a link), and generics keep their
    `Array<…>` / `Object<…>` wrapper as text around the already-chipped element."""
    if "$ref" in entry:
        return render_ref(entry["$ref"])
    t = entry.get("type")
    if t == "array":
        return f"Array&lt;{render_type(entry.get('items', {}))}&gt;"
    if t == "object":
        ap = entry.get("additionalProperties")
        if ap not in (None, False):
            inner = render_type(ap) if isinstance(ap, dict) and ap else "Any"
            return f"Object&lt;{inner}&gt;" if inner != "Any" else "`Object`"
        return "`Object`"
    if "enum" in entry:
        return f"`{t or 'string'} (enum)`"
    if isinstance(t, list):  # JSON Schema type array = a union
        return "`" + " | ".join(t) + "`"
    if t:
        fmt = entry.get("format")
        return f"`{t} ({fmt})`" if fmt else f"`{t}`"
    return "`any`"


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

# Fields dropped from every type — opaque internal bookkeeping the docs ignore.
SKIP_FIELDS = {"meta", "metadata"}
# Fields always documented as a free-form JSON object, regardless of their
# declared schema (the app treats them as an arbitrary bag of values).
FREEFORM_FIELDS = {"attributes"}


def property_table(schema: dict) -> list[str]:
    props = {n: e for n, e in schema.get("properties", {}).items()
             if n not in SKIP_FIELDS}
    if not props:
        return ["_No properties._", ""]
    required = set(schema.get("required", []))
    lines = ["| Property | Type | Required | Description |",
             "| --- | --- | --- | --- |"]
    for name, entry in props.items():
        req = "Yes" if name in required else "No"
        desc = flatten_description(entry.get("description", ""))
        type_label = "`Object`" if name in FREEFORM_FIELDS else render_type(entry)
        lines.append(f"| `{name}` | {type_label} | {req} | {desc} |")
    lines.append("")
    return lines


def enum_block(schema: dict) -> list[str]:
    base = schema.get("type", "string")
    lines = [f"Type: `{base}` — one of:", ""]
    lines += [f"- `{v}`" for v in schema.get("enum", [])]
    return lines + [""]


def body_block(schema: dict) -> list[str]:
    return enum_block(schema) if "enum" in schema else property_table(schema)


def render_def(type_name: str, def_name: str, schema: dict,
               standalone: bool, level: str) -> list[str]:
    # Heading text doubles as the anchor source; qualify with the parent type on
    # concat pages so two types' nested `Style` defs don't collide.
    heading = def_name if standalone else f"{type_name}.{def_name}"
    lines = [f"{level} {heading}", ""]
    if schema.get("description"):
        lines += [schema["description"], ""]
    lines += body_block(schema)
    return lines


def render_type_section(type_name: str, schema: dict, is_title: bool) -> list[str]:
    """Render one top-level type. The host type (`is_title`) omits the `##` heading
    — the page title already names it — and hosts its defs at `##`; a merged type
    adds a `## {Type}` heading and hosts its defs at `###`."""
    global CURRENT_TYPE, CURRENT_STANDALONE
    CURRENT_TYPE = type_name
    CURRENT_STANDALONE = is_title

    lines: list[str] = []
    if not is_title:
        lines += [f"## {type_name}", ""]
    if schema.get("description"):
        lines += [schema["description"], ""]
    if SCHEMA_URL_BASE is not None:
        filename = schema.get("$id", f"{type_name}.schema.json")
        lines += [f"[View JSON Schema]({SCHEMA_URL_BASE}/{filename})", ""]
    lines += body_block(schema)

    def_level = "##" if is_title else "###"
    for dname, dschema in schema.get("$defs", {}).items():
        lines += render_def(type_name, dname, dschema, is_title, def_level)
    return lines


GENERATED_BANNER = ("<!-- AUTO-GENERATED by scripts/schema-to-markdown.py — do not edit. "
                    "Regenerate from public/schemas/. -->")


def render_page(page: Page) -> str:
    global CURRENT_ROUTE
    CURRENT_ROUTE = page.route
    summary = (page.types[0][1].get("description", "").split("\n", 1)[0]
               if len(page.types) == 1 else f"{page.label} reference.")
    out = ["---", f"title: {yaml_str(page.label)}",
           f"description: {yaml_str(summary or page.label)}",
           # Generated page: no "Edit page" link, hand-edits are overwritten.
           "editUrl: false", "---", "",
           GENERATED_BANNER, ""]
    for type_name, schema in page.types:
        out += render_type_section(type_name, schema, type_name == page.label)
    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------- #
# Sidebar fragment
# --------------------------------------------------------------------------- #

def build_sidebar(pages: list[Page]) -> list[dict]:
    """Nest pages under their group labels into a Starlight sidebar item tree."""
    root: dict = {"children": {}, "pages": []}
    for page in pages:
        node = root
        for label in page.groups:
            node = node["children"].setdefault(label, {"children": {}, "pages": []})
        node["pages"].append((page.label, page.route))

    def to_items(node: dict) -> list[dict]:
        items = []
        group_labels = set(node["children"])
        for label in sorted(node["children"]):
            items.append({"label": label, "items": to_items(node["children"][label])})
        for label, route in sorted(node["pages"]):
            if label in group_labels:
                print(f"warning: '{label}' is both a page and a group; "
                      f"the sidebar tree may be ambiguous", file=sys.stderr)
            items.append({"label": label, "link": route})
        return items

    return to_items(root)


def render_index(pages: list[Page]) -> str:
    """A single landing page listing every schema — the slim alternative to
    enumerating the whole type tree in the nav. The taxonomy is driven purely by
    `x-group` (the section); `x-merge` only affects page layout, so a merged type
    is listed under its own section and links into its host page. A type with no
    `x-group` (folded into a host page) is omitted."""
    sections: dict[str, list[tuple[str, dict]]] = {}
    for page in pages:
        for type_name, schema in page.types:
            group = schema.get("x-group")
            if not group:
                continue  # merge-only: rendered on its host page, not listed here
            sections.setdefault(group, []).append((type_name, schema))

    out = ["---", 'title: "Schema reference"',
           'description: "Reference for the JSON import/export and game-system '
           'configuration schemas."',
           # Generated page: no "Edit page" link, hand-edits are overwritten.
           "editUrl: false", "---", "", GENERATED_BANNER, "",
           "Reference for the JSON formats the app reads and writes, generated from "
           "its data model.", ""]

    for section in sorted(sections):
        out += [f"## {section}", "", "| Schema | Description |", "| --- | --- |"]
        for type_name, schema in sorted(sections[section], key=lambda r: r[0]):
            route, standalone = INDEX[type_name]
            detail = route if standalone else f"{route}#{github_slug(type_name)}"
            desc = escape_cell((schema.get("description") or "").split("\n", 1)[0])
            out.append(f"| [{type_name}]({detail}) | {desc} |")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


# --------------------------------------------------------------------------- #

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("schemas", type=Path, help="Directory of *.schema.json files")
    parser.add_argument("out", type=Path, help="Output directory for .md pages")
    parser.add_argument("--base-path", default="/reference",
                        help="Route prefix the pages are served under "
                             "(must match <out> on the site). Default: /reference")
    parser.add_argument("--schema-url-base",
                        help="URL prefix the raw *.schema.json files are served "
                             "from; adds a 'View JSON Schema' link per type")
    parser.add_argument("--sidebar-out", type=Path,
                        help="Write a Starlight sidebar fragment (JSON) here")
    parser.add_argument("--sidebar-root", default="JSON Schema",
                        help="In tree mode, wrap the groups under this root label; "
                             "in index mode, the label of the single index link "
                             "(empty string = no root). Default: Schema")
    parser.add_argument("--sidebar-mode", choices=("index", "tree"), default="index",
                        help="index: one 'Schema' link to a generated landing page "
                             "that lists every schema (slim nav, recommended). "
                             "tree: enumerate every group/page in the sidebar. "
                             "Default: index")
    args = parser.parse_args()

    global BASE_PATH, SCHEMA_URL_BASE
    BASE_PATH = args.base_path.rstrip("/")
    SCHEMA_URL_BASE = args.schema_url_base.rstrip("/") if args.schema_url_base else None

    files = list(args.schemas.glob("*.schema.json"))
    if not files:
        print(f"no *.schema.json found in {args.schemas}", file=sys.stderr)
        return 1

    pages = build_pages(files)

    if any(p.slug == "index" for p in pages):
        print("error: a schema page has slug 'index', colliding with the landing "
              "page", file=sys.stderr)
        raise SystemExit(1)

    args.out.mkdir(parents=True, exist_ok=True)
    for page in pages:
        dest = args.out / f"{page.slug}.md"
        dest.write_text(render_page(page))
        print(f"wrote {dest}  ({len(page.types)} type(s))")

    index_route = BASE_PATH + "/"
    (args.out / "index.md").write_text(render_index(pages))
    print(f"wrote {args.out / 'index.md'}  (landing page)")

    if args.sidebar_out:
        if args.sidebar_mode == "index":
            label = args.sidebar_root or "Schema"
            sidebar = [{"label": label, "link": index_route}]
        else:
            sidebar = build_sidebar(pages)
            if args.sidebar_root:
                sidebar = [{"label": args.sidebar_root, "items": sidebar}]
        args.sidebar_out.parent.mkdir(parents=True, exist_ok=True)
        args.sidebar_out.write_text(json.dumps(sidebar, indent=2) + "\n")
        print(f"wrote {args.sidebar_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
