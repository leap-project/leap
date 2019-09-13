# This file contains the code for the server that listens
# to requests from a coordinator. It also operates the logic
# for running the algorithms.
#
# Usage: python -m site_algo -ip=127.0.0.1:60000 -cip=127.0.0.1:50001

import sys
sys.path.append("../")
import grpc
import time
import pandas
import multiprocessing
import argparse
import concurrent.futures as futures
import redcap
import json
import ProtoBuf as pb
import logging
from pylogrus import PyLogrus, TextFormatter
import Utils.env_manager as env_manager
import LeapApi.codes as codes
import CloudAlgo.functions.privacy as leap_privacy
import csv

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ip_port", default="127.0.0.1:60000", help="The ip and port this algorithm is listening to")
parser.add_argument("-cip", "--connector_ip_port", default="127.0.0.1:50001", help="The ip and port of the site connector")
parser.add_argument("-csv", "--csv_true", default="0", help="Whether this site algo will retrieve data from csv or RedCap")
args = parser.parse_args()

# Setup logging tool
logging.setLoggerClass(PyLogrus)
logger = logging.getLogger(__name__)  # type: PyLogrus
logger.setLevel(logging.DEBUG)
formatter = TextFormatter(datefmt='Z', colorize=True)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
log = logger.withFields({"node": "site-algo"})

# TODO: Don't hardcode this
redCapUrl = "https://rc.bcchr.ca/redcap_demo/api/"
redCapToken = "3405DC778F3D3B9639E53C1A3394EC09"


# Gets the data from a database or csv file and returns
# the records to perform a computation on.
#
# filter: The filter that is used to retrieve the Redcap data.
def get_data_from_src(filter=""):
    if args.csv_true == "1":
        return get_csv_data()
    else:
        return get_redcap_data(redCapUrl, redCapToken, filter)


# TODO: Actually filter the data according to a user selector
# Gets the data from a csv file and returns the records to
# perform a computation on.
def get_csv_data():
    patients = pandas.read_csv("data.csv")
    print(patients)
    return patients


# Contacts a redCap project and returns the filtered records
# from this project
#
# url: Url of the RedCap project
# token: Token used to access RedCap project given in the url
# filterLogic: The filter to be applied to the results."""
def get_redcap_data(url, token, filter_logic):
    project = redcap.Project(url, token)
    patients = project.export_records(filter_logic=filter_logic)
    return patients

# Starts listening for RPC requests at the specified ip and
# port.

# No args
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb.site_algos_pb2_grpc.add_SiteAlgoServicer_to_server(SiteAlgoServicer(args.ip_port, args.connector_ip_port), server)
    server.add_insecure_port(args.ip_port)
    server.start()
    log.info("Server started")
    log.info("Listening at " + args.ip_port)
    while True:
        time.sleep(5)

# RPC Service for Site Algos
class SiteAlgoServicer(pb.site_algos_pb2_grpc.SiteAlgoServicer):
    def __init__(self, ip_port, connector_ip_port):
        self.ip_port = ip_port
        self.connector_ip_port = connector_ip_port
        self.live_requests = {}

    # RPC requesting for a map function to be run
    #
    # request: A protobuf request determining what to be
    #          computed
    # context: Boilerplate for grpc containing the context
    #          of the RPC."""
    def Map(self, request, context):
        try:
            self.live_requests[request.id] = None
            log.withFields({"request-id": request.id}).info("Got map request")

            req = json.loads(request.req)
            leap_type = req["leap_type"]
            if leap_type == codes.UDF:
                env = env_manager.SiteUDFEnvironment()
            elif leap_type == codes.LAPLACE_UDF:
                env = env_manager.SiteUDFEnvironment()
            elif leap_type == codes.EXPONENTIAL_UDF:
                env = env_manager.SiteExponentialUDFEnvironment()
            elif leap_type == codes.PREDEFINED:
                env = env_manager.SitePredefinedEnvironment()
            elif leap_type == codes.PRIVATE_PREDEFINED:
                env = env_manager.SitePrivatePredefinedEnvironment()
            elif leap_type == codes.FEDERATED_LEARNING:
                env = env_manager.SiteFederatedLearningEnvironment()
            env.set_env(globals(), req, request.id)
            log.withFields({"request-id": request.id}).info("Loaded all necessary environment")
            map_result = self.map_logic(request)
            res = self._get_response_obj()
            res.response = map_result
            self.live_requests.pop(request.id)
            return  res
        except BaseException as e:
            log.withFields({"request-id": request.id}).error(e)
            raise e

    # Gets the protobuf message for a map response
    #
    # No args
    def _get_response_obj(self):
        return pb.computation_msgs_pb2.MapResponse()

    # Chooses the appropriate map function to run, gets the
    # data, and computes the map function on the data.
    #
    # request: Request containing the functions to be run.
    def map_logic(self, request):
        req_id = request.id
        req = json.loads(request.req)

        state = req["state"]
                
        choice = choice_fn(state)
        data = self.get_data(req)
        if 'dataprep_fn' in globals():
            data = dataprep_fn(data)
        
        # Adding logic for private udf functions
        leap_type = req["leap_type"]
        if leap_type == codes.LAPLACE_UDF:
            # Compute sensitivity: maximum difference in score function
            epsilon = req["epsilon"]
            delta = req["delta"]
            target_attribute = req["target_attribute"]
            map_result = leap_privacy.dynamic_laplace(epsilon, delta, target_attribute, map_fn[choice], data, state)
        elif leap_type == codes.EXPONENTIAL_UDF:
            epsilon = req["epsilon"]
            delta = req["delta"]
            target_attribute = req["target_attribute"]
            map_result = leap_privacy.exponential(epsilon, delta, target_attribute, score_fn[choice], data, state)
        else:
            map_result = map_fn[choice](data, state)
        return map_result

    # Gets the data from the database
    #
    # req: A leap request containing the selector to retrieve
    #      the data.
    def get_data(self, req):
        s_filter = req["selector"]
        data = get_data_from_src(s_filter)
        return data

if __name__ == "__main__":
    serverProcess = multiprocessing.Process(target=serve)
    serverProcess.start()
