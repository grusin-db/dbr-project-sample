"""Test local Agent Skill installation."""

from pathlib import Path

import pytest

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
