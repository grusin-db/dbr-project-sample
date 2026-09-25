"""Test the package command-line entry points."""

import sys
from collections.abc import Callable

import pytest

from dbrdemo import cli


def test_cli_foobar(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that the foo/bar command forwards parsed arguments.

    Args:
        monkeypatch: Pytest fixture for replacing functions and arguments.

    Returns:
        None.
    """
    calls: list[tuple[str, str, str]] = []

    def fake_write_foobar(table: str, foo: str, bar: str) -> None:
        calls.append((table, foo, bar))

    monkeypatch.setattr(cli, "write_foobar", fake_write_foobar)
    monkeypatch.setattr(
        sys,
        "argv",
        ["dbrdemo-foobar", "--table", "catalog.schema.table", "--foo", "hello", "--bar", "world"],
    )

    cli.cli_foobar()

    assert calls == [("catalog.schema.table", "hello", "world")]


def test_cli_docs(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    """Verify that the docs command prints a bundled document.

    Args:
        monkeypatch: Pytest fixture for replacing functions and arguments.
        capsys: Pytest fixture for capturing terminal output.

    Returns:
        None.
    """

    def fake_list_docs() -> list[str]:
        return ["user/foobar.md"]

    def fake_read_doc(document: str) -> str:
        return f"Documentation: {document}"

    monkeypatch.setattr(cli, "list_docs", fake_list_docs)
    monkeypatch.setattr(cli, "read_doc", fake_read_doc)
    monkeypatch.setattr(sys, "argv", ["dbrdemo-docs", "user/foobar.md"])

    cli.cli_docs()

    assert capsys.readouterr().out == "Documentation: user/foobar.md\n"


@pytest.mark.parametrize(
    ("entrypoint", "installer_name", "destination"),
    [
        (cli.cli_install_skills, "install_skills", "~/.agents/skills"),
        (cli.cli_install_user_skills, "install_user_skills", "your Databricks user skills folder"),
        (cli.cli_install_workspace_skills, "install_workspace_skills", "the workspace skills folder"),
    ],
)
def test_skill_install_commands(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    entrypoint: Callable[[], None],
    installer_name: str,
    destination: str,
) -> None:
    """Verify that each skill command reports its installed skills.

    Args:
        monkeypatch: Pytest fixture for replacing installer functions.
        capsys: Pytest fixture for capturing terminal output.
        entrypoint: Command-line entry point under test.
        installer_name: Installer function used by the entry point.
        destination: Expected destination text in the command output.

    Returns:
        None.
    """

    def fake_installer() -> list[str]:
        return ["dbrdemo-getting-started"]

    monkeypatch.setattr(cli, installer_name, fake_installer)

    entrypoint()

    output = capsys.readouterr().out
    assert "Installed 1 skill(s)" in output or "Uploaded 1 skill(s)" in output
    assert destination in output
    assert "dbrdemo-getting-started" in output
