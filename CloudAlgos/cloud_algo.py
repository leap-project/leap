"""
Server to listen to requests from the Coordinator and 
spawn processes responsible for iterative aggregation logic

1. Generate unique ID for UDF
2. grpc call to coordinator to get site map results
"""
import sys
sys.path.append("../")
import time
import argparse
import multiprocessing
import grpc
import ProtoBuf as pb
import concurrent.futures as futures
import pdb
import json
import logging
from pylogrus import PyLogrus, TextFormatter

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ip_port", default="127.0.0.1:70000", help="The ip and port this algorithm is listening to")
parser.add_argument("-cip", "--coordinator_ip_port", default="127.0.0.1:50000", help="The ip and port of the cloud coordinator")
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
log = logger.withFields({"node": "cloud-algo"})

# Receives ComputeRequest from Coordinator
class CloudAlgoServicer(pb.cloud_algos_pb2_grpc.CloudAlgoServicer):
    def __init__(self, ip_port, coordinator_ip_port):
        self.ip_port = ip_port
        self.coordinator_ip_port = coordinator_ip_port
        self.id_count = 0
        self.live_requests = {}

    # input_req is the request sent by the client_connector
    def _create_computation_request(self, req_id, input_req, state):
        request = pb.computation_msgs_pb2.MapRequest()
        request.id = req_id
        # TODO: Split cloud algo udf functions from site algos
        req = {}
        req["module"] = input_req["module"]
        req["filter"] = input_req["filter"]
        req["state"] = state
        request.req = json.dumps(req)
        return request

    def _generate_req_id(self):
        # TODO: actually spawn child processes. thread is currently None
        new_id = self.id_count
        self.live_requests[self.id_count] = None
        self.id_count += 1
        return new_id       

    def Compute(self, request, context):
        # TODO: This logic should eventually be ran in separate thread
        req = json.loads(request.req)
        exec(req["module"], globals())
        state = globals()["state"]
        # local_state = prep(state)
        local_state = state
        stop = False
        
        # Generate algo_id
        req_id = self._generate_req_id()
        with grpc.insecure_channel(self.coordinator_ip_port) as channel:
            coord_stub = pb.coordinator_pb2_grpc.CoordinatorStub(channel)
            while not stop:
                map_results = []
                choice = choice_fn(state)
                try:
                    request = self._create_computation_request(req_id, req, state)               
                except Exception as e:
                    log.error(e)

                try:
                    results = coord_stub.Map(request) # Computed remotely
                except grpc.RpcError as e:
                    log.error(e.details())
                    return e

                extracted_responses = self._extract_map_responses(results.responses)
                agg_result = agg_fn[choice](extracted_responses, local_state)
                state = update_fn[choice](agg_result, state, local_state)
                stop = stop_fn(agg_result, state, local_state)
            
            res = pb.computation_msgs_pb2.ComputeResponse()
            res.response = json.dumps(post_fn(agg_result, state, local_state))
        return res
    
    def _extract_map_responses(self, pb_responses):
        responses = []
        for r in pb_responses:
            responses.append(r.response)
        return responses


# Starts listening for RPC requests at the specified ip and
# port.
#
# No args
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb.cloud_algos_pb2_grpc.add_CloudAlgoServicer_to_server(CloudAlgoServicer(args.ip_port, args.coordinator_ip_port), server)
    server.add_insecure_port(args.ip_port)
    server.start()
    log.info("Server started")
    log.withFields({"ip-port": args.ip_port}).info("Listening for requests")
    while True:
        time.sleep(5)

if __name__ == "__main__":
    serverProcess = multiprocessing.Process(target=serve)
    serverProcess.start()


