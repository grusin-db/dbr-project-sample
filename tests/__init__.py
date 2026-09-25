"""Configure logging for the test suite."""

import logging

logging.getLogger('urllib3.connectionpool').setLevel('INFO')
