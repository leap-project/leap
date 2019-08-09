import pdb
import json
import inspect
import numpy as np

# Sum a particular column

def map_fns():


    def map_fn1(data, state):
        COUNT_SENSITIVITY = 1
        epsilon = privacy_params["epsilon"]
        delta = privacy_params["delta"]

        count = len(data)
        count = leap_privacy.laplace(count, epsilon, delta, COUNT_SENSITIVITY).item()
        
        # if delta == 0:
        #     noise = np.random.laplace(loc = 0, scale = COUNT_SENSITIVITY/float(epsilon), size = (1,1))
        # else:
        #     sigma = (COUNT_SENSITIVITY/(epsilon))*np.sqrt(2*np.log(1.25/delta))
        #     noise = np.random.normal(0.0, sigma, 1)

        # count = len(data) + noise.item()

        result = {
            "count": count
        }
        return json.dumps(result)

    return [map_fn1]

def agg_fns():

    def agg_fn1(map_results):
        s = 0
        for result in map_results:
            result = json.loads(result)
            s += result["count"]
        return s
    return [agg_fn1]

def update_fns():

    def update_fn1(agg_result, state):
        state["i"] += 1
        return state

    return [update_fn1]

# Returns which map/agg fn to run
def choice_fn(state):
    return 0

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