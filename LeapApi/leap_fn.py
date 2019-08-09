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
    def __init__(self):
        self.map_fns = None
        self.agg_fns = None
        self.update_fns = None
        self.choice_fn = None
        self.stop_fn = None
        self.dataprep_fn = None
        self.postprocessing_fn = None
        self.init_state_fn = None
        self.selector = None
        self.leap_type = None

    def create_request(self):
        req = {}
        map_fns = leap_utils.fn_to_string(self.map_fns)
        agg_fns = leap_utils.fn_to_string(self.agg_fns)
        update_fns = leap_utils.fn_to_string(self.update_fns)
        choice_fn = leap_utils.fn_to_string(self.choice_fn)
        stop_fn = leap_utils.fn_to_string(self.stop_fn)
        dataprep_fn = leap_utils.fn_to_string(self.dataprep_fn)
        postprocessing_fn = leap_utils.fn_to_string(self.postprocessing_fn)
        init_state_fn = leap_utils.fn_to_string(self.init_state_fn)

        req["map_fns"] = map_fns
        req["agg_fns"] = agg_fns
        req["update_fns"] = update_fns
        req["choice_fn"] = choice_fn
        req["stop_fn"] = stop_fn
        req["dataprep_fn"] = dataprep_fn
        req["postprocessing_fn"] = postprocessing_fn
        req["init_state_fn"] = init_state_fn
        req["selector"] = self.selector
        req["leap_type"] = self.leap_type

        return req


class UDF(LeapFunction):
    def __init__(self):
        super().__init__()
        self.leap_type = codes.UDF
        
    def validate(self):
        pass


class PrivateLaplaceUDF(UDF):
    def __init__(self):
        super().__init__()
        self.leap_type = codes.LAPLACE_UDF

    def validate(self):
        pass


class PrivateExponentialUDF(UDF):
    def __init__(self):
        super().__init__()
        self.leap_type = codes.EXPONENTIAL_UDF


class PredefinedFunction(LeapFunction):
    def __init__(self, algo_code):
        super().__init__()
        self.algo_code = algo_code
        self.leap_type = codes.PREDEFINED

    def validate(self):
        pass

    def create_request(self):
        req = super().create_request()
        req["algo_code"] = self.algo_code
        return req

class PrivatePredefinedFunction(PredefinedFunction):
    def __init__(self, algo_code, epsilon, delta):
        super().__init__(algo_code)
        self.epsilon = epsilon
        self.delta = delta
        self.leap_type = codes.PRIVATE_PREDEFINED

    def validate(self):
        pass

    def create_request(self):
        req = super().create_request()
        req["epsilon"] = self.epsilon
        req["delta"] = self.delta
        return req


# Federated Learning class that extends the main Leap class.
class FedLearnFunction(PredefinedFunction):
    def __init__(self):
        super().__init__(codes.FEDERATED_LEARNING_ALGO)
        self.get_optimizer = None
        self.get_model = None
        self.get_criterion = None
        self.hyperparams = None
        self.get_dataloader = None
        self.leap_type = codes.FEDERATED_LEARNING
    
    def create_request(self):
        req = super().create_request()

        req["get_optimizer"] = leap_utils.fn_to_string(self.get_optimizer)
        req["get_criterion"] = leap_utils.fn_to_string(self.get_criterion)
        req["get_model"] = leap_utils.fn_to_string(self.get_model)
        req["get_dataloader"] = leap_utils.fn_to_string(self.get_dataloader)
        req["hyperparams"] = json.dumps(self.hyperparams)
        req["algo_code"] = self.algo_code
        return req

    def validate(self):
        pass
