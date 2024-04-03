from databricks.labs.blueprint.logger import install_logger
install_logger()

import logging
logging.getLogger().setLevel(level=logging.CRITICAL)
logger = logging.getLogger('dbrdemo.update_package_version')
logger.setLevel(logging.DEBUG)

from datetime import datetime
import sh
import sys
from packaging import version
import argparse
import logging
import re

def get_current_version():
    VERSIONFILE="dbrdemo/version.py"
    verstrline = open(VERSIONFILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

def build_pkg_version(*, env: str, date_str: str, daily_build_numer: str, commit: str, build_id: str):
    base_version = version.parse(get_current_version()).base_version
    date_str = datetime.now().strftime("%Y.%m.%d")
    commit:str = commit or sh.git('rev-parse', '--short', 'HEAD')
    commit = commit.strip()
    daily_build_numer = daily_build_numer or "0"
    build_id = build_id or ""

    if env[0] == "l" or not env:
        v = version.parse(f"{base_version}alpha+{date_str}")
    elif env[0] == "d":
        v = version.parse(f"{base_version}dev+{date_str}.{daily_build_numer}.{commit}")
    elif env[0] == "t":
        v = version.parse(f"{base_version}beta+{date_str}.{daily_build_numer}.{commit}")
    elif env[0] == "a":
        v = version.parse(f"{base_version}rc+{date_str}.{daily_build_numer}.{commit}")
    elif env[0] == "p":
        v = version.parse(base_version)
    else:
        raise ValueError("Invalid env")

    return str(v)

def set_package_version(version: str):
	with open('dbrdemo/version.py', 'w') as f:
		f.write(f"__version__ = '{version}'\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('--env', required=True)
    parser.add_argument('--date-str')
    parser.add_argument('--daily-build-no')
    parser.add_argument('--commit')
    parser.add_argument('--build-id')

    args = parser.parse_args()

    v = build_pkg_version(
         env=args.env, 
         date_str=args.date_str,
         daily_build_numer=args.daily_build_no,
         commit=args.commit,
         build_id=args.build_id)
    logger.info(f"Setting package version: {v}")
    set_package_version(v)

    with open('.dist_version', "w", encoding="utf-8") as f:
        f.write(str(v))
