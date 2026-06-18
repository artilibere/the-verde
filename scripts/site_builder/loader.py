"""Load and validate JSON content documents."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
from jsonschema.validators import validator_for

SCHEMAS_DIR_NAME = "_schemas"
SKIP_DIRS = {"_config", "_schemas"}


def load_json(path: Path) -> dict | list:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _schemas_dir(content_dir: Path) -> Path:
    return content_dir / SCHEMAS_DIR_NAME


def load_schema_store(content_dir: Path) -> dict[str, dict]:
    store: dict[str, dict] = {}
    schema_dir = _schemas_dir(content_dir)
    if not schema_dir.exists():
        return store
    for path in sorted(schema_dir.glob("*.schema.json")):
        schema = json.loads(path.read_text(encoding="utf-8"))
        sid = schema.get("$id", path.name)
        store[sid] = schema
        store[path.name] = schema
    return store


def _resolve_ref(ref: str, store: dict[str, dict]) -> dict:
    if ref in store:
        return copy.deepcopy(store[ref])
    name = ref.split("/")[-1]
    if name in store:
        return copy.deepcopy(store[name])
    raise ValueError(f"Unresolved schema ref: {ref}")


def merge_schema(schema: dict, store: dict[str, dict]) -> dict:
    """Flatten allOf + $ref into a single schema dict."""
    if "allOf" not in schema:
        return copy.deepcopy(schema)
    merged: dict = {}
    for part in schema["allOf"]:
        if "$ref" in part:
            base = merge_schema(_resolve_ref(part["$ref"], store), store)
            merged = _deep_merge(merged, base)
        else:
            merged = _deep_merge(merged, copy.deepcopy(part))
    return merged


def _deep_merge(base: dict, overlay: dict) -> dict:
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def get_validator(content_dir: Path, doc_type: str):
    store = load_schema_store(content_dir)
    schema_name = f"{doc_type}.schema.json"
    if schema_name not in store:
        raise ValueError(f"Schema not found for type: {doc_type}")
    schema = merge_schema(store[schema_name], store)
    cls = validator_for(schema)
    return cls(schema)


def validate_document(content_dir: Path, doc: dict) -> list[str]:
    doc_type = doc.get("type")
    if not doc_type:
        return ["Missing document type"]
    try:
        validator = get_validator(content_dir, doc_type)
    except ValueError as exc:
        return [str(exc)]
    errors = []
    for error in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.path) or "(root)"
        errors.append(f"{path}: {error.message}")
    return errors


def infer_type_from_path(path: Path, content_dir: Path) -> str:
    rel = path.relative_to(content_dir)
    parts = rel.parts
    if parts[0] == "varieta":
        return "variety"
    if parts[0] == "guide":
        return "article"
    if parts[0] == "glossario":
        return "glossary"
    if parts[0] == "impara" and len(parts) > 2 and parts[1] == "controversie":
        return "controversy"
    if parts[0] == "impara":
        return "hub"
    if parts[0] == "italia":
        if path.stem == "abbinamenti":
            return "article"
        return "hub"
    if parts[0] == "gioca" and len(parts) > 1 and parts[1] == "percorsi":
        return "article"
    if parts[0] == "pagine":
        return "page"
    return "article"


SKIP_FILES = {"relazioni.json"}


def discover_documents(content_dir: Path) -> list[Path]:
    paths: list[Path] = []
    for path in sorted(content_dir.rglob("*.json")):
        if path.name in SKIP_FILES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(content_dir).parts):
            continue
        if path.parent.name == SCHEMAS_DIR_NAME:
            continue
        paths.append(path)
    return paths


def load_document(path: Path, content_dir: Path) -> dict:
    doc = json.loads(path.read_text(encoding="utf-8"))
    doc.setdefault("slug", path.stem)
    doc.setdefault("type", infer_type_from_path(path, content_dir))
    doc.setdefault("schema_version", "1.0")
    return doc


def load_all_documents(content_dir: Path, *, validate: bool = True) -> list[dict]:
    docs: list[dict] = []
    errors: list[str] = []
    for path in discover_documents(content_dir):
        doc = load_document(path, content_dir)
        if validate:
            doc_errors = validate_document(content_dir, doc)
            if doc_errors:
                errors.extend(f"{path}: {e}" for e in doc_errors)
        docs.append(doc)
    if errors:
        raise ValueError("Content validation failed:\n" + "\n".join(errors))
    return docs


def index_documents(docs: list[dict]) -> dict[str, dict[str, dict]]:
    by_type: dict[str, dict[str, dict]] = {}
    for doc in docs:
        dtype = doc.get("type", "article")
        slug = doc.get("slug", "")
        by_type.setdefault(dtype, {})[slug] = doc
    return by_type
