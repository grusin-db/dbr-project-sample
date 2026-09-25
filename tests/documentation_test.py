"""Test documentation bundled with the package."""

import pytest

from dbrdemo.documentation import list_docs, read_doc


def test_foobar_docs() -> None:
    """Verify that documentation indexes and the foo/bar guide are available.

    Returns:
        None.
    """
    expected = {
        "README.md",
        "admin/README.md",
        "developer/README.md",
        "developer/testing.md",
        "user/README.md",
        "user/foobar.md",
        "user/local-notebook.md",
    }

    assert expected <= set(list_docs())
    assert "write_foobar" in read_doc("user/foobar.md")


def test_read_doc_rejects_parent_path() -> None:
    """Verify that documentation reads stay in the bundled directory.

    Returns:
        None.
    """
    with pytest.raises(ValueError):
        read_doc("../__init__.py")
