import pdb
import json
import inspect
import pandas as pd

# Sum a particular column
def map_fn1(data, site_state):
    data = pd.DataFrame(data)
    result = {
        "sum": data[site_state["col"]].astype('float').sum(),
        "count": len(data)
    }
    return json.dumps(result)

# Compute variance given mean in site_state
def map_fn2(data, site_state):
    data = pd.DataFrame(data)
    mean = site_state["mean"]
    col = data[state["col"]].astype('float')
    result = {
        "ss": ((col - mean)**2).sum(),
        "count": len(data)
    }
    return json.dumps(result)
map_fn = [map_fn1, map_fn2]

def agg_fn1(map_results):
    s = 0
    c = 0.0
    for result in map_results:
        result = json.loads(result)
        s += result["sum"]
        c += result["count"]
    return s/c

def agg_fn2(map_results):
    ss = 0
    c = 0.0
    for result in map_results:
        result = json.loads(result)
        ss += result["ss"]
        c += result["count"]
    return ss/c
agg_fn = [agg_fn1, agg_fn2]

# Returns which map/agg fn to run
def choice_fn(site_state):
    return site_state["i"] % 2

def update_fn1(agg_result, site_state):
    site_state["i"] += 1
    site_state["mean"] = agg_result
    return site_state
def update_fn2(agg_result, site_state):
    site_state["i"] += 1
    return site_state

update_fn = [update_fn1, update_fn2]

def stop_fn(agg_result, site_state):
    return site_state["i"] == 2

def post_fn(agg_result, site_state):
    return agg_result

site_state = {
    "i": 0,
    "col":"age"
}