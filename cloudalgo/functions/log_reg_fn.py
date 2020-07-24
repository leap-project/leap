# An algorithm to perform simple logistic regression 
# with gradient descent

import json
import numpy as np
import random

def map_fns():
    # Sum a particular column
    def map_fn1(data, state):
        y = data[state["targetCol"]]
        X = data.drop(columns=[state["targetCol"]])
        n_samples, n_features = X.shape
        if (state["i"] == 0):
            # Set initial weights and biases
            print("setting initial values")
            state["weights"] = np.zeros(n_features)
        weights_loc = state["weights"]
        bias_loc = state["bias"]
        dw_loc_list = []
        db_loc_list = []
        for i in range(state["sub_i"]):
            # approximate y with linear combination of weights and x, plus bias
            linear_model = np.dot(X, weights_loc) + bias_loc
            # apply sigmoid function
            y_predicted = 1 / (1 + np.exp(-linear_model))
            # compute gradients
            dw_loc = np.dot(X.T, (y_predicted - y))
            db_loc = np.sum(y_predicted - y)
            # push dw_loc and db_loc into an array:
            # dw_loc_list.append(dw_loc)
            # db_loc_list.append(db_loc)
            # update weights and biases
            weights_loc -= state["lr"]*np.array((1/n_samples)*dw_loc)
            bias_loc -= state["lr"]*(1/n_samples)*db_loc

        # dw_loc_avg = np.sum(dw_loc_list)/len(dw_loc_list)
        # db_loc_avg = np.sum(db_loc_list)/len(db_loc_list)
        result = {
            "features": n_features,
            "count": n_samples,
            "w_loc": weights_loc.tolist(),
            "b_loc": bias_loc.tolist()
        }
        return json.dumps(result)
        
    return [map_fn1]

def agg_fns():
    def agg_fn1(map_results):
        ret = {
            "map_results": map_results
        }
        return json.dumps(ret)
   
    return [agg_fn1]

def update_fns():
    def update_fn1(agg_result, state):
        agg_result = json.loads(agg_result)
        map_results = agg_result["map_results"]
        # pick C sites at random
        C = state["C"]
        c_results = random.sample(map_results, C)
        # sum up the number of items in the C sites
        total_count = 0
        for result in c_results:
            result = json.loads(result)
            total_count += result["count"]
        # Get weighted weights and biases
        w_global = np.zeros(1)
        b_global = 0
        for result in c_results:
            result = json.loads(result)
            w_loc = np.array(result["w_loc"])
            b_loc = np.float64(result["b_loc"])
            if (w_global.size != result["features"]):
                w_global = np.zeros(result["features"])
            weight = result["count"]/total_count
            w_global = np.add(w_global, weight*w_loc)
            b_global = np.add(b_global, weight*b_loc)

        state["weights"] = w_global.tolist()
        state["bias"] = b_global.tolist()
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
    return {
        "weights": state["weights"],
        "bias": state["bias"]
    }

def init_state_fn():
    state = {
        "i": 0,
        "weights": [],
        "bias": 0,
        "lr": 0.001,
        "iter": 100,
        "targetCol": "osi",
        "sub_i": 100,
        "C": 1
    }
    return state