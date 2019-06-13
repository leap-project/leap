import grpc
import argparse
import sys
import google.protobuf.any_pb2 as any_pb2
# TODO: Fix this ugly import
sys.path.append('../ProtoBuf')

import coordinator_pb2_grpc
import registration_msgs_pb2
import computation_msgs_pb2
import count_msgs_pb2 as identity_msgs_pb2
import pdb
import json

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--algoId", default=1, help="The id of this algorithm")
parser.add_argument("-cip", "--coordinatorIpPort", default='127.0.0.1:50000', help="The ip and port of the coordinator")
args = parser.parse_args()

# Creates a cloud algo registration request using the parameters
# given.
#
# id: The id of the algorithm to be registered.
# description: A description of what this algorithm does.
# proto_version: The protocol buffer version being used by
#                this algorithm.
# ip_port: The ip and port this algorithm is listening to.
def create_registration_request(id, description, proto_version, ip_port):
    request = registration_msgs_pb2.CloudAlgoRegReq()
    request.id = id
    request.description = description
    request.proto_version = proto_version
    request.algo_ip_port = ip_port
    return request

# Makes an RPC call to the coordinator to register an algo
# with the id given as parameter.
#
# stub: Stub for the cloud coordinator.
# algo_id: The id of the algo to be registered.
# ip_port: The ip and port of the algo to be registered.
def register(stub, algo_id, ip_port):
    description = "An identity algorithm"
    registration_request = create_registration_request(algo_id, description, "proto3", ip_port)
    response = stub.RegisterAlgo(registration_request)
    if hasattr(response, "success"):
        if response.success:
            print(response.msg)
        else:
            print(response.msg)

# Return a protobuf query from a filter_logic string.
#
# filter_logic: The filter_logic used to filter the results
#               from posting a request to RedCap.
def create_identity_query(filter_logic):
    query = identity_msgs_pb2.Query()
    query.filter_logic = filter_logic
    return query

# Returns a request containing a query and the algorithm id.
# This request is passed to the coordinator and will be used
# to return a response.
#
# query: The query that the request will slap a header on.
def create_computation_request(q):
    request = computation_msgs_pb2.ComputeRequest()
    any_msg = any_pb2.Any()
    request.algo_id = int(args.algoId)
    any_msg.Pack(q)
    request.req.CopyFrom(any_msg)
    return request

# Makes an RPC call to the coordinator with the given query
# and returns the count from each site.
#
# stub:  Stub for the cloud coordinator
# query: Query to be performed in local sites
def identity(stub, query):
    req = create_computation_request(query)
    result = stub.Compute(req)
    if hasattr(result, "err"):
        print(result.err)
    unpacked_result = computation_msgs_pb2.StringResponse()
    res = []

    
    for i in result.responses:
        i.response.Unpack(unpacked_result)
        json_response = json.loads(unpacked_result.val)
        res.extend(json_response)
    print(res)
    return res

if __name__ == "__main__":
    # Sets up the connection so that we can make RPC calls
    with grpc.insecure_channel(args.coordinatorIpPort) as channel:
        stub = coordinator_pb2_grpc.CloudCoordinatorStub(channel)

        register(stub, int(args.algoId), "")
        query = create_identity_query("[age] > 50 and [bmi] < 25")
        print("Returning all records that are above 50 and with bmi less than 25")
        identity(stub, query)

