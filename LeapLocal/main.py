import sys
sys.path.append("../")

from cloud import LocalCloudAlgoServicer
from localsite import LocalSiteAlgoServicer
from coordinator import LocalCoordinator
import LeapApi.leap as leap
import LeapApi.leap_fn as leap_fn

import textwrap
import pdb
import inspect

import LeapLocal.functions as functions



def predefined_count_exp(cloud):
    selector = "[age] > 50 and [bmi] < 25"
    leap_predef = leap_fn.PredefinedFunction(leap.codes.COUNT_ALGO)
    leap_predef.selector = selector
    local_leap = leap.LocalLeap(leap_predef, cloud)
    module = functions.count_fn
    local_leap.send_request()

def udf_count_exp(cloud):
    selector = "[age] > 50 and [bmi] < 25"
    leap_udf = leap_fn.UDF()
    leap_udf.selector = selector
    module = functions.count_fn
    leap_udf.map_fns = module.map_fns
    leap_udf.update_fns = module.update_fns
    leap_udf.agg_fns = module.agg_fns
    leap_udf.choice_fn = module.choice_fn
    leap_udf.stop_fn = module.stop_fn
    leap_udf.dataprep_fn = module.dataprep_fn
    leap_udf.postprocessing_fn = module.postprocessing_fn
    leap_udf.init_state_fn = module.init_state_fn
    
    local_leap = leap.LocalLeap(leap_udf, cloud)
    module = functions.count_fn
    local_leap.send_request()


if __name__=="__main__":  
    sites = []
    sites.append(LocalSiteAlgoServicer(0))
    
    coordinator = LocalCoordinator(sites)

    cloud = LocalCloudAlgoServicer(coordinator)

    udf_count_exp(cloud)
    pdb.set_trace()
    