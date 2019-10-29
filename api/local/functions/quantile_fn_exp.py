import pdb
import json
import inspect
import numpy as np

# Exponential mechanism as described in:
# http://dimacs.rutgers.edu/~graham/pubs/slides/privdb-tutorial.pdf
# https://www.cis.upenn.edu/~aaroth/courses/slides/Lecture3.pdf
# TODO: Not sure how to handle medians of even numbered lists
def map_fn1(data, state):
    col = data[state["col"]]
    O = col.as_matrix()
    O.sort()
    def score(o, O):
        rank = np.where(O == o)[0].max()
        target = len(O)*state["quantile"] # Hard coded for median
        return -abs(rank - target)
    epsilon = state["epsilon"]
    

    sample_pr = np.zeros(len(O))
    for i,o in enumerate(O):
        sample_pr[i] = np.exp(epsilon*score(o,O))
    sample_pr = sample_pr / sample_pr.sum()
    
    sample = np.random.choice(O, 1, p=sample_pr).item()

    result = {
        "quantile": sample
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
    "epsilon":1,
    "quantile":0.5
}