import pdb
import json

# Welford's algorithm to compute variance of a particular column
def map_fn(data, state):
    state = json.loads(state)
    samples = data[state["col"]]
    M = state["M"]
    S = state["S"]
    k = state["k"]
    for i in range(len(data)):
        x = samples[i]
        k = k+1
        oldM = M
        M = M + (x - M)/k
        S = S + (x - M)*(x - oldM)
    return M, S, k
    
# TODO
def agg_fn(map_results):
    s = 0
    c = 0.0
    for result in map_results:
        result = json.loads(result)
        s += result["sum"]
        c += result["count"]
    return s/c

update_fn = None

stop_fn = None

post_fn = None

state = {
    "i": 0,
    "col":"age",
    "M":0,
    "S":0,
    "k":0
}