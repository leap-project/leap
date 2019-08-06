import pdb
import json
import inspect

# Sum a particular column
def map_fn1(data, state):
    result = {
        "count": len(data)
    }
    return json.dumps(result)

map_fn = [map_fn1]

def agg_fn1(map_results):
    s = 0   
    for result in map_results:
        result = json.loads(result)
        s += result["count"]       
    return s

agg_fn = [agg_fn1]

# Returns which map/agg fn to run
def choice_fn(site_state):
    return 0

def update_fn1(agg_result, state):
    state["i"] += 1
    return state

update_fn = [update_fn1]

def dataprep_fn(data):
    return data

def stop_fn(agg_result, state):
    return state["i"] == 1

def postprocessing_fn(agg_result, state):
    return agg_result

def init_state_fn():
    state = {
        "i": 0,
    }
    return state


