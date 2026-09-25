"""Provide console entry points for the package."""

import argparse
import logging

from databricks.sdk import WorkspaceClient

from .skills import install_skills, install_user_skill, install_workspace_skill

logger = logging.getLogger(__name__)


def cli_foobar() -> None:
    """Build and display a one-row DataFrame from CLI arguments.

    Returns:
        None.
    """
    # Avoid creating a Spark session when running a skill installer.
    from . import spark

    parser = argparse.ArgumentParser(add_help=True, description="Sample CLI")
    parser.add_argument('--foo', default="foo", type=str, required=False, help="FOO text")
    parser.add_argument('--bar', default="bar", type=str, required=False, help="BAR text")
    args = parser.parse_args()

    w = WorkspaceClient()
    logger.info(f"Current cluster id: {w.config.cluster_id!r}")
    cluster = w.clusters.get(w.config.cluster_id)
    logger.info(f"Current cluster name: {cluster.cluster_name!r}")

    df = spark.createDataFrame([[args.foo, args.bar]], "foo string, bar string")
    df.show(truncate=False)


def cli_install_skills() -> None:
    """Install bundled skills locally.

    Returns:
        None.
    """
    installed = install_skills()
    print(f"Installed {len(installed)} skill(s) to ~/.agents/skills: {', '.join(installed) or '(none)'}")


def cli_install_user_skill() -> None:
    """Upload bundled skills to the current user's Databricks folder.

    Returns:
        None.
    """
    installed = install_user_skill()
    print(
        f"Uploaded {len(installed)} skill(s) to your Databricks user skills folder: {', '.join(installed) or '(none)'}"
    )


def cli_install_workspace_skill() -> None:
    """Upload bundled skills to the workspace-wide Databricks folder.

    Returns:
        None.
    """
    installed = install_workspace_skill()
    print(f"Uploaded {len(installed)} skill(s) to the workspace skills folder: {', '.join(installed) or '(none)'}")
