"""Access documentation bundled in the installed package."""

from pathlib import Path

DOCS_PATH = Path(__file__).parent / "resources" / "docs"


def list_docs() -> list[str]:
    """List bundled Markdown documents.

    Returns:
        Sorted document paths relative to the bundled docs directory.
    """
    return sorted(path.relative_to(DOCS_PATH).as_posix() for path in DOCS_PATH.rglob("*.md"))


def read_doc(relative_path: str) -> str:
    """Read a bundled Markdown document.

    Args:
        relative_path: Path relative to the bundled docs directory.

    Returns:
        The document content.
    """
    docs_path = DOCS_PATH.resolve()
    document_path = (docs_path / relative_path).resolve()
    if not document_path.is_relative_to(docs_path):
        raise ValueError(f"Document path must stay inside {DOCS_PATH}")
    return document_path.read_text(encoding="utf-8")
