import pdb
import json
import inspect
import numpy as np

# Sum a particular column
def map_fn1(data, state):
    col = data[state["col"]]
    result = {
        "quantile": col.quantile(state["quantile"])
    }
    return json.dumps(result)

map_fn = [map_fn1]

def agg_fn1(map_results):
    r = [] 
    for result in map_results:
        result = json.loads(result)
        r.append(result["quantile"])
    return r

agg_fn = [agg_fn1]

# Returns which map/agg fn to run
def choice_fn(state):
    return 0

def update_fn1(agg_result, state):
    state["i"] += 1
    return state

update_fn = [update_fn1]

def stop_fn(agg_result, state):
    return state["i"] == 1

def post_fn(agg_result, state):
    return agg_result

state = {
    "i": 0,
    "col":"age",
    "quantile":0
}