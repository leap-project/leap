# This is the main API that users interact with LEAP. Users
# will create an instance of the LEAP class and can either
# set their own user defined functions or use one of the func-
# tions available in LEAP

import sys
sys.path.append("../")
import json
import grpc
import ProtoBuf as pb
import LeapApi.codes as codes
import inspect
import pdb
from Utils import leap_utils

# TODO: Deal with imports. Right now, we assume the local sites and cloud have all necessary imports.
class LeapFunction():

    # Constructor that takes in a code representing one of
    # the available algorithms in Leap.
    def __init__(self, is_local=False):
        self.map_fns = None
        self.agg_fns = None
        self.update_fns = None
        self.choice_fn = None
        self.stop_fn = None
        self.dataprep_fn = None
        self.postprocessing_fn = None
        self.init_state_fn = None

class UDF(LeapFunction):
    def __init__(self):
        super().__init__()
    
    def validate(self):
        pass
    
class PredefinedFunction(LeapFunction):
    def __init__(self, algo_code):
        super().__init__()
        self.algo_code = algo_code

    def validate(self):
        pass

    # Takes a json request and adds custom attributes    
    def modify_req(self, filter, req):
        req["algo_code"] = self.algo_code
        req["leap_type"] = codes.PREDEFINED
        return req


# Federated Learning class that extends the main Leap class.
class FedLearnFunction(PredefinedFunction):
    def __init__(self, algo_id):
        super().__init__(algo_id)
        self.optimizer = None
        self.model = None
        self.criterion = None
    
    def validate(self):
        pass
