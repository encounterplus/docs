#!/usr/bin/env python3
"""Convert Swift symbol-graph JSON into JSON Schema (draft 2020-12).

The Encounter+ app's import/export and configuration formats are defined as
Swift `Codable` structs. Building the app with the compiler's symbol-graph
export (`-emit-symbol-graph`) produces `*.symbols.json` describing every symbol,
its doc comments, and its relationships. This script transforms that into one
JSON Schema file per top-level Codable type, which becomes the version-controlled
source of truth for the generated reference documentation.

Emit the input from the app project with, e.g.:

    swiftc ... -emit-symbol-graph -emit-symbol-graph-dir <dir> \\
        -symbol-graph-minimum-access-level internal \\
        -symbol-graph-pretty-print -symbol-graph-skip-synthesized-members

`-symbol-graph-minimum-access-level internal` is required: the Codable structs
are `internal`, and without it they are omitted from the graph.

Tag a type for the docs by adding a `- SchemaGroup:` line to its doc comment:

    /// A battle map and everything placed on it.
    ///
    /// - SchemaGroup: Content
    struct Map: Codable { ... }

The value is a single section name (written to the schema as `x-group` and
stripped from the description). It only decides which section/sidebar group the
type is listed under — it no longer carries layout meaning (no trailing slash, no
nested `A/B` paths; a slash-bearing value is collapsed to its first segment).

Concatenate several types onto one shared page with a `- SchemaMerge:` line:

    /// - SchemaMerge: Map
    struct Marker: Codable { ... }

Every type sharing a `SchemaMerge` value renders as a `##` section of one page
named after that value (written as `x-merge`, stripped from the description).

Only tagged types — those with `SchemaGroup` or `SchemaMerge`, plus everything
they transitively `$ref` — are emitted; untagged, unreferenced Codable types are
dropped. If no type is tagged, all Codable types are emitted (unfiltered),
preserving the pre-tag behavior.

Add a `- SchemaAllOptional: true` line to mark a type whose every field is optional
— for types with hand-written Codable conformance that decodes via `decodeIfPresent`,
where a property being non-optional in Swift no longer implies its key is required.
The type's `required` array is then omitted. (Whether a property is `?` is invisibly
decoupled from key presence here, so this can't be inferred from the symbol graph.)

Types with a `ViewModel` path component (e.g. `Foo.ViewModel`) are skipped — they
are app-internal and not part of the exported format (see SKIP_PATH_COMPONENTS).

Usage:
    symbolgraph-to-schema.py <symbols-dir-or-file> <out-dir> [--draft 2020-12]
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# Path components that exclude a type from emission entirely (matched per
# component, so `Foo.ViewModel` is skipped but `FooViewModelThing` is not).
SKIP_PATH_COMPONENTS = {"ViewModel"}

# Stable stdlib USRs for the conformances that mark a Codable type.
USR_DECODABLE = "s:Se"
USR_ENCODABLE = "s:SE"
USR_RAW_REPRESENTABLE = "s:SY"

# Swift type name -> JSON Schema fragment (for non-custom, non-collection types).
SCALAR_TYPES: dict[str, dict] = {
    "String": {"type": "string"},
    "Bool": {"type": "boolean"},
    "Int": {"type": "integer"},
    "Int8": {"type": "integer"}, "Int16": {"type": "integer"},
    "Int32": {"type": "integer"}, "Int64": {"type": "integer"},
    "UInt": {"type": "integer"}, "UInt8": {"type": "integer"},
    "UInt16": {"type": "integer"}, "UInt32": {"type": "integer"},
    "UInt64": {"type": "integer"},
    "Double": {"type": "number"}, "Float": {"type": "number"},
    "CGFloat": {"type": "number"},
    "URL": {"type": "string", "format": "uri"},
    "Date": {"type": "string", "format": "date-time"},
    "UUID": {"type": "string", "format": "uuid"},
    "Data": {"type": "string", "contentEncoding": "base64"},
    # RealmSwift free-form primitive: a string, number, or boolean.
    "AnyRealmValue": {"type": ["string", "number", "boolean"]},
}

# App free-form JSON container types: mapped directly to their JSON Schema shape and
# NOT emitted as their own schema files (their internal `value` storage is opaque).
_FREEFORM_OBJECT = {"type": "object", "additionalProperties": True}
JSON_CONTAINERS: dict[str, dict] = {
    "JSONObject": _FREEFORM_OBJECT,
    "JSONData": _FREEFORM_OBJECT,                         # freeform JSON object: {}
    "JSONValue": {},                                     # any JSON value
    "AnyCodable": {},
    "JSONArrayData": {"type": "array", "items": _FREEFORM_OBJECT},
    "JSONObjectArray": {"type": "array", "items": _FREEFORM_OBJECT},  # array of freeform objects
}


def warn(msg: str) -> None:
    print(f"warning: {msg}", file=sys.stderr)


# A `- SchemaGroup: <section>` doc-comment line tags a type for the docs taxonomy.
# It drives filtering (only tagged types and what they reach are emitted) and
# placement (the value becomes the schema's `x-group` — a single section name).
# See README/CLAUDE.md.
SCHEMA_GROUP_RE = re.compile(r"^\s*-\s*SchemaGroup\s*:\s*(.+?)\s*$", re.IGNORECASE)

# A `- SchemaMerge: <page>` doc-comment line concatenates every type sharing the
# value onto one page (written as `x-merge`). Also counts as a tag for filtering.
SCHEMA_MERGE_RE = re.compile(r"^\s*-\s*SchemaMerge\s*:\s*(.+?)\s*$", re.IGNORECASE)

# A `- SchemaAllOptional: true` doc-comment line marks a type whose every field is
# optional. Use it for types with hand-written Codable conformance that decodes
# with `decodeIfPresent` (whether a property is `?` in Swift then says nothing
# about whether the key must be present), which the symbol graph can't see.
SCHEMA_ALL_OPTIONAL_RE = re.compile(r"^\s*-\s*SchemaAllOptional\s*:\s*(.*?)\s*$", re.IGNORECASE)

# Every recognized schema tag; stripped from descriptions so it never renders.
SCHEMA_TAG_RES = (SCHEMA_GROUP_RE, SCHEMA_MERGE_RE, SCHEMA_ALL_OPTIONAL_RE)

# Group assigned to a type that is reached from a tagged root but isn't tagged
# itself, so every emitted schema is self-describing and lands on a page.
DEFAULT_GROUP = "Shared"


# Dotted property paths (e.g. "ViewDefinition.id") to force-exclude / force-include,
# populated from --exclude / --include. Resolves the ambiguous `{ get set }` cases.
FORCE_EXCLUDE: set[str] = set()
FORCE_INCLUDE: set[str] = set()


# --- doc comments --------------------------------------------------------

def doc_text(symbol: dict) -> str | None:
    """Join a symbol's doc-comment lines into a description string.

    Preserves paragraph breaks (blank lines) and normalizes DocC double-backtick
    symbol links (``Foo``) to single-backtick code spans for Markdown rendering.
    """
    dc = symbol.get("docComment")
    if not dc:
        return None
    # Drop schema tag line(s) (`- SchemaGroup:`, `- SchemaMerge:`,
    # `- SchemaAllOptional:`) — that metadata drives generation, it is not part of
    # the human-readable description.
    lines = [l["text"] for l in dc["lines"]
             if not any(r.match(l["text"]) for r in SCHEMA_TAG_RES)]
    text = "\n".join(lines).strip()
    if not text:
        return None
    return _docc_links_to_code(text)


def _docc_links_to_code(text: str) -> str:
    """Normalize DocC double-backtick symbol links (``Foo`` -> `Foo`) for Markdown,
    without disturbing fenced code blocks. The match is confined to a single line
    (no newline in the span) and skipped entirely inside ```-fenced blocks, so a
    ```json … ``` example is never collapsed to two backticks."""
    out: list[str] = []
    in_fence = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence:
            line = re.sub(r"``([^`\n]+)``", r"`\1`", line)
        out.append(line)
    return "\n".join(out)


