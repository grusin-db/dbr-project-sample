import logging
logging.getLogger('urllib3.connectionpool').setLevel('INFO')

import dbrdemo
from dbrdemo import spark

logger = dbrdemo.logger.getChild("__test__init__")

spark.conf.set('spark.sql.shuffle.partitions', 1)

logger.info("Testing framework is initialized!")
