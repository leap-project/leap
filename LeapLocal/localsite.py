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
        
        # data = self._load_data(data_id)
        data = [{'record_id': '30', 'patient_id': '30', 'age': '52.10033695', 'bmi': '23.0220392', 'date_dx': '2012-04-15', 'stage': 'III', 'grade': '4', 'nodes': '1', 'feel': 'Strongly Disagree', 'alive': 'TRUE', 'comment': 'touch'}, {'record_id': '85', 'patient_id': '85', 'age': '50.67954949', 'bmi': '23.13432404', 'date_dx': '2010-01-18', 'stage': 'I', 'grade': '2', 'nodes': '0', 'feel': 'Disagree', 'alive': 'FALSE', 'comment': 'increase'}, {'record_id': '93', 'patient_id': '93', 'age': '55.11974411', 'bmi': '21.18744011', 'date_dx': '2003-07-21', 'stage': 'V', 'grade': '4', 'nodes': '1', 'feel': 'Agree', 'alive': 'TRUE', 'comment': 'lead'}, {'record_id': '94', 'patient_id': '94', 'age': '50.46660426', 'bmi': '23.67997552', 'date_dx': '2005-06-10', 'stage': 'V', 'grade': '4', 'nodes': '0', 'feel': 'Strongly Agree', 'alive': 'FALSE', 'comment': 'big'}]

        choice = choice_fn(state)

        if 'data_prep' in globals():
            data = data_prep(data)
            
        map_result = map_fn[choice](data, state)
        # print("map_result: {}".format(map_result))
        return map_result


    def _load_data(self, data_id):
        if data_id == 0:
            data = np.load("data/randdata.npy")
        if data_id > 0:
            data = pd.read_csv("data/data{}.csv".format(data_id), delimiter=", ")
        return data
    
    

if __name__=="__main__":
    pdb.set_trace()