def extract_group(symbol: dict) -> str | None:
    """The `- SchemaGroup:` value from a symbol's doc comment, or None.

    The value is a single section name. Slashes carry no meaning anymore, so a
    slash-bearing value is collapsed to its first segment (with a warning)."""
    dc = symbol.get("docComment")
    if not dc:
        return None
    for line in dc["lines"]:
        m = SCHEMA_GROUP_RE.match(line["text"])
        if m:
            value = m.group(1).strip()
            if "/" in value:
                first = value.strip("/").split("/", 1)[0]
                warn(f"SchemaGroup {value!r} contains '/': sections are single "
                     f"segments now; using {first!r}")
                return first
            return value
    return None


def extract_merge(symbol: dict) -> str | None:
    """The `- SchemaMerge:` value from a symbol's doc comment, or None."""
    dc = symbol.get("docComment")
    if not dc:
        return None
    for line in dc["lines"]:
        m = SCHEMA_MERGE_RE.match(line["text"])
        if m:
            return m.group(1).strip()
    return None


def extract_all_optional(symbol: dict) -> bool:
    """Whether the type is tagged `- SchemaAllOptional:` with a truthy value. A bare
    or `true`/`yes`/`1` value enables it; `false`/`no`/`0` disables it (as does the
    tag's absence)."""
    dc = symbol.get("docComment")
    if not dc:
        return False
    for line in dc["lines"]:
        m = SCHEMA_ALL_OPTIONAL_RE.match(line["text"])
        if m:
            return m.group(1).strip().lower() not in ("false", "no", "0")
    return False


