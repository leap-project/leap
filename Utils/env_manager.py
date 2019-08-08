""" Responsible for loading global variables in cloud_algos and site_algos
"""
import pdb
import logging
from pylogrus import PyLogrus, TextFormatter
import json
import inspect 

import CloudAlgo.functions as leap_fn
import Utils.env_utils as env_utils

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
        self.logger = logger.withFields({"node": "site-algo"})

    def set_env(self, context, req):
        import pandas as pd
        globals()["pd"] = pd
        self.logger.info("Loaded base site environment variables")


class SiteUDFEnvironment(SiteEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)

        exec(req["map_fns"], globals())
        context["map_fn"] = map_fns()
        exec(req["choice_fn"], context)
        exec(req["dataprep_fn"], context)

        self.logger.info("Loaded site environment variables for udf function.")


class SitePredefinedEnvironment(SiteEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)
        algo_code = req["algo_code"]
        module = getattr(leap_fn, algo_code)

        env_utils.load_fn("choice_fn", req, module, context)
        env_utils.load_fn("dataprep_fn", req, module, context)
        env_utils.load_from_fn_generator("map_fns", "map_fn", req, module, context)
        
        self.logger.info("Loaded site environment variables for predefined function.")


class SiteFederatedLearningEnvironment(SitePredefinedEnvironment):
    def set_env(self, context, req):
        algo_code = req["algo_code"]
        module = getattr(leap_fn, algo_code)

        ### Fn specific imports
        import torch
        globals()["torch"] = torch
        context["torch"] = torch
        import pandas as pd
        context["pd"] = pd        
        context["AverageMeter"] = leap_fn.fl_fn.AverageMeter

        hyperparams = json.loads(req["hyperparams"])
        context["hyperparams"] = hyperparams
        ###
        exec(req["get_model"], globals())
        model = get_model(hyperparams)
        context["model"] = model

        exec(req["get_optimizer"], globals())
        optimizer = get_optimizer(model.parameters(), hyperparams)
        context["optimizer"] = optimizer

        exec(req["get_criterion"], globals())
        criterion = get_criterion(hyperparams)
        context["criterion"] = criterion
        
        exec(req["get_dataloader"], globals())
        # dataloader = get_dataloader(hyperparams)        
        context["get_dataloader"] = get_dataloader

        self.logger.info("Loaded site environment variables for federated learning.")
        super().set_env(context, req)


class CloudEnvironment(Environment):
    def __init__(self):
        self.logger = logger.withFields({"node": "cloud-algo"})

    def set_env(self, context, req):
        import json
        context["json"] = json
        self.logger.info("Loaded base cloud environment variables.")


class CloudUDFEnvironment(CloudEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)

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
        self.logger.info("Loaded cloud environment variables for udf function.")
        

class CloudPredefinedEnvironment(CloudEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)
        algo_code = req["algo_code"]
        module = getattr(leap_fn, algo_code)
        
        env_utils.load_fn("init_state_fn", req, module, context)
        env_utils.load_fn("choice_fn", req, module, context)
        env_utils.load_fn("stop_fn", req, module, context)
        env_utils.load_fn("postprocessing_fn", req, module, context)

        env_utils.load_from_fn_generator("update_fns", "update_fn", req, module, context)
        env_utils.load_from_fn_generator("agg_fns", "agg_fn", req, module, context)
        self.logger.info("Loaded cloud environment variables for predefined function.")

class CloudFedereatedLearningEnvironment(CloudPredefinedEnvironment):
    def set_env(self, context, req):
        super().set_env(context, req)
        import torch
        globals()["torch"] = torch
        context["torch"] = torch
        context["AverageMeter"] = leap_fn.fl_fn.AverageMeter

        hyperparams = json.loads(req["hyperparams"])
        context["hyperparams"] = hyperparams
        
        # pass in context as second argument so that get_model has access to context variables
        exec(req["get_model"], globals()) 
        model = get_model(hyperparams)
        context["model"] = model

        exec(req["get_optimizer"], globals())
        optimizer = get_optimizer(model.parameters(), hyperparams)
        context["optimizer"] = optimizer

        exec(req["get_criterion"], globals())
        criterion = get_criterion(hyperparams)
        context["criterion"] = criterion
        
