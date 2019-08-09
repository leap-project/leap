import pdb 
import pandas as pd
import json
import numpy as np

from SiteAlgo.site_algo import SiteAlgoServicer
class SiteResponse():
    def __init__(self):
        self.response = None

class LocalSiteAlgoServicer(SiteAlgoServicer):
    def __init__(self, site_id):
        self.live_requests = {}
        self.site_id = site_id

    def _get_response_obj(self):
        return SiteResponse()

    # def _load_data(self, data_id):
    #     if data_id == 0:
    #         data = np.load("data/randdata.npy")
    #     if data_id > 0:
    #         data = pd.read_csv("data/data{}.csv".format(data_id), delimiter=", ")
    #     return data
    
    

if __name__=="__main__":
    pdb.set_trace()