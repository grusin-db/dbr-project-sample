"""Test package initialization."""

import logging
import subprocess
import sys


def test_import_preserves_root_logging() -> None:
    """Verify that importing the package does not configure application logging.

    Returns:
        None.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import logging; "
                "logging.getLogger().setLevel(logging.WARNING); "
                "import dbrdemo; "
                "print(logging.getLogger().level)"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout == f"{logging.WARNING}\n"


def test_install_logger_logs_version() -> None:
    """Verify that installing the logger focuses output on dbrdemo.

    Returns:
        None.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import logging\n"
                "from dbrdemo import install_logger\n"
                "install_logger()\n"
                "print(logging.getLogger().level)\n"
                "print(logging.getLogger('dbrdemo').level)\n"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Using dbrdemo version:" in result.stdout + result.stderr
    assert result.stdout.endswith(f"{logging.CRITICAL}\n{logging.DEBUG}\n")
