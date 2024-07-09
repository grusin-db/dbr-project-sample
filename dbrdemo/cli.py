import argparse
import logging
from databricks.sdk import WorkspaceClient
from . import spark

logger = logging.getLogger(__name__)


def cli_foobar():
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
