import argparse
import logging

logger = logging.getLogger(__name__)


def cli_foobar():
    parser = argparse.ArgumentParser(add_help=True, description="Sample CLI")

    parser.add_argument('--foo', default=1, type=int, required=False, help="FOO Counter")
    parser.add_argument('--bar', default=1, type=int, required=False, help="BAR Counter")

    args = parser.parse_args()

    for _ in range(args.foo):
        logger.info("FOO!!!")

    for _ in range(args.bar):
        logger.warning("BAR!!!")
