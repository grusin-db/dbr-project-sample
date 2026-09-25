"""Test the installed wheel outside the source checkout."""

import os
import subprocess
import sys
from pathlib import Path


def test_installed_wheel_contains_resources_and_scripts(tmp_path: Path) -> None:
    """Verify the installed wheel from a temporary working directory.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        None.
    """
    script = """
import importlib.metadata
from pathlib import Path
import sys

import dbrdemo
from dbrdemo.documentation import list_docs
from dbrdemo.skills import _source_skill_dirs

assert Path(dbrdemo.__file__).resolve().is_relative_to(Path(sys.prefix).resolve())
assert "user/foobar.md" in list_docs()
assert [path.name for path in _source_skill_dirs()] == ["dbrdemo-getting-started"]

distribution = importlib.metadata.distribution("dbrdemo")
assert distribution.metadata["License-Expression"] == "Apache-2.0"
assert set(distribution.metadata.get_all("Project-URL") or []) == {
    "Documentation, https://github.com/grusin-db/dbr-project-sample/tree/main/docs",
    "Repository, https://github.com/grusin-db/dbr-project-sample",
}
scripts = {
    entry.name
    for entry in distribution.entry_points
    if entry.group == "console_scripts"
}
assert scripts == {
    "dbrdemo-docs",
    "dbrdemo-foobar",
    "dbrdemo-install-skills",
    "dbrdemo-install-user-skills",
    "dbrdemo-install-workspace-skills",
}
"""
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    for name in tuple(environment):
        if name == "COVERAGE_PROCESS_START" or name.startswith("COV_CORE_"):
            environment.pop(name)

    subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=environment,
        check=True,
    )