def with_field(schema: dict, key: str, value: str) -> dict:
    """Return schema with `key` inserted right after its title/description for
    readable diffs (existing occurrences of `key` are dropped and re-placed)."""
    out: dict = {}
    placed = False
    for k, v in schema.items():
        if k == key:
            continue
        out[k] = v
        if not placed and k in ("title", "description"):
            out[key] = value
            placed = True
    if not placed:
        out[key] = value
    return out


def ref_filenames(node) -> set[str]:
    """All cross-file `$ref` targets (the `<Type>.schema.json` part) within a schema."""
    out: set[str] = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                fp = v.split("#", 1)[0]
                if fp.endswith(".schema.json"):
                    out.add(fp)
            else:
                out |= ref_filenames(v)
    elif isinstance(node, list):
        for x in node:
            out |= ref_filenames(x)
    return out


def filter_to_tagged(files: dict[str, dict]) -> None:
    """Keep only tagged roots and everything they transitively `$ref`; drop the rest.

    A schema is a tagged root if it carries `x-group` or `x-merge`. Reached-but-
    fully-untagged schemas (neither tag) are stamped with the default group so
    every emitted file lands on a page. A schema with only `x-merge` keeps its
    group unset — it is folded into its merge page and not listed separately. If
    nothing is tagged (e.g. the app source has no tags yet), leave all files
    untouched."""
    def is_tagged(s: dict) -> bool:
        return "x-group" in s or "x-merge" in s

    tagged = {fn for fn, s in files.items() if is_tagged(files[fn])}
    if not tagged:
        warn("no `- SchemaGroup:`/`- SchemaMerge:` tags found; emitting all "
             "Codable types unfiltered")
        return

    keep = set(tagged)
    stack = list(tagged)
    while stack:
        for ref in ref_filenames(files[stack.pop()]):
            if ref in files and ref not in keep:
                keep.add(ref)
                stack.append(ref)

    dropped = sorted(set(files) - keep)
    for fn in dropped:
        del files[fn]
    untagged_kept = sorted(fn for fn in keep if not is_tagged(files[fn]))
    for fn in untagged_kept:
        files[fn] = with_field(files[fn], "x-group", DEFAULT_GROUP)
    if untagged_kept:
        warn(f"reached but untagged, assigned to {DEFAULT_GROUP!r}: "
             f"{', '.join(file_part[:-12] for file_part in untagged_kept)}")
    if dropped:
        print(f"dropped {len(dropped)} untagged, unreferenced type(s)", file=sys.stderr)


# --- stored vs computed --------------------------------------------------

def fragment_keywords(symbol: dict) -> set[str]:
    return {
        f["spelling"]
        for f in symbol.get("declarationFragments", [])
        if f["kind"] == "keyword"
    }


_SOURCE_CACHE: dict[str, list[str] | None] = {}


def _source_path(loc: dict) -> str | None:
    uri = loc.get("uri", "") if loc else ""
    if not uri:
        return None
    return unquote(uri[7:]) if uri.startswith("file://") else uri


def _read_source(path: str | None) -> list[str] | None:
    """Source file lines (with newlines), cached. None if unreadable."""
    if path is None:
        return None
    if path not in _SOURCE_CACHE:
        try:
            with open(path, encoding="utf-8") as f:
                _SOURCE_CACHE[path] = f.readlines()
        except OSError:
            _SOURCE_CACHE[path] = None
    return _SOURCE_CACHE[path]


