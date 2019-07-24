import grpc
import argparse
import sys
sys.path.append("../")
import pdb
import json

import inspect

import CloudAlgos.functions.count_fn as count_fn

import ProtoBuf as pb
# pb.computation_msgs_pb2

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--algoId", default=10, help="The id of this algorithm")
parser.add_argument("-cip", "--coordinatorIpPort", default='127.0.0.1:50000', help="The ip and port of the coordinator")
args = parser.parse_args()


class ClientConnector():
    def __init__(self, ipPort):
        print("Initialized Client Connector")
        self.coordinatorIpPort = ipPort


    def _create_computation_request(self, u_module, query):
        request = pb.computation_msgs_pb2.ComputeRequest()
        request.algo_id = int(args.algoId)
        req = {}
        req["module"] = u_module
        req["query"] = query
        request.req = json.dumps(req)
        return request


    # Creates a cloud algo registration request using the parameters
    # given.
    #
    # id: The id of the algorithm to be registered.
    # description: A description of what this algorithm does.
    # proto_version: The protocol buffer version being used by
    #                this algorithm.
    def _create_registration_request(self, id, description, proto_version):
        request = pb.registration_msgs_pb2.CloudAlgoRegReq()
        request.id = id
        request.description = description
        request.proto_version = proto_version
        return request

    # Makes an RPC call to the coordinator to register an algo
    # with the id given as parameter.
    #
    # stub: Stub for the cloud coordinator.
    # algo_id: The id of the algo to be registered.
    def _register(self, stub, algo_id):
        description = "A generic UDF algorithm"
        registration_request = self._create_registration_request(algo_id, description, "proto3")
        response = stub.RegisterCloudAlgo(registration_request)
        if hasattr(response, "success"):
            if response.success:
                print(response.msg)
            else:
                print(response.msg)

    def send_request(self, algo_id, u_module, query):
        # Sets up the connection so that we can make RPC calls
        with grpc.insecure_channel(args.coordinatorIpPort) as channel:
            stub = pb.coordinator_pb2_grpc.CoordinatorStub(channel)

            self._register(stub, int(algo_id))
            print("Query: {}".format(query))


            req = self._create_computation_request(u_module, query)

            result = stub.Compute(req) # Computed remotely

            if hasattr(result, "err"):
                print(result.err)

            result = json.loads(result.response)


            print("Received response")
            print(result)
        return result


def client_request():
    # Create connector. TODO: Decide how client request will talk to connector
    connector = ClientConnector(args.coordinatorIpPort)

    # Get source code for map, agg, update, etc
    module = inspect.getsource(count_fn)
    query = "[age] > 50 and [bmi] < 25"
    algoId = args.algoId
    connector.send_request(algoId, module, query)
    pdb.set_trace()


if __name__ == "__main__":
    client_request()

