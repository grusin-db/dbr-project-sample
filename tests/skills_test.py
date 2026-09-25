"""Test local and Databricks Agent Skill installation."""

from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from databricks.sdk import WorkspaceClient

from dbrdemo import skills
from dbrdemo.skills import SKILL_DIR_PREFIX, install_skills


@pytest.fixture
def skills_dir(tmp_path: Path) -> Path:
    """Create a temporary directory containing the bundled skills.

    Args:
        tmp_path: Temporary directory provided by pytest.

    Returns:
        The temporary skills directory.
    """
    install_skills(target=tmp_path)
    return tmp_path


def test_sample_skill_installed(skills_dir: Path) -> None:
    """Verify that the sample skill is installed.

    Args:
        skills_dir: Temporary directory containing the installed skills.

    Returns:
        None.
    """
    assert (skills_dir / "dbrdemo-getting-started" / "SKILL.md").is_file()


def test_reinstall_replaces_only_prefixed_skills(skills_dir: Path) -> None:
    """Verify that reinstalling replaces only project-owned skills.

    Args:
        skills_dir: Temporary directory containing the installed skills.

    Returns:
        None.
    """
    (skills_dir / f"{SKILL_DIR_PREFIX}stale").mkdir()
    (skills_dir / "third-party-skill").mkdir()

    install_skills(target=skills_dir)

    assert not (skills_dir / f"{SKILL_DIR_PREFIX}stale").exists()
    assert (skills_dir / "third-party-skill").exists()
    assert (skills_dir / "dbrdemo-getting-started").is_dir()


def test_upload_replaces_prefixed_workspace_skills() -> None:
    """Verify that a workspace upload replaces only project-owned skills.

    Returns:
        None.
    """
    ws = MagicMock()
    directory_type = SimpleNamespace(value="DIRECTORY")
    ws.workspace.list.return_value = [
        SimpleNamespace(path=None, object_type=directory_type),
        SimpleNamespace(path="/Workspace/.assistant/skills/third-party", object_type=directory_type),
        SimpleNamespace(path="/Workspace/.assistant/skills/dbrdemo-stale", object_type=directory_type),
    ]

    installed = skills._upload_to_databricks(ws, skills.WORKSPACE_SKILLS_PATH)

    assert installed == ["dbrdemo-getting-started"]
    ws.workspace.list.assert_called_once_with("/.assistant/skills")
    ws.workspace.delete.assert_called_once_with(
        "/Workspace/.assistant/skills/dbrdemo-stale",
        recursive=True,
    )
    ws.workspace.mkdirs.assert_called_once_with(
        "/Workspace/.assistant/skills/dbrdemo-getting-started",
    )
    assert ws.workspace.upload.call_args.args[0].endswith("/dbrdemo-getting-started/SKILL.md")


def test_upload_surfaces_workspace_listing_errors() -> None:
    """Verify that workspace failures are not treated as missing folders.

    Returns:
        None.
    """
    ws = MagicMock()
    ws.workspace.list.side_effect = RuntimeError("workspace unavailable")

    with pytest.raises(RuntimeError, match="workspace unavailable"):
        skills._upload_to_databricks(ws, skills.WORKSPACE_SKILLS_PATH)


@pytest.mark.parametrize(
    ("installer", "target"),
    [
        (skills.install_user_skills, "/Users/test@example.com/.assistant/skills"),
        (skills.install_workspace_skills, skills.WORKSPACE_SKILLS_PATH),
    ],
)
def test_databricks_install_targets(
    monkeypatch: pytest.MonkeyPatch,
    installer: Callable[[], list[str]],
    target: str,
) -> None:
    """Verify user and workspace installers select the correct target.

    Args:
        monkeypatch: Pytest fixture for replacing the workspace client.
        installer: Databricks skill installer under test.
        target: Expected Databricks workspace path.

    Returns:
        None.
    """
    ws = MagicMock()
    ws.current_user.me.return_value.user_name = "test@example.com"
    calls: list[tuple[WorkspaceClient, str]] = []

    def fake_workspace_client() -> MagicMock:
        return ws

    def fake_upload(client: WorkspaceClient, upload_target: str) -> list[str]:
        calls.append((client, upload_target))
        return ["dbrdemo-getting-started"]

    monkeypatch.setattr(skills, "WorkspaceClient", fake_workspace_client)
    monkeypatch.setattr(skills, "_upload_to_databricks", fake_upload)

    assert installer() == ["dbrdemo-getting-started"]
    assert calls == [(ws, target)]
