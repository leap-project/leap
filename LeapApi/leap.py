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

# TODO: Deal with imports. Right now, we assume the local sites and cloud have all necessary imports.



class Leap():

    # Constructor that takes in a code representing one of
    # the available algorithms in Leap.
    def __init__(self):
        self.__map_fn = []
        self.__agg_fn = []
        self.__choice_fn = None
        self.__update_fn = []
        self.__stop_fn = None
        self.__data_prep_fn = None
        self.__postprocessing_fn = None
        self.__init_algo_state_fn = None


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
        request = 0
        return request


class UDF(Leap):
    def __init__(self):
        super().__init__()
    
    def validate(self):
        pass
    
class PredefinedFunction(Leap):
    def __init__(self, algo_code):
        super().__init__()
        self.algo_code = algo_code

    def validate(self):
        pass


# Federated Learning class that extends the main Leap class.
class FedLearn(PredefinedFunction):
    def __init__(self, algo_id):
        super().__init__(algo_id)
        self.optimizer = None
        self. model = None
        self. criterion = None
    
    def validate(self):
        pass
