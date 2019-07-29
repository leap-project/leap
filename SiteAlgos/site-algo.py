import grpc
import time
import multiprocessing
import argparse
import concurrent.futures as futures
import sys
import google.protobuf.any_pb2 as any_pb2
import redcap

# TODO: Find way to get rid of this ugly import
sys.path.append('../ProtoBuf')

import computation_msgs_pb2 as computation_pb2
import count_msgs_pb2 as count_pb2
import site_algos_pb2_grpc as site_algos_grpc

parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ip_port", default="127.0.0.1:60000", help="The ip and port this algorithm is listening to")
parser.add_argument("-cip", "--connector_ip_port", default="127.0.0.1:50001", help="The ip and port of the site connector")
args = parser.parse_args()

redCapUrl = "https://rc.bcchr.ca/redcap_demo/api/"
redCapToken = "3405DC778F3D3B9639E53C1A3394EC09"

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
    site_algos_grpc.add_SiteAlgoServicer_to_server(SiteAlgoServicer(args.ip_port, args.connector_ip_port), server)
    server.add_insecure_port(args.ip_port)
    server.start()
    print("Site Algo: Server started")
    print("Site Algo: Listening at " + args.ip_port)
    while True:
        time.sleep(5)

# RPC Service for Site Algos
class SiteAlgoServicer(site_algos_grpc.SiteAlgoServicer):

    def __init__(self, ip_port, connector_ip_port):
        self.live_requests = {}
        self.ip_port = ip_port
        self.connector_ip_port = connector_ip_port

    # RPC requesting for a computation to be done using
    # this algorithm.
    #
    # request: A protobuf request determining what to be
    #          computed
    # context: Boilerplate for grpc containing the context
    #          of the RPC.
    def Map(self, request, context):
        print("Site-Algo: Got compute call")
        self.live_requests[request.id] = None
        # TODO: Extract map code and run it

        res = computation_pb2.MapResponse()
        res.response = "test result"
        return res

if __name__ == "__main__":
    serverProcess = multiprocessing.Process(target=serve)
    serverProcess.start()
