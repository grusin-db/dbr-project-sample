"""Build and write environment-specific package versions."""

import argparse
import re
import subprocess
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

VERSION_FILE = Path("dbrdemo/version.py")
DIST_VERSION_FILE = Path(".dist_version")
SUPPORTED_ENVIRONMENTS = ("dev", "test", "acc", "prod")
VERSION_PATTERN = re.compile(r"^__version__ = ['\"](?P<version>[^'\"]+)['\"]", re.MULTILINE)
BASE_VERSION_PATTERN = re.compile(r"^(?P<base>\d+\.\d+\.\d+)")


def get_current_version(version_file: Path = VERSION_FILE) -> str:
    """Read the current package version.

    Args:
        version_file: Python file containing ``__version__``.

    Returns:
        The current package version.
    """
    match = VERSION_PATTERN.search(version_file.read_text(encoding="utf-8"))
    if match is None:
        raise ValueError(f"Unable to find __version__ in {version_file}")
    return match.group("version")


def get_git_commit() -> str:
    """Read the short commit hash for the current checkout.

    Returns:
        The short Git commit hash.
    """
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def build_package_version(
    current_version: str,
    environment: str,
    date_str: str,
    daily_build_number: int,
    commit: str,
) -> str:
    """Build a PEP 440 package version for an environment.

    Args:
        current_version: Current package version containing the base version.
        environment: Release environment: dev, test, acc, or prod.
        date_str: Build date in ``YYYY.MM.DD`` format.
        daily_build_number: Build sequence number for the date.
        commit: Short Git commit hash.

    Returns:
        The environment-specific package version.
    """
    if environment not in SUPPORTED_ENVIRONMENTS:
        supported = ", ".join(SUPPORTED_ENVIRONMENTS)
        raise ValueError(f"Unsupported environment {environment!r}; expected one of: {supported}")

    match = BASE_VERSION_PATTERN.match(current_version)
    if match is None:
        raise ValueError(f"Version {current_version!r} does not start with major.minor.patch")

    base_version = match.group("base")
    if environment == "prod":
        return base_version

    suffix = {
        "dev": ".dev0",
        "test": "b0",
        "acc": "rc0",
    }[environment]
    return f"{base_version}{suffix}+{date_str}.{daily_build_number}.{commit.lower()}"


def update_package_version(
    environment: str,
    daily_build_number: int = 0,
    date_str: str | None = None,
    commit: str | None = None,
    version_file: Path = VERSION_FILE,
    dist_version_file: Path = DIST_VERSION_FILE,
) -> str:
    """Update the package and distribution version files.

    Args:
        environment: Release environment: dev, test, acc, or prod.
        daily_build_number: Build sequence number for the date.
        date_str: Override the UTC build date.
        commit: Override the short Git commit hash.
        version_file: Python file containing ``__version__``.
        dist_version_file: File receiving the built version.

    Returns:
        The package version written to both files.
    """
    package_version = build_package_version(
        current_version=get_current_version(version_file),
        environment=environment,
        date_str=date_str or datetime.now(UTC).strftime("%Y.%m.%d"),
        daily_build_number=daily_build_number,
        commit=commit or get_git_commit(),
    )
    version_file.write_text(f"__version__ = '{package_version}'\n", encoding="utf-8")
    dist_version_file.write_text(f"{package_version}\n", encoding="utf-8")
    return package_version


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: Optional command-line argument sequence.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Update the dbrdemo package version")
    parser.add_argument("--env", choices=SUPPORTED_ENVIRONMENTS, required=True)
    parser.add_argument("--daily-build-no", default=0, type=int)
    parser.add_argument("--date")
    parser.add_argument("--commit")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """Update the package version from command-line arguments.

    Args:
        argv: Optional command-line argument sequence.

    Returns:
        None.
    """
    args = parse_args(argv)
    package_version = update_package_version(
        environment=args.env,
        daily_build_number=args.daily_build_no,
        date_str=args.date,
        commit=args.commit,
    )
    print(f"Set package version: {package_version}")


if __name__ == "__main__":
    main()
