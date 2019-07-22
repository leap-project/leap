from client import Client
from cloud import Cloud
from localsite import Site

import textwrap
import pdb
import inspect

import functions.sum_fn 
import functions.mean_fn
import functions.count_fn
import functions.count_fn_dp
import functions.var_fn
import functions.quantile_fn
import functions.quantile_fn_exp
import functions.fl_fn


def count_exp(client):
    client.send_request(inspect.getsource(functions.count_fn))

def count_exp_dp(client):
    client.send_request(inspect.getsource(functions.count_fn_dp))

def sum_exp(client):
    client.send_request(inspect.getsource(functions.sum_fn))

def mean_exp(client):    
    client.send_request(inspect.getsource(functions.mean_fn))

def var_exp(client):
    client.send_request(inspect.getsource(functions.var_fn))

def quantile_exp(client):
    client.send_request(inspect.getsource(functions.quantile_fn))

def quantile_exp_dp(client):
    client.send_request(inspect.getsource(functions.quantile_fn_exp))

def fl_exp(client):
    client.send_request(inspect.getsource(functions.fl_fn))

if __name__=="__main__":  
    sites = []
    sites.append(Site(0))
    
    cloud = Cloud(sites)

    client = Client(cloud)
    
    quantile_exp_dp(client)
    pdb.set_trace()
    