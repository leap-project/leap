import pdb 
import pandas as pd
import json
import numpy as np

class Site():
    def __init__(self, site_id):
        self.site_id = site_id

    # Return: f(q(data)) where data corresponds the data for data_id
    # def local_compute(self, f, aux_input, data_preprocess, data_filter, data_id):
    def local_compute(self, req):
        req = json.loads(req)
        exec(req["module"], globals())
        state = json.loads(req["state"])
        q_selector = {}
        data_id = 2
        data_filter = None
        
        data = self._load_data(data_id)

        choice = choice_fn(state)
        
        map_result = map_fn[choice](data, state)
        print("map_result: {}".format(map_result))
        return map_result


    def _load_data(self, data_id):
        if data_id == 0:
            data = np.load("data/randdata.npy")
        if data_id > 0:
            data = pd.read_csv("data/data{}.csv".format(data_id), delimiter=", ")
        return data
    
    

if __name__=="__main__":
    pdb.set_trace()