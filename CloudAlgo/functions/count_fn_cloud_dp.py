# An algorithm that counts the number of elements returned
# from the database and makes the output differentially private
# in the cloud.

import json


def map_fns():


    def map_fn1(data, state):
        COUNT_SENSITIVITY = 1
        epsilon = privacy_params["epsilon"]
        delta = privacy_params["delta"]

        count = len(data)

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
    COUNT_SENSITIVITY = 1
    epsilon = privacy_params["epsilon"]
    delta = privacy_params["delta"]
    private_agg_result = leap_privacy.laplace(agg_result, epsilon, delta, COUNT_SENSITIVITY).item()
    
    return private_agg_result

def init_state_fn():
    state = {
        "i": 0,
    }
    return state