import sys
sys.path.append("../")

from local_leap import LocalLeap
from cloud import LocalCloudAlgoServicer
from localsite import LocalSiteAlgoServicer
from coordinator import LocalCoordinator
import LeapApi.leap as leap

import textwrap
import pdb
import inspect

import LeapLocal.functions as leap_fn



def predefined_count_exp(client):
    filter = "[age] > 50 and [bmi] < 25"
    leap_udf = leap.PredefinedFunction(leap.codes.COUNT_ALGO)
    module = leap_fn.count_fn
    local_leap_udf.send_request(filter)

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
    
    client = LocalLeap(cloud)

    predefined_count_exp(client)
    pdb.set_trace()
    