# This file contains the code for loading variables and functions
# into the appropriate context.

import pdb
import logging
from pylogrus import PyLogrus, TextFormatter
import json
from cloudalgo.functions import *
import cloudalgo.functions as leap_fn
import utils.env_utils as env_utils

# Setup logging tool
logging.setLoggerClass(PyLogrus)
logger = logging.getLogger(__name__)  # type: PyLogrus
logger.setLevel(logging.DEBUG)
formatter = TextFormatter(datefmt='Z', colorize=True)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


# Base environment class. The environment class loads the
# appropriate imports, state, function and variables. This
# allows the functions, state, and imports to be accessed
# inside the process dealing with the requests from a client.
class Environment:
    pass


# Environment class for a site. Loads the imports, state and
# functions that run inside a site.
class SiteEnvironment(Environment):

    def __init__(self):
        self.logger = logger.withFields({"node": "site-algo"})

    # Loads the general imports that every site needs.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        import random
        context["random"] = random
        import numpy as np
        context["np"] = np
        import pandas as pd
        context["pd"] = pd
        self.logger.withFields({"request-id": req_id}).info("Loaded base site environment variables")


# Environment class for user defined functions. Loads the
# imports, state and functions that run in a site.
class SiteUDFEnvironment(SiteEnvironment):

    # Loads the map functions, the choice function, and the
    # dataprep function in a site.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        super().set_env(context, req_body, req_id, req)

        exec(req_body["map_fns"], context, globals())
        context["map_fn"] = map_fns()
        exec(req_body["choice_fn"], context)
        exec(req_body["dataprep_fn"], context)

        self.logger.withFields({"request-id": req_id}).info("Loaded site environment variables for udf function.")


# Loads the appropriate variables and functions for running
# a differentially private computation in a site using the
# exponential mechanism.
class SiteExponentialUDFEnvironment(SiteUDFEnvironment):

    # Loads the score functions, choice function and dataprep
    # function, along with the functions loaded by SiteUDFEn-
    # vironment, into the appropriate context.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        super(SiteUDFEnvironment, self).set_env(context, req_body, req_id, req)

        exec(req_body["score_fns"], context, globals())
        context["score_fn"] = score_fns()
        exec(req_body["choice_fn"], context)
        exec(req_body["dataprep_fn"], context)

        self.logger.withFields({"request-id": req_id}).info("Loaded site environment variables for udf function.")


# Environment class for loading the appropriate variables
# and functions for running a predefined algorithm in a site.
class SitePredefinedEnvironment(SiteEnvironment):

    # Loads the choice, dataprep, and algo code, along with the
    # functions loaded by SiteEnvironment, into the appropriate
    # context.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        super().set_env(context, req_body, req_id, req)
        algo_code = req.algo_code
        module = getattr(leap_fn, env_utils.convert_algo_code(algo_code))

        env_utils.load_fn("choice_fn", req_body, context, module=module)
        env_utils.load_fn("dataprep_fn", req_body, context, module=module)
        env_utils.load_from_fn_generator("map_fns", "map_fn", req_body, context, module=module)
        
        self.logger.withFields({"request-id": req_id}).info("Loaded site environment variables for predefined function.")

# Environment class for loading the appropriate variables
# and functions for running differentially private algorithms
# in a site.
class SitePrivatePredefinedEnvironment(SitePredefinedEnvironment):

    # Loads the epsilon and delta values, along with the
    # parameters defined by the SitePredefinedEnvironment,
    # into the appropriate context.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        import cloudalgo.functions.privacy as leap_privacy
        context["leap_privacy"] = leap_privacy
        epsilon = req_body["epsilon"]
        delta = req_body["delta"]
        privacy_params = {
            "epsilon": epsilon,
            "delta": delta
        }
        context["privacy_params"] = privacy_params
        super().set_env(context, req_body, req_id, req)


# Environment class for loading the appropriate variables and functions
# for running federated learning in a site.
class SiteFederatedLearningEnvironment(SitePredefinedEnvironment):

    # Loads the model, optimizer and criterion into the context.
    # Also imports the necessary libraries for federated
    # learning.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        algo_code = req.algo_code
        module = getattr(leap_fn, env_utils.convert_algo_code(algo_code))

        import torch
        globals()["torch"] = torch
        context["torch"] = torch
        import pandas as pd
        context["pd"] = pd        
        context["AverageMeter"] = leap_fn.fl_fn.AverageMeter

        import torchvision
        context["torchvision"] = torchvision
        import requests
        context["requests"] = requests
        import io
        context["io"] = io
        from PIL import Image
        context["Image"] = Image
        import os
        context["os"] = os

        hyperparams = json.loads(req_body["hyperparams"])
        context["hyperparams"] = hyperparams

        env_utils.load_fn("get_dataloader", req_body, context)
        env_utils.load_from_fn_generator("get_model", "model", req_body, context, gen_fn_args=[hyperparams])
        params = context["model"].parameters()
        env_utils.load_from_fn_generator("get_optimizer", "optimizer", req_body, context, gen_fn_args=[params, hyperparams])
        env_utils.load_from_fn_generator("get_criterion", "criterion", req_body, context, gen_fn_args=[hyperparams])

        super().set_env(context, req_body, req_id, req)
        self.logger.withFields({"request-id": req_id}).info("Loaded site environment variables for federated learning.")


