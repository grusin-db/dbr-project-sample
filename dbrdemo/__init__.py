from databricks.labs.blueprint.logger import install_logger

install_logger()

import logging

logging.getLogger().setLevel(level=logging.CRITICAL)
logger = logging.getLogger('dbrdemo')
logger.setLevel(logging.DEBUG)

from .version import __version__

logger.info(f"Using dbrdemo version: {__version__}")

import datetime

from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession


def _get_spark_seession() -> SparkSession:
    try:
        # if running in real databricks
        from pyspark.sql import SparkSession
        spark = SparkSession.getActiveSession()
    except: # NOQA
        spark = None

    if not spark:
        logger.debug("Trying to aquire vscode/pytest databricks connect session...")
        from databricks.connect.session import DatabricksSession
        spark_unsupported_tz_map = {"CEST": "+01:00"}

        spark = DatabricksSession.builder.getOrCreate()
        now = datetime.datetime.now()
        local_now = now.astimezone()
        local_tz = local_now.tzinfo
        local_tzname = local_tz.tzname(local_now)
        local_tzname = spark_unsupported_tz_map.get(local_tzname) or local_tzname
        spark.conf.set('spark.sql.session.timeZone', local_tzname)

        # TODO: use ascii art to make this personalized just for your code!!! :)
        #       Open source tools for generating ascii art: https://itsfoss.com/ascii-art-linux-terminal/
        logger.warning("_________ _______  _______ _________   _______  _______  ______   _______ ")
        logger.warning("\\__   __/(  ____ \\(  ____ \\\\__   __/  (       )(  ___  )(  __  \\ (  ____ \\")
        logger.warning("   ) (   | (    \\/| (    \\/   ) (     | () () || (   ) || (  \\  )| (    \\/")
        logger.warning("   | |   | (__    | (_____    | |     | || || || |   | || |   ) || (__    ")
        logger.warning("   | |   |  __)   (_____  )   | |     | |(_)| || |   | || |   | ||  __)   ")
        logger.warning("   | |   | (            ) |   | |     | |   | || |   | || |   ) || (      ")
        logger.warning("   | |   | (____/\\/\\____) |   | |     | )   ( || (___) || (__/  )| (____/\\")
        logger.warning("   )_(   (_______/\\_______)   )_(     |/     \\|(_______)(______/ (_______/")

    spark.conf.set('spark.sql.legacy.timeParserPolicy', 'CORRECTED')
    spark.conf.set('spark.sql.legacy.json.allowEmptyString.enabled', 'true')

    return spark


spark = _get_spark_seession()
dbutils = DBUtils(spark)
