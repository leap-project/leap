""" Responsible for loading global variables in cloud_algos and site_algos
"""
import pdb
import logging
from pylogrus import PyLogrus, TextFormatter
import json

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
    def __init__(self):
        self.logger = logger.withFields({"node": "site-env"})

    def set_env(self, context, request):
        self.logger.info("Loaded base cloud environment variables")
        import pandas as pd
        globals()["pd"] = pd

class SiteUDFEnvironment(SiteEnvironment):
    def set_env(self, context, request):
        super().set_env(context, request)        
        self.logger.info("Loading custom cloud environment variables")
        req = json.loads(request.req)

        exec(req["get_map_fn"], globals())
        context["map_fn"] = get_map_fn()

        exec(req["choice_fn"], context)
        exec(req["dataprep_fn"], context)

class CloudEnvironment(Environment):
    def __init__(self):
        self.logger = logger.withFields({"node": "cloud-env"})

    def set_env(self, context, request):
        import json
        req = json.loads(request.req)
        
        context["json"] = json
        self.logger.info("Loaded base cloud environment variables")

       
        

class CloudUDFEnvironment(CloudEnvironment):
    def set_env(self, context, request):
        super().set_env(context, request)        
        self.logger.info("Loading custom cloud environment variables")

        req = json.loads(request.req)

        exec(req["init_state_fn"], context)
        exec(req["choice_fn"], context)
        exec(req["stop_fn"], context)
        exec(req["postprocessing_fn"], context)
        
        exec(req["get_update_fn"], globals())
        exec(req["get_agg_fn"], globals())
        update_fn = get_update_fn()
        agg_fn = get_agg_fn()
        context["update_fn"] = update_fn
        context["agg_fn"] = agg_fn
        self.logger.info("Loaded custom cloud environment variables")
        

