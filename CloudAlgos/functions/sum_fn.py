import pdb
import json
import inspect
import pandas as pd

# Sum a particular column
def map_fn1(data, site_state):
    data = pd.DataFrame(data)
    result = {
        "sum": data[site_state["col"]].astype('float').sum()
    }
    return json.dumps(result)

map_fn = [map_fn1]

def agg_fn1(map_results):
    s = 0   
    for result in map_results:
        result = json.loads(result)
        s += result["sum"]       
    return s

agg_fn = [agg_fn1]

# Returns which map/agg fn to run
def choice_fn(site_state):
    return 0

def update_fn1(agg_result, site_state):
    site_state["i"] += 1
    return site_state

update_fn = [update_fn1]

def stop_fn(agg_result, site_state):
    return site_state["i"] == 1

def post_fn(agg_result, site_state):
    return agg_result

site_state = {
    "i": 0,
    "col": "age"
}