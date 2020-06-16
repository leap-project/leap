# This is the main API that users interact with LEAP. Users
# will create an instance of the LEAP class and can either
# set their own user defined functions or use one of the func-
# tions available in LEAP

import json
import proto as pb
from utils import leap_utils
from proto import computation_msgs_pb2

# The main base class for a Leap function.
class LeapFunction:

    # Constructor that initializes the abstract functions in
    # Leap to None.
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

    # Creates a request to be sent to a Leap program with the
    # abstract functions and the selector.
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

        return req


# A user defined leap function. Extends the base LeapFunction.
class UDF(LeapFunction):

    def __init__(self):
        super().__init__()
        self.leap_type = pb.computation_msgs_pb2.LeapTypes.UDF
        
    def validate(self):
        pass


# A user defined leap function that uses the laplace mechanism
# for privacy.
class PrivateLaplaceUDF(UDF):

    # Takes in epsilon and delta, which are privacy parameters,
    # and the target_attribute, which is the field in the map result
    # that we want to make private
    def __init__(self, epsilon, delta, target_attribute):
        super().__init__()
        self.leap_type = pb.computation_msgs_pb2.LeapTypes.LAPLACE_UDF
        self.epsilon = epsilon
        self.delta = delta
        self.target_attribute = target_attribute

    # Creates a request with the abstract funcitons and the
    # privacy parameters and target attributes defined.
    def create_request(self):
        req = super().create_request()
        req["epsilon"] = self.epsilon
        req["delta"] = self.delta
        req["target_attribute"] = self.target_attribute
        return req

    def validate(self):
        pass


# A user defined leap funciton that uses the exponential mechanism
# for privacy.
class PrivateExponentialUDF(UDF):

    # Takes in epsilon and delta, which are privacy parameters,
    # and the target_attribute, which is the field in the map result
    # that we want to make private
    def __init__(self, epsilon, delta, target_attribute):
        super().__init__()
        self.leap_type = pb.computation_msgs_pb2.LeapTypes.EXPONENTIAL_UDF
        self.epsilon = epsilon
        self.delta = delta
        self.target_attribute = target_attribute
        self.score_fns = None

    # Creates a request with the abstract functions, the
    # privacy parameters and target attributes, and the score
    # function used by the exponential mechanism.
    def create_request(self):
        req = {}
        score_fns = leap_utils.fn_to_string(self.score_fns)
        agg_fns = leap_utils.fn_to_string(self.agg_fns)
        update_fns = leap_utils.fn_to_string(self.update_fns)
        choice_fn = leap_utils.fn_to_string(self.choice_fn)
        stop_fn = leap_utils.fn_to_string(self.stop_fn)
        dataprep_fn = leap_utils.fn_to_string(self.dataprep_fn)
        postprocessing_fn = leap_utils.fn_to_string(self.postprocessing_fn)
        init_state_fn = leap_utils.fn_to_string(self.init_state_fn)

        req["score_fns"] = score_fns
        req["agg_fns"] = agg_fns
        req["update_fns"] = update_fns
        req["choice_fn"] = choice_fn
        req["stop_fn"] = stop_fn
        req["dataprep_fn"] = dataprep_fn
        req["postprocessing_fn"] = postprocessing_fn
        req["init_state_fn"] = init_state_fn
        req["selector"] = self.selector
        req["epsilon"] = self.epsilon
        req["delta"] = self.delta
        req["target_attribute"] = self.target_attribute
        return req


# Extends the base LeapFunction and allows the user to choose
# a Leap function that is already implemented in Leap.
class PredefinedFunction(LeapFunction):

    # Constructor
    #
    # algo_code: The number code for the algorithm that the
    #            user wants to run.
    def __init__(self, algo_code):
        super().__init__()
        self.algo_code = algo_code
        self.leap_type = pb.computation_msgs_pb2.LeapTypes.PREDEFINED

    def validate(self):
        pass

    # Creates a request with the algo_code of the function
    # that we want to run.
    def create_request(self):
        req = super().create_request()
        return req


# Extends the PredefinedFunction, but allows the output to
# be differentially private.
class PrivatePredefinedFunction(PredefinedFunction):

    # Constructor
    #
    # algo_code: Number code for the algo to be executed.
    # epsilon: Privacy parameter
    # delta: Privacy parameter
    def __init__(self, algo_code, epsilon, delta):
        super().__init__(algo_code)
        self.eps = epsilon
        self.delt = delta
        self.leap_type = pb.computation_msgs_pb2.LeapTypes.PRIVATE_PREDEFINED

    def validate(self):
        pass

    # Creates a request with epsilon and delta.
    def create_request(self):
        req = super().create_request()
        req["epsilon"] = self.eps
        req["delta"] = self.delt
        return req


# Federated Learning class that extends the main Leap class.
class FedLearnFunction(PredefinedFunction):
    def __init__(self):
        super().__init__(computation_msgs_pb2.AlgoCodes.FEDERATED_LEARNING_ALGO)
        self.get_optimizer = None
        self.get_model = None
        self.get_criterion = None
        self.hyperparams = None
        self.get_dataloader = None
        self.leap_type = pb.computation_msgs_pb2.LeapTypes.FEDERATED_LEARNING

    # Creates a request for a federated learning model to be
    # trained. The request includes the optimizer, criterion, model,
    # dataloader, and hyperparams necessary for training a Pytorch
    # model.
    def create_request(self):
        req = super().create_request()

        req["get_optimizer"] = leap_utils.fn_to_string(self.get_optimizer)
        req["get_criterion"] = leap_utils.fn_to_string(self.get_criterion)
        req["get_model"] = leap_utils.fn_to_string(self.get_model)
        req["get_dataloader"] = leap_utils.fn_to_string(self.get_dataloader)
        req["hyperparams"] = json.dumps(self.hyperparams)
        return req

    def validate(self):
        pass
