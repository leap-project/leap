# A file with a few examples on how to write a Leap program.

import sys
sys.path.append("../")
import api.codes as codes
import api.leap as leap
import api.leap_fn as leap_fn
import cloudalgo.functions as cloud_functions
import api.local.functions as leap_functions
import api.register.user.registration as user_reg

from proto import computation_msgs_pb2
from api.local.cloud import LocalCloudAlgoServicer
from api.local.localsite import LocalSiteAlgoServicer
from api.local.coordinator import LocalCoordinator


def predef_count_exp():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.COUNT_ALGO)
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef.selector = selector
    return leap_predef

def predef_private_site_count_exp():
    leap_predef = leap_fn.PrivatePredefinedFunction(computation_msgs_pb2.AlgoCodes.PRIVATE_SITE_COUNT_ALGO, epsilon=1, delta=0)
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef.selector = selector
    return leap_predef

def predef_private_cloud_count_exp():
    leap_predef = leap_fn.PrivatePredefinedFunction(computation_msgs_pb2.AlgoCodes.PRIVATE_CLOUD_COUNT_ALGO, epsilon=1, delta=0)
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef.selector = selector
    return leap_predef

def udf_private_count_exp():
    epsilon = 1
    delta = 0
    target_attribute = "count"
    leap_udf = leap_fn.PrivateLaplaceUDF(epsilon, delta, target_attribute)
    module = cloud_functions.count_fn_udf
    leap_udf.map_fns = module.map_fns
    leap_udf.update_fns = module.update_fns
    leap_udf.agg_fns = module.agg_fns
    leap_udf.choice_fn = module.choice_fn
    leap_udf.stop_fn = module.stop_fn
    leap_udf.dataprep_fn = module.dataprep_fn
    leap_udf.postprocessing_fn = module.postprocessing_fn
    leap_udf.init_state_fn = module.init_state_fn

    selector = "[age] > 50 and [bmi] < 25"
    leap_udf.selector = selector
    return leap_udf 

def udf_private_quantile_exp():
    epsilon = 1
    delta = 0
    target_attribute = "quantile"
    leap_udf = leap_fn.PrivateExponentialUDF(epsilon, delta, target_attribute)
    module = cloud_functions.quantile_fn_site_dp
    leap_udf.score_fns = module.score_fns
    leap_udf.update_fns = module.update_fns
    leap_udf.agg_fns = module.agg_fns
    leap_udf.choice_fn = module.choice_fn
    leap_udf.stop_fn = module.stop_fn
    leap_udf.dataprep_fn = module.dataprep_fn
    leap_udf.postprocessing_fn = module.postprocessing_fn
    leap_udf.init_state_fn = module.init_state_fn

    # selector = "[age] > 50 and [bmi] < 25"
    selector = ""
    leap_udf.selector = selector
    return leap_udf 

def udf_count_exp():
    leap_udf = leap_fn.UDF()
    module = cloud_functions.count_fn
    leap_udf.map_fns = module.map_fns
    leap_udf.update_fns = module.update_fns
    leap_udf.agg_fns = module.agg_fns
    leap_udf.choice_fn = module.choice_fn
    leap_udf.stop_fn = module.stop_fn
    leap_udf.dataprep_fn = module.dataprep_fn
    leap_udf.postprocessing_fn = module.postprocessing_fn
    leap_udf.init_state_fn = module.init_state_fn

    selector = "[age] > 50 and [bmi] < 25"
    leap_udf.selector = selector
    return leap_udf

def quantile_exp():
    leap_predef = leap_fn.PredefinedFunction(computation_msgs_pb2.AlgoCodes.QUANTILE_ALGO)
    selector = ""
    leap_predef.selector = selector
    return leap_predef

def fed_learn_exp():
    module = leap_functions.fl_fn
    selector = {
        "type": codes.DEFAULT,
        "useLocalData": True
    }
    leap_fed_learn = leap_fn.FedLearnFunction()
    leap_fed_learn.selector = selector
    leap_fed_learn.get_model = module.get_model
    leap_fed_learn.get_optimizer = module.get_optimizer
    leap_fed_learn.get_criterion = module.get_criterion
    leap_fed_learn.get_dataloader = module.get_dataloader
    hyperparams = {
        "lr": 1e-5,
        "d_x": 2, # input dimension
        "d_y": 1, # output dimension
        "batch_size": 1,
        "max_iters": 7,
        "iters_per_epoch":1
    }
    leap_fed_learn.hyperparams = hyperparams
    return leap_fed_learn

def distributed(sites, auth_token):
    leap_exp_fn = fed_learn_exp()
    dist_leap = leap.DistributedLeap(leap_exp_fn, "127.0.0.1:50000", auth_token)
    print(dist_leap.get_result(sites))

def local():
    sites = []
    sites.append(LocalSiteAlgoServicer(0))    
    coordinator = LocalCoordinator(sites)
    cloud = LocalCloudAlgoServicer(coordinator)

    leap_exp_fn = udf_private_quantile_exp()
    local_leap = leap.LocalLeap(leap_exp_fn, cloud)
    print(local_leap.get_result())


if __name__ == "__main__":
    #local()
    #user_reg.register_user("TestUser", "123456", "127.0.0.1:50000")
    auth_res = user_reg.authenticate_user("TestUser", "123456", "127.0.0.1:50000")
    distributed([1], auth_res.token)
