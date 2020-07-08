# An algorithm to perform simple logistic regression 
# with gradient descent

import json
import numpy as np

def map_fns():
    # Sum a particular column
    def map_fn1(data, state):
        y = data[state["targetCol"]]
        X = data.drop[state["targetCol"]]
        if (state["i"] == 0):
            # Set initial weights and biases
            n_samples, n_features = X.shape
            state["weights"] = np.zeros(n_features)
        
        # approximate y with linear combination of weights and x, plus bias
        linear_model = np.dot(X, state["weights"]) + state["bias"]
        # apply sigmoid function
        y_predicted = 1 / (1 + np.exp(-linear_model))
        # compute gradients
        dw_loc = np.dot(X.T, (y_predicted - y))
        db_loc = np.sum(y_predicted - y)

        result = {
            "count": n_samples,
            "dw_loc": dw_loc,
            "db_loc": db_loc
        }
        return json.dumps(result)
    return [map_fn1]

def agg_fns():
    def agg_fn1(map_results):
        s = 0
        dw = np.zeros(1)
        db = 0
        for result in map_results:
            result = json.loads(result)
            if (dw.shape != result["dw_loc"].shape):
                dw.shape = np.zeros(result["dw_loc"].shape)
            dw = np.add(dw, result["dw_loc"])
            db = np.add(db, result["db_loc"])
            s += result["count"] 
        dw = (1/s)*dw
        db = (1/s)*db    
        return json.dumps({
            "dw": dw,
            "db": db,
            "s": s
        })
   
    return [agg_fn1]

def update_fns():
    def update_fn1(agg_result, state):
        result = json.loads(agg_result)
        state["weights"] -= state["lr"]*result["dw"]
        state["bias"] -= state["lr"]*result["db"]
        state["i"] += 1
        return state
    return [update_fn1]

# Returns which map/agg fn to run
def choice_fn(site_state):
    return 0

def dataprep_fn(data):
    return data

def stop_fn(agg_result, state):
    return state["i"] == state["iter"]

def postprocessing_fn(agg_result, state):
    return agg_result

def init_state_fn():
    state = {
        "i": 0,
        "weights": [],
        "bias": 0,
        "lr": 0.1,
        "iter": 100,
        "targetCol": ""
    }
    return state


