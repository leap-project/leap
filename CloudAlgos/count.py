import grpc
import sys
import google.protobuf.any_pb2 as any_pb2
# TODO: Fix this ugly import
sys.path.append('../ProtoBuf')

import coordinator_pb2_grpc as coordinator_pb2_grpc
import computation_msgs_pb2 as computation_msgs_pb2
import count_msgs_pb2 as count_msgs_pb2


# Return a protobuf query from a filter_logic string.
#
# filter_logic: The filter_logic used to filter the results
#               from posting a request to RedCap.
def create_count_query(filter_logic):
    query = count_msgs_pb2.Query()
    query.filter_logic = filter_logic
    return query

# Returns a request containing a query and the algorithm id.
# This request is passed to the coordinator and will be used
# to return a response.
#
# query: The query that the request will slap a header on
def create_computation_request(q):
    request = computation_msgs_pb2.ComputeRequest()
    any_msg = any_pb2.Any()
    request.algo_id = 0
    any_msg.Pack(q)
    request.req.CopyFrom(any_msg)
    return request

# Makes an RPC call to the coordinator with the given query
# and returns the count from each site.
#
# stub:  Stub for the cloud coordinator
# query: Query to be performed in local sites
def count(stub, query):
    req = create_computation_request(query)
    result = stub.Compute(req)
    if hasattr(result, "err"):
        print(result.err)
    unpacked_result = computation_msgs_pb2.IntResponse()
    total = 0
    for i in result.responses:
        i.response.Unpack(unpacked_result)
        total += unpacked_result.val
    print(total)
    return total

if __name__ == "__main__":
    # Sets up the connection so that we can make RPC calls
    with grpc.insecure_channel('127.0.0.1:50000') as channel:
        stub = coordinator_pb2_grpc.CloudCoordinatorStub(channel)
        print("Counting all records that are above 50 and with bmi less than 25")
        query = create_count_query("[age] > 50 and [bmi] < 25")
        count(stub, query)

