# The laplace and exponential mechanisms to add noise to outputs
# in Leap.

import json
import numpy as np
import pandas as pd 

""" Returns differentially private result through the laplace mechanism
Adds noise from laplace distribution to result such that result is epsilon, delta dp
"""
def laplace(result, epsilon, delta, sensitivity):
    if delta == 0:
        noise = np.random.laplace(loc = 0, scale = sensitivity/float(epsilon), size = (1,1))
    else:    
        sigma = (sensitivity/(epsilon))*np.sqrt(2*np.log(1.25/delta))
        noise = np.random.normal(0.0, sigma, 1)

    return result + noise

""" Dynamically computes sensitivity for a given map function
TODO: Note that sensitivity is computed on filtered dataset instead of entire dataset
"""
def dynamic_laplace(epsilon, delta, target_attribute, map_fn, D, state):
    sensitivity = -1
    D_result = map_fn(D, state)[target_attribute]
    for i,y in enumerate(D):
        # For every (n-1)subset dataset
        D_prime = D[:i] + D[i+1:]
        D_prime_result = map_fn(D_prime, state)[target_attribute]
        candidate_sensitvity = abs(D_result - D_prime_result)
        if candidate_sensitvity > sensitivity: 
            sensitivity = candidate_sensitvity
    
    private_result = laplace(D_result, epsilon, delta, sensitivity).item()
    result = {}
    result[target_attribute] = private_result
    return json.dumps(result)

""" Returns differentially private result through the exponential mechanism
http://dimacs.rutgers.edu/~graham/pubs/slides/privdb-tutorial.pdf
https://www.cis.upenn.edu/~aaroth/courses/slides/Lecture3.pdf

epsilon, delta: sampled output is epsilon delta differentially private
D: Dataset
out_range: candidate output values to sample from
score_fn(Dataset, output): returns how good output is for Dataset
sensitivity:    sensitivity of the score function for dataset D
TODO: Note that sensitivity is computed on filtered dataset instead of entire dataset
"""
def exponential(epsilon, delta, target_attribute, score_fn, D, state, sensitivity=None):
    col = D[state["col"]]
    # TODO: Think about if other output ranges are possible and how to define it in api
    out_range = col

    sample_pr = np.zeros(len(out_range))
    # Expensive computation of the sensitivity
    if sensitivity is None:
        sensitivity = -1
        for i,row in enumerate(D):
            D_prime = pd.concat([D[:i], D[i+1:]])
            # Iterate only out range that is not removed
            for y in pd.concat([out_range[:i], out_range[i+1:]]):
                q_d = score_fn(D, state, y)
                q_d_prime = score_fn(D_prime, state, y)
                candidate_sensitvity = abs(q_d - q_d_prime)
                if candidate_sensitvity > sensitivity: 
                    sensitivity = candidate_sensitvity

    for i,y in enumerate(out_range):
        sample_pr[i] = np.exp(epsilon*score_fn(D, state, y) / (2*sensitivity))
    sample_pr = sample_pr / sample_pr.sum()
    
    sample = np.random.choice(out_range, 1, p=sample_pr).item()
    result = {}
    result[target_attribute] = sample
    return json.dumps(result)
