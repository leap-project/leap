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
# TODO: Deal with imports. Right now, we assume the local sites and cloud have all necessary imports.



class Leap():

    # Constructor that takes in a code representing one of
    # the available algorithms in Leap.
    def __init__(self):
        self.map_fn = []
        self.agg_fn = []
        self.choice_fn = None
        self.update_fn = []
        self.stop_fn = None
        self.dataprep_fn = None
        self.postprocessing_fn = None
        self.init_state_fn = None

    # Gets the result of performing the selected algorithm
    # on the filtered data.
    #
    # filter: A SQL string filter to select the data to perform
    #         a computation.
    def send_request(self, filter):
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
        map_fn = [inspect.getsource(m_fn) for m_fn in self.map_fn]
        agg_fn = [inspect.getsource(a_fn) for a_fn in self.agg_fn]
        update_fn = [inspect.getsource(u_fn) for u_fn in self.update_fn]
        choice_fn = inspect.getsource(self.choice_fn)
        stop_fn = inspect.getsource(self.stop_fn)
        dataprep_fn = inspect.getsource(self.dataprep_fn)
        postprocessing_fn = inspect.getsource(self.postprocessing_fn)
        init_state_fn = inspect.getsource(self.init_state_fn)

        req["map_fn"] = map_fn
        req["agg_fn"] = agg_fn
        req["update_fn"] = update_fn
        req["choice_fn"] = choice_fn
        req["stop_fn"] = stop_fn
        req["dataprep_fn"] = dataprep_fn
        req["postprocessing_fn"] = postprocessing_fn
        req["init_state_fn"] = init_state_fn

        request.req = json.dumps(req)
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
