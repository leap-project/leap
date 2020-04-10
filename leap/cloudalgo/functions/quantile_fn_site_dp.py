# Algorithm that returns the quantiles for the data on each site
# in Leap and adds noise using the exponential mechanism.

import json
import numpy as np


# Exponential mechanism as described in:
# http://dimacs.rutgers.edu/~graham/pubs/slides/privdb-tutorial.pdf
# https://www.cis.upenn.edu/~aaroth/courses/slides/Lecture3.pdf
# TODO: Not sure how to handle medians of even numbered lists
def score_fns():
    def score1(data, state, output):
        col = data[state["col"]]
        col = col.values
        col.sort()
        rank = np.where(col == output)[0].max()
        target = len(col)*state["quantile"] 
        return -abs(rank - target)
    return [score1]

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
