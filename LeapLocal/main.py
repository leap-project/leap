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

# def count_exp_dp(client):
#     client.send_request(inspect.getsource(functions.count_fn_dp))

# def sum_exp(client):
#     client.send_request(inspect.getsource(functions.sum_fn))

# def mean_exp(client):    
#     client.send_request(inspect.getsource(functions.mean_fn))

# def var_exp(client):
#     client.send_request(inspect.getsource(functions.var_fn))

# def quantile_exp(client):
#     client.send_request(inspect.getsource(functions.quantile_fn))

# def quantile_exp_dp(client):
#     client.send_request(inspect.getsource(functions.quantile_fn_exp))

# def fl_exp(client):
#     client.send_request(inspect.getsource(functions.fl_fn))

if __name__=="__main__":  
    sites = []
    sites.append(LocalSiteAlgoServicer(0))
    
    coordinator = LocalCoordinator(sites)

    cloud = LocalCloudAlgoServicer(coordinator)

    predefined_count_exp(cloud)
    pdb.set_trace()
    