def coding_key_name(case_sym: dict) -> str:
    """The JSON key for a CodingKeys case: its raw-value rename if present, else the
    case name. Raw values are absent from the symbol graph, so read them from source
    via the case's recorded location (the script runs where the source lives)."""
    name = case_sym["pathComponents"][-1]
    loc = case_sym.get("location")
    lines = _read_source(_source_path(loc)) if loc else None
    if lines is None:
        return name
    try:
        line = lines[loc["position"]["line"]]  # symbol-graph positions are 0-based
    except (IndexError, KeyError):
        return name
    m = re.search(r"\b" + re.escape(name) + r"""\s*=\s*["']([^"']+)["']""", line)
    return m.group(1) if m else name


def _blank_swift_noise(s: str) -> str:
    """Blank out comments and string literals (preserving length) so brace matching
    isn't fooled by braces inside them."""
    s = re.sub(r"//[^\n]*", lambda m: " " * len(m.group()), s)
    s = re.sub(r"/\*.*?\*/", lambda m: " " * len(m.group()), s, flags=re.S)
    s = re.sub(r'"(?:\\.|[^"\\])*"', lambda m: " " * len(m.group()), s)
    return s


def _match_brace(s: str, i: int) -> tuple[int, int] | None:
    """Given s[i] == '{', return (content_start, close_index) of the matching block."""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return (i + 1, j)
    return None


def _parse_coding_cases(enum_src: str) -> list[tuple[str, str]]:
    """(case_name, json_key) pairs from a CodingKeys enum body."""
    out: list[tuple[str, str]] = []
    for m in re.finditer(r"\bcase\b([^\n]*)", enum_src):
        for part in m.group(1).split(","):
            part = part.strip().rstrip(";")
            cm = re.match(r"([A-Za-z_]\w*)\s*(?:=\s*[\"']([^\"']+)[\"'])?", part)
            if cm:
                out.append((cm.group(1), cm.group(2) or cm.group(1)))
    return out


def source_coding_keys(type_sym: dict) -> list[tuple[str, str]] | None:
    """Parse a type's `CodingKeys` enum from its source file. Handles a CodingKeys
    nested directly in the type declaration (covers private ones invisible to the
    symbol graph). Returns None if not found."""
    loc = type_sym.get("location")
    lines = _read_source(_source_path(loc)) if loc else None
    if lines is None:
        return None
    orig = "".join(lines[loc["position"]["line"]:])
    blank = _blank_swift_noise(orig)
    open_i = blank.find("{")
    if open_i < 0:
        return None
    body = _match_brace(blank, open_i)
    if body is None:
        return None
    bs, be = body
    m = re.search(r"enum\s+CodingKeys\b[^{]*\{", blank[bs:be])
    if not m:
        return None
    enum_block = _match_brace(blank, bs + m.end() - 1)
    if enum_block is None:
        return None
    es, ee = enum_block
    return _parse_coding_cases(orig[es:ee]) or None


def classify_property(symbol: dict) -> tuple[bool, bool]:
    """Return (is_stored, is_ambiguous).

    Codable encodes only stored properties. The symbol graph has no explicit
    flag, so we infer from the accessor block in declarationFragments:
      - no accessor block            -> stored
      - `{ get }` (read-only)        -> computed (a stored prop is never read-only)
      - `{ get set }`                -> ambiguous: stored-with-didSet vs computed
                                        read-write. Default to stored, but warn.
    """
    kws = fragment_keywords(symbol)
    has_get = "get" in kws
    has_set = "set" in kws
    if has_get and not has_set:
        return (False, False)
    if has_get and has_set:
        return (True, True)
    return (True, False)


# --- type parsing --------------------------------------------------------

def type_fragments(symbol: dict) -> list[dict]:
    """Fragments describing the property's type (after the name, before any
    accessor block)."""
    frags = symbol.get("declarationFragments", [])
    # Locate the property name (first identifier fragment).
    start = None
    for i, f in enumerate(frags):
        if f["kind"] == "identifier":
            start = i + 1
            break
    if start is None:
        return []
    out = []
    for f in frags[start:]:
        if f["kind"] == "text" and "{" in f["spelling"]:
            # The accessor block begins here, but the compiler fuses the brace
            # with the preceding type token (e.g. a property-wrapped optional is
            # spelled `String` + `"? { "`). Keep the part before the `{` so the
            # trailing `?` survives, then stop.
            before = f["spelling"].split("{", 1)[0]
            if before.strip():
                out.append({**f, "spelling": before})
            break
        out.append(f)
    # Strip the leading ": " separator. The compiler may fuse it with the next
    # token (e.g. ": [" for an array), so trim it off the first fragment rather
    # than dropping whole fragments.
    if out and out[0]["kind"] == "text":
        stripped = re.sub(r"^\s*:\s*", "", out[0]["spelling"])
        if stripped:
            out[0] = {**out[0], "spelling": stripped}
        else:
            out.pop(0)
    return out


