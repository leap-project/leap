# An algorithm that gets the max of a column from the data returned
# form the selector.

import json
import numpy as np

def map_fns():
    # Sum a particular column
    def map_fn1(data, state):
        result = {
            "max": int(data.iloc[0][0])
        }
        return json.dumps(result)
    return [map_fn1]

def agg_fns():
    def agg_fn1(map_results):
        s = 0  
        for result in map_results:
            result = json.loads(result)
            if (result["max"] > s):
                s = result["max"]    
        return s
   
    return [agg_fn1]

def update_fns():
    def update_fn1(agg_result, state):
        state["i"] += 1
        return state
    return [update_fn1]

# Returns which map/agg fn to run
def choice_fn(site_state):
    return 0

def dataprep_fn(data):
    return data

def stop_fn(agg_result, state):
    return state["i"] == 1

def postprocessing_fn(agg_result, state):
    return agg_result

def init_state_fn():
    state = {
        "i": 0
    }
    return state