# Environment class for the cloud. Loads the libraries, functions,
# and variables that run in the cloud.
class CloudEnvironment(Environment):

    def __init__(self):
        self.logger = logger.withFields({"node": "cloud-algo"})

    # Imports the libraries necessary to run algorithms in the
    # cloud.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        import random
        context["random"] = random
        import json
        context["json"] = json
        import numpy as np
        context["np"] = np
        import pandas as pd
        context["pd"] = pd
        self.logger.withFields({"request-id": req_id}).info("Loaded base cloud environment variables.")


# Extends the cloud environment and loads the appropriate
# parameters for running user defined algorithms in the cloud.
class CloudUDFEnvironment(CloudEnvironment):

    # Loads the choice, stop, post-
    # processing, update and aggregate functions from a user into
    # the appropriate context in the cloud.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        super().set_env(context, req_body, req_id, req)

        exec(req_body["init_state_fn"], context)
        exec(req_body["choice_fn"], context)
        exec(req_body["stop_fn"], context)
        exec(req_body["postprocessing_fn"], context)
        exec(req_body["update_fns"], context, globals())
        exec(req_body["agg_fns"], context, globals())
        update_fn = update_fns()
        agg_fn = agg_fns()
        context["update_fn"] = update_fn
        context["agg_fn"] = agg_fn
        self.logger.withFields({"request-id": req_id}).info("Loaded cloud environment variables for udf function.")
    

# Extends the cloud environment and loads the appropriate
# parameters for running user predefined algorithms in the
# cloud.
class CloudPredefinedEnvironment(CloudEnvironment):

    # Loads the choice, stop, post-
    # processing, update and aggregate functions from a
    # predefined library into the appropriate context in
    # the cloud.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        super().set_env(context, req_body, req_id, req)

        algo_code = req.algo_code
        module = getattr(leap_fn, env_utils.convert_algo_code(algo_code))

        env_utils.load_fn("init_state_fn", req_body, context, module=module)
        env_utils.load_fn("choice_fn", req_body, context, module=module)
        env_utils.load_fn("stop_fn", req_body, context, module=module)
        env_utils.load_fn("postprocessing_fn", req_body, context, module=module)

        env_utils.load_from_fn_generator("update_fns", "update_fn", req_body, context, module=module)
        env_utils.load_from_fn_generator("agg_fns", "agg_fn", req_body, context, module=module)
        self.logger.withFields({"request-id": req_id}).info("Loaded cloud environment variables for predefined function.")


# Extends the cloud predefined environment and loads the
# appropriate parameters for running private predefined
# algorithms.
class CloudPrivatePredefinedEnvironment(CloudPredefinedEnvironment):

    # Loads the epsilon and the delta into the appropriate
    # context for the cloud.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        import cloudalgo.functions.privacy as leap_privacy
        context["leap_privacy"] = leap_privacy

        epsilon = req_body["epsilon"]
        delta = req_body["delta"]
        privacy_params = {
            "epsilon": epsilon,
            "delta": delta
        }

        context["privacy_params"] = privacy_params
        super().set_env(context, req_body, req_id, req)


# Extends the CloudPredefinedEnvironment but also loads the
# the parameters necessary to run a federated learning algorithm
# in the cloud.
class CloudFedereatedLearningEnvironment(CloudPredefinedEnvironment):

    # Loads the optimizer, model, criterion and imports Pytorch
    # into the appropriate context in the cloud.
    #
    # context: The context where the imports are loaded to.
    # req: The request containing the functions to be loaded.
    # req_id: The id of this request. Used for logging.
    def set_env(self, context, req_body, req_id, req):
        super().set_env(context, req_body, req_id, req)
        import torch
        globals()["torch"] = torch
        context["torch"] = torch
        context["AverageMeter"] = leap_fn.fl_fn.AverageMeter
        hyperparams = json.loads(req_body["hyperparams"])
        context["hyperparams"] = hyperparams

        import torchvision
        context["torchvision"] = torchvision
        import requests
        context["requests"] = requests
        import io
        context["io"] = io
        from PIL import Image
        context["Image"] = Image
        import os
        context["os"] = os
        
        # pass in context as second argument so that get_model has access to context variables
        env_utils.load_from_fn_generator("get_model", "model", req_body, context, gen_fn_args=[hyperparams])
        params = context["model"].parameters()
        env_utils.load_fn("get_dataloader", req_body, context)
        env_utils.load_from_fn_generator("get_optimizer", "optimizer", req_body, context, gen_fn_args=[params, hyperparams])
        env_utils.load_from_fn_generator("get_criterion", "criterion", req_body, context, gen_fn_args=[hyperparams])
        self.logger.withFields({"request-id": req_id}).info("Loaded cloud environment variables for federated learning.")