def reconstruct(frags: list[dict]) -> str:
    return "".join(f["spelling"] for f in frags).strip()


def split_optional(frags: list[dict]) -> tuple[list[dict], bool]:
    """Strip a single trailing top-level `?` (Optional)."""
    trimmed = list(frags)
    while trimmed and trimmed[-1]["kind"] == "text" and trimmed[-1]["spelling"].strip() == "":
        trimmed.pop()
    if trimmed and trimmed[-1]["kind"] == "text" and trimmed[-1]["spelling"].rstrip().endswith("?"):
        last = dict(trimmed[-1])
        last["spelling"] = last["spelling"].rstrip()[:-1]
        trimmed[-1] = last
        if not last["spelling"]:
            trimmed.pop()
        return trimmed, True
    return trimmed, False


def typealias_underlying(sym: dict) -> list[dict] | None:
    """Fragments of a typealias's underlying type (everything after `=`).

    The compiler fuses the `=` with the following token (e.g. ` = [`), so split
    that fragment and keep the trailing part rather than dropping it.
    """
    frags = sym.get("declarationFragments", [])
    for i, f in enumerate(frags):
        if f["kind"] == "text" and "=" in f["spelling"]:
            after = f["spelling"].split("=", 1)[1]
            rest = frags[i + 1:]
            return [{"kind": "text", "spelling": after}] + rest if after.strip() else rest
    return None


def map_named_type(name: str, usr: str, graph: "SymbolGraph", resolver) -> dict:
    if usr:
        ref = resolver(usr)
        if ref is not None:
            return ref
    # Known scalars and free-form JSON containers (matched by name) take precedence
    # over alias expansion, so e.g. JSONObject/JSONData stay free-form.
    if name in JSON_CONTAINERS:
        return copy.deepcopy(JSON_CONTAINERS[name])
    if name in SCALAR_TYPES:
        return dict(SCALAR_TYPES[name])
    if name in ("Any", "AnyObject", "AnyHashable"):
        return {}
    # Expand any other typealias to its underlying type.
    if usr:
        sym = graph.symbols.get(usr)
        if sym and sym["kind"]["identifier"] == "swift.typealias":
            under = typealias_underlying(sym)
            if under:
                return map_type(under, graph, resolver)
    # Unresolved generic parameter (e.g. T, Element) -> permit anything.
    if re.fullmatch(r"[A-Z][A-Za-z0-9]?", name) or name in ("Element", "Key", "Value", "Wrapped"):
        return {}
    warn(f"unrecognized type {name!r} (usr={usr or '-'}); emitting permissive schema")
    return {"$comment": f"unmapped Swift type: {name}"}


# Generic container kinds. RealmSwift collections are matched by USR (NOT name) because
# the app has its own `Map`/`List` model types whose names would otherwise collide.
_REALM_COLLECTION_USRS = {
    "s:10RealmSwift4ListC": "array",       # List<Element>  -> array
    "s:10RealmSwift3MapC": "dict",         # Map<Key,Value> -> object (dictionary)
    "s:10RealmSwift10MutableSetC": "set",  # MutableSet<Element> -> array (unique)
}
_STDLIB_COLLECTION_NAMES = {
    "Array": "array", "ContiguousArray": "array",
    "Set": "set", "Dictionary": "dict", "Optional": "optional",
}


def _collection_kind(name: str, usr: str) -> str | None:
    """array / set / dict / optional for a generic container base type, else None."""
    if usr in _REALM_COLLECTION_USRS:
        return _REALM_COLLECTION_USRS[usr]
    return _STDLIB_COLLECTION_NAMES.get(name)


def _tid_schema(tid: dict | None, graph: "SymbolGraph", resolver) -> dict:
    if tid is None:
        return {}
    return map_named_type(tid["spelling"], tid.get("preciseIdentifier", ""), graph, resolver)


