"""Validate all editorial JSON documents against schemas."""

from __future__ import annotations

from site_builder.loader import discover_documents, load_document, validate_document

from conftest import CONTENT_DIR


def test_all_content_documents_validate():
    errors = []
    for path in discover_documents(CONTENT_DIR):
        doc = load_document(path, CONTENT_DIR)
        doc_errors = validate_document(CONTENT_DIR, doc)
        errors.extend(f"{path.relative_to(CONTENT_DIR)}: {e}" for e in doc_errors)
    assert not errors, "\n".join(errors)


def test_minimum_document_count():
    paths = discover_documents(CONTENT_DIR)
    assert len(paths) >= 75
