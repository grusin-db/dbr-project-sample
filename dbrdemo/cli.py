"""Provide console entry points for the package."""

import argparse

from .documentation import list_docs, read_doc
from .foobar import write_foobar
from .skills import install_skills, install_user_skills, install_workspace_skills


def cli_foobar() -> None:
    """Append a foo/bar row to a Databricks table.

    Returns:
        None.
    """
    parser = argparse.ArgumentParser(add_help=True, description="Append a foo/bar row to a Databricks table")
    parser.add_argument('--table', type=str, required=True, help="Target table: catalog.schema.table")
    parser.add_argument('--foo', default="foo", type=str, required=False, help="FOO text")
    parser.add_argument('--bar', default="bar", type=str, required=False, help="BAR text")
    args = parser.parse_args()

    write_foobar(args.table, args.foo, args.bar)


def cli_docs() -> None:
    """Display documentation bundled in the installed package.

    Returns:
        None.
    """
    parser = argparse.ArgumentParser(add_help=True, description="Display bundled dbrdemo documentation")
    parser.add_argument("document", choices=list_docs(), default="README.md", nargs="?")
    args = parser.parse_args()

    print(read_doc(args.document))


def cli_install_skills() -> None:
    """Install bundled skills locally.

    Returns:
        None.
    """
    installed = install_skills()
    print(f"Installed {len(installed)} skill(s) to ~/.agents/skills: {', '.join(installed) or '(none)'}")


def cli_install_user_skills() -> None:
    """Upload bundled skills to the current user's Databricks folder.

    Returns:
        None.
    """
    installed = install_user_skills()
    print(
        f"Uploaded {len(installed)} skill(s) to your Databricks user skills folder: {', '.join(installed) or '(none)'}"
    )


def cli_install_workspace_skills() -> None:
    """Upload bundled skills to the workspace-wide Databricks folder.

    Returns:
        None.
    """
    installed = install_workspace_skills()
    print(f"Uploaded {len(installed)} skill(s) to the workspace skills folder: {', '.join(installed) or '(none)'}")