def map_type(frags: list[dict], graph: "SymbolGraph", resolver) -> dict:
    """Map a list of type fragments to a JSON Schema fragment."""
    frags, _optional = split_optional(frags)
    text = reconstruct(frags)
    type_ids = [f for f in frags if f["kind"] == "typeIdentifier"]

    # [T] (array) or [Key: Value] (dictionary) sugar.
    if text.startswith("[") and text.endswith("]"):
        is_dict = any(f["kind"] == "text" and ":" in f["spelling"] for f in frags)
        if is_dict:
            return {"type": "object", "additionalProperties": _tid_schema(type_ids[-1] if type_ids else None, graph, resolver)}
        return {"type": "array", "items": _tid_schema(type_ids[0] if type_ids else None, graph, resolver)}

    # Generic containers: Array<T>, Set<T>, Dictionary<K,V>, Optional<T>, and the
    # RealmSwift List<T> (array) / Map<K,V> (object) / MutableSet<T> (matched by USR).
    # The base may be module-qualified (`RealmSwift.List<Tile>`), so split the type
    # identifiers at the first `<`: the base is the last identifier before it (which
    # skips a module qualifier that itself surfaces as an identifier), and the
    # generic arguments are the identifiers after it.
    if "<" in text and text.endswith(">") and type_ids:
        before, after, seen_lt = [], [], False
        for f in frags:
            if f["kind"] == "text" and "<" in f["spelling"]:
                seen_lt = True
            elif f["kind"] == "typeIdentifier":
                (after if seen_lt else before).append(f)
        base = before[-1] if before else type_ids[0]
        arg_ids = after if before else type_ids[1:]
        kind = _collection_kind(base["spelling"], base.get("preciseIdentifier", ""))
        if kind:
            inner = arg_ids  # generic argument type identifiers
            if kind == "array":
                return {"type": "array", "items": _tid_schema(inner[0] if inner else None, graph, resolver)}
            if kind == "set":
                return {"type": "array", "uniqueItems": True, "items": _tid_schema(inner[0] if inner else None, graph, resolver)}
            if kind == "optional":
                return _tid_schema(inner[0] if inner else None, graph, resolver)
            if kind == "dict":
                return {"type": "object", "additionalProperties": _tid_schema(inner[-1] if inner else None, graph, resolver)}
        # Other custom generic (e.g. Wrapper<T>): resolve the base type.
        return _tid_schema(base, graph, resolver)

    # Plain or qualified (Parent.Nested) named type: the last identifier is the type.
    if type_ids:
        return _tid_schema(type_ids[-1], graph, resolver)

    if text in ("Any", "AnyObject"):
        return {}
    warn(f"could not parse type {text!r}; emitting permissive schema")
    return {"$comment": f"unparsed Swift type: {text}"}


# --- model ---------------------------------------------------------------

class SymbolGraph:
    def __init__(self, paths: list[Path]):
        self.symbols: dict[str, dict] = {}
        self.conforms: dict[str, set[str]] = {}
        for p in paths:
            data = json.loads(p.read_text())
            for s in data.get("symbols", []):
                self.symbols[s["identifier"]["precise"]] = s
            for r in data.get("relationships", []):
                if r["kind"] == "conformsTo":
                    self.conforms.setdefault(r["source"], set()).add(r["target"])
        self.path_to_usr: dict[tuple, str] = {}
        for usr, s in self.symbols.items():
            self.path_to_usr[tuple(s["pathComponents"])] = usr

    def is_codable(self, usr: str) -> bool:
        c = self.conforms.get(usr, set())
        return USR_DECODABLE in c or USR_ENCODABLE in c

    def selected_types(self) -> dict[str, dict]:
        """USR -> symbol, for structs/enums/classes that are Codable."""
        out = {}
        for usr, s in self.symbols.items():
            path = s["pathComponents"]
            simple = path[-1]
            if simple in JSON_CONTAINERS or simple == "CodingKeys":
                continue  # opaque container / coding-keys helper: not emitted
            if usr in _REALM_COLLECTION_USRS:
                continue  # RealmSwift List/Map/MutableSet: rendered as inline array/
                # object containers (see _collection_kind), never their own schema file.
                # Their names would otherwise collide with app model types (e.g. Map).
            if SKIP_PATH_COMPONENTS.intersection(path):
                continue  # e.g. a `.ViewModel` type: app-internal, not exported
            if s["kind"]["identifier"] in ("swift.struct", "swift.enum", "swift.class") and self.is_codable(usr):
                out[usr] = s
        return out

    def members(self, type_path: list[str]) -> list[dict]:
        """Property symbols whose parent path equals type_path."""
        tp = tuple(type_path)
        out = []
        for s in self.symbols.values():
            if s["kind"]["identifier"] != "swift.property":
                continue
            if tuple(s["pathComponents"][:-1]) == tp:
                out.append(s)
        return out

    def enum_cases(self, type_path: list[str]) -> list[dict]:
        tp = tuple(type_path)
        out = []
        for s in self.symbols.values():
            if s["kind"]["identifier"] != "swift.enum.case":
                continue
            if tuple(s["pathComponents"][:-1]) == tp:
                out.append(s)
        return out

    def coding_keys_cases(self, type_path: list[str]) -> list[dict] | None:
        """Case symbols of a type's explicit `CodingKeys` enum (source order), or
        None if it has none (then all stored properties are encoded)."""
        ck_path = list(type_path) + ["CodingKeys"]
        has = any(s["kind"]["identifier"] == "swift.enum" and s["pathComponents"] == ck_path
                  for s in self.symbols.values())
        if not has:
            return None
        cases = self.enum_cases(ck_path)
        cases.sort(key=lambda c: (c.get("location", {}).get("position", {}).get("line", 0),
                                  c.get("location", {}).get("position", {}).get("character", 0)))
        return cases


