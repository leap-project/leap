""" Responsible for loading global variables in cloud_algos and site_algos
"""
import pdb
import logging
from pylogrus import PyLogrus, TextFormatter

# Setup logging tool
logging.setLoggerClass(PyLogrus)
logger = logging.getLogger(__name__)  # type: PyLogrus
logger.setLevel(logging.DEBUG)
formatter = TextFormatter(datefmt='Z', colorize=True)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

""" Any commonalities between site and cloud environments
"""
class Environment():
    pass


class SiteEnvironment(Environment):
    pass

class CloudEnvironment(Environment):
    def __init__(self):
        self.logger = logger.withFields({"node": "cloud-env"})

    def set_env(self, context):
        import pandas as pd
        context["pd"] = pd
        self.logger.info("Loaded base cloud environment variables")

class CloudUDFEnvironment(CloudEnvironment):
    def set_env(self, context):
        super().set_env(context)
        import math
        context["math"] = math
        self.logger.info("Loaded custom cloud environment variables")


