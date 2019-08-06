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

# TODO: Deal with imports. Right now, we assume the local sites and cloud have all necessary imports.



class Leap():

    # Constructor that takes in a code representing one of
    # the available algorithms in Leap.
    def __init__(self, algo_code):
        self.algo_code = algo_code
        self.__map_fn = None
        self.__agg_fn = None
        self.__choice_fn = None
        self.__update_fn = None
        self.__stop_fn = None
        self.__data_prep_fn = None
        self.__postprocessing_fn = None
        self.__site_state = None
        self.__cloud_state = None

    # Returns an instance of the Leap class that will count
    # the number of selected records.
    @staticmethod
    def Count(self):
        return Leap(codes.COUNT)
    # Returns an instance of the Leap class that will compute
    # a summation of selected records.
    @staticmethod
    def Sum(self):
        return Leap(codes.SUM)

    # Returns an instance of the Leap class that will compute
    # the variance of selected records.
    @staticmethod
    def Variance(self):
        return Leap(codes.VARIANCE)

    # Returns an instance of the Leap class that can fit a
    # federated learning model.
    @staticmethod
    def FederatedLearning(self):
        return FedLearn(codes.FEDERATED_LEARNING)

    # Sets the map function of the algorithm to be a user
    # defined map function.
    #
    # map_fn: User defined map function.
    def set_map_fn(self, map_fn):
        self.__map_fn = map_fn

    # Sets the aggregation function of the algorithm to be a
    # user defined aggregation function.
    #
    # agg_fn: User defined aggregate function.
    def set_agg_fn(self, agg_fn):
        self.__agg_fn = agg_fn

    # Sets the choice function of the algorithm to be a user
    # defined choice function.
    #
    # choice_fn: User defined choice function.
    def set_choice_fn(self, choice_fn):
        self.__choice_fn = choice_fn

    # Sets the update function of the algorithm to be a user
    # defined update function.
    #
    # update_fn: User defined update function.
    def set_update_fn(self, update_fn):
        self.__update_fn = update_fn

    # Sets the stop function of the algorithm to be a user
    # defined stop function.
    #
    # stop_fn: User defined stop function.
    def set_stop_fn(self, stop_fn):
        self.__stop_fn = stop_fn

    # Sets the data prep function of the algorithm to be a
    # user defined data prep function.
    #
    # data_prep_fn: User defined data prep function.
    def set_data_prep_fn(self, data_prep_fn):
        self.__data_prep_fn = data_prep_fn

    # Sets the postprocessing function of the algorithm to be
    # a user defined postprocessing function.
    #
    # postprocessing_fn: User defined postprocessing function.
    def set_postprocessing_fn(self, postprocessing_fn):
        self.__postprocessing_fn = postprocessing_fn

    # Sets the initial state of the local site.
    #
    # site_state: The initial state of the site.
    def set_site_state(self, site_state):
        self.__site_state = site_state

    # Sets the initial state of the cloud algo.
    #
    # cloud_state: The initial state of the cloud algo.
    def set_cloud_state(self, cloud_state):
        self.__cloud_state = cloud_state

    # Gets the result of performing the selected algorithm
    # on the filtered data.
    #
    # filter: A SQL string filter to select the data to perform
    #         a computation.
    def get_result(self, filter):
        request = self.__create_computation_request("")

        # Sets up the connection so that we can make RPC calls
        with grpc.insecure_channel("127.0.0.1:70000") as channel:
            stub = pb.cloud_algos_pb2_grpc.CloudAlgoStub(channel)

            # Computed remotely
            result = stub.Compute(request)

            if hasattr(result, "err"):
                print(result.err)

            result = json.loads(result.response)


            print("Received response")
            print(result)
        return result

    # Uses protobuf to create a computation request.
    #
    # filter: The SQL string filter that is passed as an
    #         argument to the request.
    def __create_computation_request(self, filter):
        request = pb.computation_msgs_pb2.ComputeRequest()
        req = {}
        req["map_fn"] = self.__map_fn
        req["agg_fn"] = self.__agg_fn
        req["choice_fn"] = self.__choice_fn
        req["update_fn"] = self.__update_fn
        req["stop_fn"] = self.__stop_fn
        req["dataprep_fn"] = self.__data_prep_fn
        req["setup_fn"] = self.__setup_fn
        req["post_fn"] = self.__postprocessing_fn
        req["filter"] = filter
        request.req = json.dumps(req)
        return request


# Federated Learning class that extends the main Leap class.
class FedLearn(Leap):
    def __init__(self, algo_id):
        super().__init__(algo_id)
        self.optimizer = None
        self. model = None
        self. criterion = None

    # Sets the optimizer for federated learning to be the
    # optimizer given as a parameter.
    #
    # optimizer: Optimizer for federated learning
    def set_optimizer(self, optimizer):
        self.optimizer = optimizer

    # Sets the model for federated learning to be the model
    # given as a parameter.
    #
    # model: Model for federated learning.
    def set_model(self, model):
        self.model = model

    # Sets the criterion for federated learning to be the
    # criterion given as a parameter.
    #
    # criterion: Criterion for federated learning.
    def set_criterion(self, criterion):
        self.criterion = criterion