def build(graph: SymbolGraph, draft: str) -> dict[str, dict]:
    """Return {filename: schema} for each top-level Codable type.

    A Codable type becomes its own schema file unless it is nested inside another
    Codable type, in which case it is emitted under that ancestor's `$defs`. Types
    nested in a non-Codable container (e.g. an @objc class) are promoted to their
    own files.
    """
    selected = graph.selected_types()
    selected_by_path = {tuple(s["pathComponents"]): usr for usr, s in selected.items()}

    def simple_name(usr: str) -> str:
        return selected[usr]["pathComponents"][-1]

    def codable_owner(usr: str) -> str | None:
        """Nearest strict ancestor that is itself a selected Codable type."""
        path = selected[usr]["pathComponents"]
        for i in range(len(path) - 1, 0, -1):
            anc = selected_by_path.get(tuple(path[:i]))
            if anc is not None:
                return anc
        return None

    def root_of(usr: str) -> str:
        owner = codable_owner(usr)
        while owner is not None:
            usr = owner
            owner = codable_owner(usr)
        return usr

    roots: dict[str, list[str]] = {}
    for usr in selected:
        roots.setdefault(root_of(usr), []).append(usr)

    def filename(root_usr: str) -> str:
        return f"{simple_name(root_usr)}.schema.json"

    def make_resolver(current_root: str):
        def resolve(usr: str) -> dict | None:
            if usr not in selected:
                return None
            r = root_of(usr)
            if r == current_root:
                return {"$ref": "#"} if usr == r else {"$ref": f"#/$defs/{simple_name(usr)}"}
            fn = filename(r)
            return {"$ref": fn} if usr == r else {"$ref": f"{fn}#/$defs/{simple_name(usr)}"}
        return resolve

    def schema_for(usr: str, resolver) -> dict:
        s = selected[usr]
        if s["kind"]["identifier"] == "swift.enum":
            return enum_schema(s, graph)
        return object_schema(s, graph, resolver)

    files: dict[str, dict] = {}
    for root_usr, members in roots.items():
        resolver = make_resolver(root_usr)
        schema = {
            "$schema": f"https://json-schema.org/draft/{draft}/schema",
            "$id": filename(root_usr),
            **schema_for(root_usr, resolver),
        }
        group = extract_group(selected[root_usr])
        if group:
            schema = with_field(schema, "x-group", group)
        merge = extract_merge(selected[root_usr])
        if merge:
            schema = with_field(schema, "x-merge", merge)
        defs: dict[str, dict] = {}
        for usr in members:
            if usr == root_usr:
                continue
            key = simple_name(usr)
            if key in defs:  # two nested types share a simple name
                key = "_".join(selected[usr]["pathComponents"])
            defs[key] = schema_for(usr, resolver)
        if defs:
            schema["$defs"] = defs
        fn = filename(root_usr)
        if fn in files:
            warn(f"duplicate schema filename {fn}; overwriting")
        files[fn] = schema
    filter_to_tagged(files)
    return files


def _property_entry(prop: dict, graph: SymbolGraph, resolver) -> tuple[dict, bool]:
    """Schema fragment and optionality for a stored-property symbol."""
    frags = type_fragments(prop)
    _, optional = split_optional(frags)
    entry = map_type(frags, graph, resolver)
    pdesc = doc_text(prop)
    if pdesc:
        entry["description"] = pdesc
    return entry, optional


