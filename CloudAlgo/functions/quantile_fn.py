# Algorithm that returns the quantiles for the data on each site
# in Leap.

import json
import numpy as np

def map_fns():
    # Sum a particular column
    def map_fn1(data, state):
        col = data[state["col"]].values.astype('float')
        result = {
            "quantile": np.quantile(col, state["quantile"])
        }
        return json.dumps(result)
    return [map_fn1]

def agg_fns():
    def agg_fn1(map_results):
        r = [] 
        for result in map_results:
            result = json.loads(result)
            r.append(result["quantile"])
        return r
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
    return pd.DataFrame(data)
    
def stop_fn(agg_result, state):
    return state["i"] == 1

def postprocessing_fn(agg_result, state):
    return agg_result

def init_state_fn():
    state = {
        "i": 0,
        "col": "age",
        "quantile": .5
    }
    return state

