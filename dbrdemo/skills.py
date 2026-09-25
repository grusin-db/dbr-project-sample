"""Install bundled Agent Skills locally or in Databricks."""

import logging
import os
import shutil
from pathlib import Path

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat

logger = logging.getLogger(__name__)

SKILL_DIR_PREFIX = "dbrdemo-"
SKILLS_SRC = Path(__file__).parent / "resources" / "skills"
LOCAL_SKILLS_PATH = Path.home() / ".agents" / "skills"
WORKSPACE_SKILLS_PATH = "/Workspace/.assistant/skills"


def _source_skill_dirs() -> list[Path]:
    """Find the bundled skill directories to install.

    Returns:
        Sorted bundled directories whose names start with ``SKILL_DIR_PREFIX``.
    """
    if not SKILLS_SRC.is_dir():
        return []
    return sorted(p for p in SKILLS_SRC.iterdir() if p.is_dir() and p.name.startswith(SKILL_DIR_PREFIX))


def install_skills(target: Path | None = None) -> list[str]:
    """Install bundled skills in the local Agent Skills directory.

    Args:
        target: Override the target directory (used by tests).

    Returns:
        Sorted names of the installed skill directories.
    """
    target = target or LOCAL_SKILLS_PATH
    target.mkdir(parents=True, exist_ok=True)

    for existing in target.iterdir():
        if existing.is_dir() and existing.name.startswith(SKILL_DIR_PREFIX):
            shutil.rmtree(existing)

    installed = []
    for src in _source_skill_dirs():
        shutil.copytree(src, target / src.name, dirs_exist_ok=True)
        installed.append(src.name)

    logger.info("Installed %d skills to %s", len(installed), target)
    return sorted(installed)


def install_user_skill() -> list[str]:
    """Upload bundled skills to the current user's Databricks skills folder.

    Returns:
        Sorted names of the installed skill directories.
    """
    ws = WorkspaceClient()
    user_name = ws.current_user.me().user_name
    target = f"/Users/{user_name}/.assistant/skills"
    return _upload_to_databricks(ws, target)


def install_workspace_skill() -> list[str]:
    """Upload bundled skills to the workspace-wide Databricks skills folder.

    Returns:
        Sorted names of the installed skill directories.
    """
    ws = WorkspaceClient()
    return _upload_to_databricks(ws, WORKSPACE_SKILLS_PATH)


def _upload_to_databricks(ws: WorkspaceClient, target: str) -> list[str]:
    """Replace prefixed skill directories with the bundled skills.

    Args:
        ws: Authenticated Databricks workspace client.
        target: Databricks workspace directory to install into.

    Returns:
        Sorted names of the installed skill directories.
    """
    list_path = target[len("/Workspace") :] if target.startswith("/Workspace") else target

    try:
        for obj in ws.workspace.list(list_path):
            if not obj.path:
                continue
            name = obj.path.rsplit("/", 1)[-1]
            if obj.object_type and obj.object_type.value == "DIRECTORY" and name.startswith(SKILL_DIR_PREFIX):
                ws.workspace.delete(obj.path, recursive=True)
    except Exception as e:  # noqa: BLE001 - target may not exist yet
        logger.debug("Skip skills cleanup for %s: %s", target, e)

    installed: set[str] = set()
    made_dirs: set[str] = set()
    for src in _source_skill_dirs():
        for dirpath, dirnames, filenames in os.walk(src):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for fname in filenames:
                if fname.startswith("__"):
                    continue
                local = Path(dirpath) / fname
                rel = local.relative_to(SKILLS_SRC).as_posix()
                remote = f"{target}/{rel}"
                remote_dir = remote.rsplit("/", 1)[0]
                if remote_dir not in made_dirs:
                    ws.workspace.mkdirs(remote_dir)
                    made_dirs.add(remote_dir)
                ws.workspace.upload(remote, local.read_bytes(), format=ImportFormat.AUTO, overwrite=True)
        installed.add(src.name)

    logger.info("Installed %d skills to %s", len(installed), target)
    return sorted(installed)