def coding_keys_for(type_sym: dict, graph: SymbolGraph) -> list[tuple[str, str]] | None:
    """Unified (case_name, json_key) list for a type's CodingKeys, or None if it has
    none. Prefers the symbol graph (internal/public CodingKeys), then falls back to
    parsing source (private CodingKeys, invisible to the graph)."""
    cases = graph.coding_keys_cases(type_sym["pathComponents"])
    if cases is not None:
        return [(c["pathComponents"][-1], coding_key_name(c)) for c in cases]
    src = source_coding_keys(type_sym)
    if src is not None:
        warn(f"{'.'.join(type_sym['pathComponents'])}: CodingKeys read from source "
             f"(not in symbol graph, likely private) — verify keys")
    return src


def object_schema(s: dict, graph: SymbolGraph, resolver) -> dict:
    type_path = s["pathComponents"]
    schema: dict = {"title": type_path[-1], "type": "object"}
    desc = doc_text(s)
    if desc:
        schema["description"] = desc

    properties: dict[str, dict] = {}
    required: list[str] = []
    members = {p["names"]["title"]: p for p in graph.members(type_path)}
    coding_keys = coding_keys_for(s, graph)

    if coding_keys is not None:
        # Explicit CodingKeys: exported attributes are exactly these cases (renames
        # honored), regardless of which other stored properties exist.
        for case_name, key in coding_keys:
            dotted = ".".join(type_path) + "." + case_name
            if dotted in FORCE_EXCLUDE:
                continue
            prop = members.get(case_name)
            if prop is None:
                warn(f"{dotted}: CodingKeys case has no matching stored property; "
                     f"emitting permissive schema")
                properties[key] = {}
                required.append(key)
                continue
            entry, optional = _property_entry(prop, graph, resolver)
            properties[key] = entry
            if not optional:
                required.append(key)
    else:
        # No CodingKeys: every stored property is encoded.
        for prop in graph.members(type_path):
            dotted = ".".join(prop["pathComponents"])
            if dotted in FORCE_EXCLUDE:
                continue
            forced_in = dotted in FORCE_INCLUDE
            stored, ambiguous = classify_property(prop)
            if not stored and not forced_in:
                continue
            if ambiguous and not forced_in:
                warn(f"{dotted}: `{{ get set }}` is ambiguous (stored-with-didSet vs "
                     f"read-write computed); included as stored "
                     f"(use --exclude {dotted} to drop it)")
            entry, optional = _property_entry(prop, graph, resolver)
            properties[prop["names"]["title"]] = entry
            if not optional:
                required.append(prop["names"]["title"])

    schema["properties"] = properties
    # A `- SchemaAllOptional:` type has hand-written coding that may omit any key,
    # so per-property optionality is meaningless — drop `required` entirely.
    if required and not extract_all_optional(s):
        schema["required"] = required
    schema["additionalProperties"] = False
    return schema


def enum_schema(s: dict, graph: SymbolGraph) -> dict:
    schema: dict = {"title": s["pathComponents"][-1]}
    desc = doc_text(s)
    if desc:
        schema["description"] = desc
    cases = [c["pathComponents"][-1] for c in graph.enum_cases(s["pathComponents"])]
    # Raw-value enums are RawRepresentable; default the value type to string.
    schema["type"] = "string"
    if cases:
        schema["enum"] = cases
    return schema


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("source", type=Path, help="Symbol-graph .symbols.json file or directory")
    parser.add_argument("out", type=Path, help="Output directory for *.schema.json")
    parser.add_argument("--draft", default="2020-12", help="JSON Schema draft (default: 2020-12)")
    parser.add_argument("--exclude", action="append", default=[], metavar="Type.prop",
                        help="Force-exclude a property by dotted path (repeatable)")
    parser.add_argument("--include", action="append", default=[], metavar="Type.prop",
                        help="Force-include a property by dotted path (repeatable)")
    args = parser.parse_args()
    FORCE_EXCLUDE.update(args.exclude)
    FORCE_INCLUDE.update(args.include)

    if args.source.is_dir():
        paths = sorted(args.source.glob("*.symbols.json"))
    else:
        paths = [args.source]
    if not paths:
        print(f"no symbol-graph files found at {args.source}", file=sys.stderr)
        return 1

    graph = SymbolGraph(paths)
    files = build(graph, args.draft)
    if not files:
        print("no Codable types found in symbol graph", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    for filename, schema in sorted(files.items()):
        (args.out / filename).write_text(json.dumps(schema, indent=2) + "\n")
        print(f"wrote {args.out / filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
