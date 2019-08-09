# This is the main API that users interact with LEAP. Users
# will create an instance of the LEAP class and can either
# set their own user defined functions or use one of the func-
# tions available in LEAP
from abc import ABC, abstractmethod
import sys
sys.path.append("../")
import json
import grpc
import ProtoBuf as pb
import LeapApi.codes as codes
import inspect
import pdb
from Utils import leap_utils

class LocalCloudRequest():
    def __init__(self):
        self.req = None

# TODO: Deal with imports. Right now, we assume the local sites and cloud have all necessary imports.
class Leap(ABC):

    # Constructor that takes in a code representing one of
    # the available algorithms in Leap.
    def __init__(self, leap_function):
        self.leap_function = leap_function

    # # Gets the result of performing the selected algorithm
    # # on the filtered data.
    # #
    def get_result(self):
        request = self._create_computation_request()
            
        compute_stub = self._get_compute_stub()

        # Computed remotely
        result = compute_stub.Compute(request, None)
        
        result = json.loads(result.response)
        return result

    # Uses protobuf to create a computation request.
    #
    def _create_computation_request(self):
        request = self._create_request_obj()

        req = self.leap_function.create_request()
        request.req = json.dumps(req)
        return request

    @abstractmethod
    def _get_compute_stub(self):
        pass
    
    @abstractmethod
    def _create_request_obj(self):
        pass
    

class LocalLeap(Leap):
    def __init__(self, leap_function, cloud):
        super().__init__(leap_function)
        self.cloud = cloud

    def _get_compute_stub(self):
        return self.cloud

    def _create_request_obj(self):
        request = LocalCloudRequest()
        return request 


class DistributedLeap(Leap):
    def __init__(self, leap_function):
        super().__init__(leap_function)
    
    def _get_compute_stub(self):
        # Sets up the connection so that we can make RPC calls
        channel = grpc.insecure_channel("127.0.0.1:70000")
        stub = pb.cloud_algos_pb2_grpc.CloudAlgoStub(channel)
        return stub

    def _create_request_obj(self):
        request = pb.computation_msgs_pb2.ComputeRequest()
        return request 