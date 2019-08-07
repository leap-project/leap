""" Responsible for loading global variables in cloud_algos and site_algos
"""
import pdb
import logging
from pylogrus import PyLogrus, TextFormatter
import json

import LeapLocal.functions as leap_fn

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

    def set_env(self, context, req):
        self.logger.info("Loaded base cloud environment variables")
        import pandas as pd
        globals()["pd"] = pd

class SiteUDFEnvironment(SiteEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)        
        self.logger.info("Loading custom cloud udf environment variables")

        exec(req["map_fns"], globals())
        context["map_fn"] = map_fns()

        exec(req["choice_fn"], context)
        exec(req["dataprep_fn"], context)

class SitePredefinedEnvironment(SiteEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)        
        self.logger.info("Loading custom cloud predefined environment variables")

        algo_code = req["algo_code"]
        module = getattr(leap_fn, algo_code)
        # TODO: Run only the parts that are needed from module
        exec(module, context)
        if req["choice_fn"] != "":
            exec(req["choice_fn"], context)
        if req["dataprep_fn"] != "":
            exec(req["dataprep_fn"], context)
        if req["map_fns"] != "":
            exec(req["map_fns"], globals())
            map_fn = update_fns()
            context["map_fn"] = update_fn

class CloudEnvironment(Environment):
    def __init__(self):
        self.logger = logger.withFields({"node": "cloud-env"})

    def set_env(self, context, req):
        import json
        
        context["json"] = json
        self.logger.info("Loaded base cloud environment variables")

       
        

class CloudUDFEnvironment(CloudEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)        
        self.logger.info("Loading custom cloud udf environment variables")


        exec(req["init_state_fn"], context)
        exec(req["choice_fn"], context)
        exec(req["stop_fn"], context)
        exec(req["postprocessing_fn"], context)
        
        exec(req["update_fns"], globals())
        exec(req["agg_fns"], globals())
        update_fn = update_fns()
        agg_fn = agg_fns()
        context["update_fn"] = update_fn
        context["agg_fn"] = agg_fn
        self.logger.info("Loaded custom cloud environment variables")
        

class CloudPredefinedEnvironment(CloudEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)        
        self.logger.info("Loading custom cloud predefined environment variables")

        # Responsible for loading predefined functions if not exists in request
        algo_code = req["algo_code"]
        module = getattr(leap_fn, algo_code)
        exec(module, context)
        # Overwrite individual fns
        if req["init_state_fn"] != "":
            exec(req["init_state_fn"], context)
        if req["choice_fn"] != "":
            exec(req["choice_fn"], context)
        if req["stop_fn"] != "":
            exec(req["stop_fn"], context)
        if req["postprocessing_fn"] != "":
            exec(req["postprocessing_fn"], context)

        if req["update_fns"] != "":
            exec(req["update_fns"], globals())
            update_fn = update_fns()
            context["update_fn"] = update_fn
        if req["agg_fn"] != "":
            exec(req["agg_fn"], globals())
            agg_fn = agg_fns()
            context["agg_fn"] = agg_fn
        
        