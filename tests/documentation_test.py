"""Test documentation bundled with the package."""

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
        "user/README.md",
        "user/foobar.md",
    }

    assert expected <= set(list_docs())
    assert "write_foobar" in read_doc("user/foobar.md")
