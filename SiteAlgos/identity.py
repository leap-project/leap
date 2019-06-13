import grpc
import time
import multiprocessing
import argparse
import concurrent.futures as futures
import sys
import google.protobuf.any_pb2 as any_pb2
import redcap
import json

# TODO: Find way to get rid of this ugly import
sys.path.append('../ProtoBuf')

import computation_msgs_pb2 as computation_pb2
import registration_msgs_pb2 as registration_pb2
import count_msgs_pb2 as count_pb2
import site_algos_pb2_grpc as site_algos_grpc
import site_connector_pb2_grpc as site_connector_grpc

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--algoId", default="1", help="The id of this algorithm")
parser.add_argument("-ip", "--ipPort", default="127.0.0.1:60000", help="The ip and port this algorithm is listening to")
parser.add_argument("-cip", "--connectorIpPort", default="127.0.0.1:50003", help="The ip and port of the site connector")
args = parser.parse_args()

redCapUrl = "https://rc.bcchr.ca/redcap_demo/api/"
redCapToken = "3405DC778F3D3B9639E53C1A3394EC09"

# Makes an RPC to the site-connector, with the intent of
# registering this algorithm with the coordinator.
#
# No args
def register():
    with grpc.insecure_channel(args.connectorIpPort) as channel:
        stub = site_connector_grpc.AlgoConnectorStub(channel)
        req = registration_pb2.SiteAlgoRegReq()
        req.algo_id = int(args.algoId)
        req.description = "An identity algorithm"
        req.proto_version = "proto3"
        req.algo_ip_port = args.ipPort
        response = stub.RegisterAlgo(req)
        if response.success:
            print("Site-Algo " + args.algoId + ": Successfully registered algorithm with coordinator")

# Contacts a redCap project and returns the filtered records
# from this project.
#
# url: Url of the RedCap project
# token: Token used to access RedCap project given in the
#        url
# filterLogic: The filter to be applied to the results.
def getRedcapData(url, token, filterLogic):
    project = redcap.Project(url, token)
    patients = project.export_records(filter_logic=filterLogic)
    return patients

# Starts listening for RPC requests at the specified ip and
# port.
#
# No args
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    site_algos_grpc.add_SiteAlgoServicer_to_server(SiteAlgoServicer(), server)
    server.add_insecure_port(args.ipPort)
    server.start()
    print("Site Algo " + args.algoId + ": Server started")
    print("Site Algo " + args.algoId + ": Listening at " + args.ipPort)
    while True:
        time.sleep(5)

# RPC Service for Site Algos
class SiteAlgoServicer(site_algos_grpc.SiteAlgoServicer):

    # RPC requesting for a computation to be done using
    # this algorithm.
    #
    # request: A protobuf request determining what to be
    #          computed
    # context: Boilerplate for grpc containing the context
    #          of the RPC.
    def Compute(self, request, context):
        print("Site-Algo " + args.algoId + ": Got compute call")
        query = count_pb2.Query()
        if request.req.Is(query.DESCRIPTOR):
            request.req.Unpack(query)
        result = getRedcapData(redCapUrl, redCapToken, query.filter_logic)

        res = computation_pb2.ComputeResponse()

        # # Option 0
        # int_response = computation_pb2.IntResponse()
        # int_response.val = 5
        # any_res = any_pb2.Any()
        # any_res.Pack(int_response)
        # res.response.CopyFrom(any_res)

        # # Option 1
        # any_res = any_pb2.Any()
        # any_res.Pack(result)
        # res.response.CopyFrom(any_res)

        # # Option 2
        # res.response = result # Doesn't work for same reason as optoin 3

        # # Option 3 -- bad because we can't set protobuf.any = result (python any)
        # # Define computation_pb2.AnyResponse()
        # any_response = computation_pb2.AnyResponse()
        # any_response.val = result
        # any_res = any_pb2.Any()
        # any_res.Pack(any_response)
        # res.response.CopyFrom(any_res)

        # Option 4
        str_response = computation_pb2.StringResponse()
        str_response.val = json.dumps(result)
        any_res = any_pb2.Any()
        any_res.Pack(str_response)
        res.response.CopyFrom(any_res)

        return res



if __name__ == "__main__":
    serverProcess = multiprocessing.Process(target=serve)
    serverProcess.start()
    register()
