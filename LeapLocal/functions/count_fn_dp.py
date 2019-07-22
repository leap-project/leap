import pdb
import json
import inspect
import numpy as np

# Sum a particular column
def map_fn1(data, state):
    print(data)
    COUNT_SENSITIVITY = 1
    epsilon = state["epsilon"]
    delta = state["delta"]


    if delta == 0:
        noise = np.random.laplace(loc = 0, scale = COUNT_SENSITIVITY/float(epsilon), size = (1,1))
    else:    
        sigma = (COUNT_SENSITIVITY/(epsilon))*np.sqrt(2*np.log(1.25/delta))
        noise = np.random.normal(0.0, sigma, 1)

    count = len(data) + noise.item()
    result = {
        "count": count
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
    "epsilon":1,
    "delta":0.1
}