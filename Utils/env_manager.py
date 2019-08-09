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

    def set_env(self, context, req, req_id):
        self.logger.withFields({"request-id": req_id}).info("Loaded base site environment variables")


class SiteUDFEnvironment(SiteEnvironment):
    def set_env(self, context, req, req_id):
        super().set_env(context, req, req_id)

        exec(req["map_fns"], context, globals())
        context["map_fn"] = map_fns()
        exec(req["choice_fn"], context)
        exec(req["dataprep_fn"], context)

        self.logger.withFields({"request-id": req_id}).info("Loaded site environment variables for udf function.")


class SitePredefinedEnvironment(SiteEnvironment):
    def set_env(self, context, req, req_id):
        super().set_env(context, req, req_id)
        algo_code = req["algo_code"]
        module = getattr(leap_fn, algo_code)

        env_utils.load_fn("choice_fn", req, context, module=module)
        env_utils.load_fn("dataprep_fn", req, context, module=module)
        env_utils.load_from_fn_generator("map_fns", "map_fn", req, context, module=module)
        
        self.logger.withFields({"request-id": req_id}).info("Loaded site environment variables for predefined function.")


class SiteFederatedLearningEnvironment(SitePredefinedEnvironment):
    def set_env(self, context, req, req_id):
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

        env_utils.load_fn("get_dataloader", req, context)
        env_utils.load_from_fn_generator("get_model", "model", req, context, gen_fn_args=[hyperparams])
        params = context["model"].parameters()
        env_utils.load_from_fn_generator("get_optimizer", "optimizer", req, context, gen_fn_args=[params, hyperparams])
        env_utils.load_from_fn_generator("get_criterion", "criterion", req, context, gen_fn_args=[hyperparams])

        super().set_env(context, req, req_id)
        self.logger.withFields({"request-id": req_id}).info("Loaded site environment variables for federated learning.")


class CloudEnvironment(Environment):
    def __init__(self):
        self.logger = logger.withFields({"node": "cloud-algo"})

    def set_env(self, context, req, req_id):
        import json
        context["json"] = json
        self.logger.withFields({"request-id": req_id}).info("Loaded base cloud environment variables.")


class CloudUDFEnvironment(CloudEnvironment):
    def set_env(self, context, req, req_id):
        super().set_env(context, req, req_id)

        exec(req["init_state_fn"], context)
        exec(req["choice_fn"], context)
        exec(req["stop_fn"], context)
        exec(req["postprocessing_fn"], context)
        exec(req["update_fns"], context, globals())
        exec(req["agg_fns"], context, globals())
        update_fn = update_fns()
        agg_fn = agg_fns()
        context["update_fn"] = update_fn
        context["agg_fn"] = agg_fn
        self.logger.withFields({"request-id": req_id}).info("Loaded cloud environment variables for udf function.")
        

class CloudPredefinedEnvironment(CloudEnvironment):
    def set_env(self, context, req, req_id):
        super().set_env(context, req, req_id)
        algo_code = req["algo_code"]
        module = getattr(leap_fn, algo_code)
        
        env_utils.load_fn("init_state_fn", req, context, module=module)
        env_utils.load_fn("choice_fn", req, context, module=module)
        env_utils.load_fn("stop_fn", req, context, module=module)
        env_utils.load_fn("postprocessing_fn", req, context, module=module)

        env_utils.load_from_fn_generator("update_fns", "update_fn", req, context, module=module)
        env_utils.load_from_fn_generator("agg_fns", "agg_fn", req, context, module=module)
        self.logger.withFields({"request-id": req_id}).info("Loaded cloud environment variables for predefined function.")

class CloudFedereatedLearningEnvironment(CloudPredefinedEnvironment):
    def set_env(self, context, req, req_id):
        super().set_env(context, req, req_id)

        ### Function specific imports
        import torch
        globals()["torch"] = torch
        context["torch"] = torch
        context["AverageMeter"] = leap_fn.fl_fn.AverageMeter
        hyperparams = json.loads(req["hyperparams"])
        context["hyperparams"] = hyperparams

        # pass in context as second argument so that get_model has access to context variables
        env_utils.load_from_fn_generator("get_model", "model", req, context, gen_fn_args=[hyperparams])
        params = context["model"].parameters()
        env_utils.load_from_fn_generator("get_optimizer", "optimizer", req, context, gen_fn_args=[params, hyperparams])
        env_utils.load_from_fn_generator("get_criterion", "criterion", req, context, gen_fn_args=[hyperparams])
        self.logger.withFields({"request-id": req_id}).info("Loaded cloud environment variables for federated learning.")


        
