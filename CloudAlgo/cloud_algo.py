# File for a program that listens to requests from clients
# and runs some of the 8 abstract functions in leap.
#
# Usage: python -m cloud_algo -ip=127.0.0.1:70000 -cip=127.0.0.1:50000 -secure=False -crt="./certificates/client.crt" -key="./certificates/client.key" -ca="../Certificates/myCA.crt"

import sys
sys.path.append("../")
import time
import argparse
import multiprocessing
import grpc
import ProtoBuf as pb
import concurrent.futures as futures
import json
import logging
from pylogrus import PyLogrus, TextFormatter
import copy

import sys
sys.path.append("../")
import Utils.env_manager as env_manager
import LeapApi.codes as codes

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ip_port", default="127.0.0.1:70000", help="The ip and port this algorithm is listening to")
parser.add_argument("-cip", "--coordinator_ip_port", default="127.0.0.1:50000", help="The ip and port of the cloud coordinator")
parser.add_argument("-secure", "--secure_with_tls", default=False, help="Whether to use SSL/TLS encryption on connections")
parser.add_argument("-crt", "--cert", default="./certificates/client.crt", help="The SSL/TLS certificate for the cloud algo")
parser.add_argument("-key", "--key", default="./certificates/client.key", help="The SSL/TLS private key for the cloud algo")
parser.add_argument("-ca", "--certificate_authority", default="../Certificates/myCA.crt", help="The certificate authority")
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


# GRPC service for cloud algos
class CloudAlgoServicer(pb.cloud_algos_pb2_grpc.CloudAlgoServicer):
    def __init__(self, ip_port, coordinator_ip_port):
        self.ip_port = ip_port
        self.coordinator_ip_port = coordinator_ip_port
        self.id_count = 0
        self.live_requests = {}
        self.crt = None
        self.key = None
        self.ca = None

    # Coordinates computations across multiple local sites and returns result to client
    #   req["module"]: stringified python module containing
    #       * map_fn: a list of map(data, site_state) that returns local computations at each iteration
    #       * agg_fn: a list of agg(map_results, cloud_state) used to aggregate results from each site
    #       * update_fn: a list of update(agg_result, site_state, cloud_state) used to update the site and cloud states
    #       * choice_fn(site_state): selects the appropriate map/agg_fn depending on the state
    #       * stop_fn(agg_result, site_state, cloud_state): returns true if stopping criterion is met
    #       * post_fn(agg_result, site_state, cloud_state): final processing of the aggregated result to return to client
    #       * data_prep(data): converts standard data schema from each site to be compatible with map_fn
    #       * prep(site_state): initialization for the cloud
    #       * site_state: state that is passed to the sites
    #       * cloud_state: state that is only used by the cloud
    #
    #   req["filter"]: query filter string to get dataset of interest

    # Grpc service call for the cloud algo to compute some
    # algorithm.
    #
    # request: The algorithm to be computed
    # context: Grpc boilerplate
    def Compute(self, request, context):
        req_id = self._generate_req_id()
        log.withFields({"request-id": req_id}).info("Received a computation request.")
        try:
            coord_stub = self._get_coord_stub()
            req = json.loads(request.req)

            leap_type = req["leap_type"]
            if leap_type == codes.UDF:
                env = env_manager.CloudUDFEnvironment()
            elif leap_type == codes.LAPLACE_UDF:
                env = env_manager.CloudUDFEnvironment() # LaplaceUDF does not change cloud api logic
            elif leap_type == codes.EXPONENTIAL_UDF:
                env = env_manager.CloudUDFEnvironment()
            elif leap_type == codes.PREDEFINED:
                env = env_manager.CloudPredefinedEnvironment()
            elif leap_type == codes.PRIVATE_PREDEFINED:
                env = env_manager.CloudPrivatePredefinedEnvironment()
            elif leap_type == codes.FEDERATED_LEARNING:
                env = env_manager.CloudFedereatedLearningEnvironment()
            env.set_env(globals(), req, req_id)

            result = self._compute_logic(req, coord_stub, req_id)

            res = pb.computation_msgs_pb2.ComputeResponse()
            res.response = json.dumps(result)
        except grpc.RpcError as e:
            log.withFields({"request-id": req_id}).error(e.details())
            raise e
        except BaseException as e:
            log.withFields({"request-id": req_id}).error(e)
            raise e
        return res

    # Takes a request and the state and creates a request to
    # be sent to the coordinator that grpc understands.
    #
    # req_id: The id of the request.
    # req: The request to be serialized
    # state: The state that will go in the request.
    def _create_computation_request(self, req_id, req, state):
        request = pb.computation_msgs_pb2.MapRequest()
        request.id = req_id
        req = req.copy()
        req["state"] = state
        request.req = json.dumps(req)
        return request

    # Generates a new id for a request
    # TODO: Lock the request counter
    def _generate_req_id(self):
        # TODO: Sandbox each request to isolate environments.
        new_id = self.id_count
        self.live_requests[self.id_count] = None
        self.id_count += 1
        return new_id       

    # Gets the grpc stub to send a message to the coordinator.
    def _get_coord_stub(self):
        channel = None

        if args.secure_with_tls:
            creds = grpc.ssl_channel_credentials(root_certificates=self.ca, private_key=self.key, certificate_chain=self.crt)
            channel = grpc.insecure_channel(self.coordinator_ip_port, creds)
        else:
            channel = grpc.insecure_channel(self.coordinator_ip_port)

        coord_stub = pb.coordinator_pb2_grpc.CoordinatorStub(channel)
        return coord_stub

    # Contains the logic for aggregating and performing the
    # general algorithmic portion of Leap that happens in the
    # cloud.
    #
    # req: The request from a client.
    # coord_stub: The stub used to send a message to the
    #             coordinator.
    # req_id: The id of the request being sent.
    def _compute_logic(self, req, coord_stub, req_id):
        state = init_state_fn()

        stop = False
        while not stop:
            map_results = []

            # Choose which map/agg/update_fn to use
            choice = choice_fn(state)
            site_request = self._create_computation_request(req_id, req, state)

            # Get result from each site through coordinator
            results = coord_stub.Map(site_request)

            extracted_responses = self._extract_map_responses(results.responses)

            # Aggregate results from each site
            agg_result = agg_fn[choice](extracted_responses)

            # Update the state
            state = update_fn[choice](agg_result, state)

            # Decide to stop or continue
            stop = stop_fn(agg_result, state)
        post_result = postprocessing_fn(agg_result, state)
        return post_result

    # Extracts the protobuf responses into a list.
    #
    # pb_responses: Response message from protobuf.
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
    cloudAlgoServicer = CloudAlgoServicer(args.ip_port, args.coordinator_ip_port)

    if args.secure_with_tls:
        fd = open(args.crt)
        cloudAlgoServicer.crt = fd.read()
        fd = open(args.key)
        cloudAlgoServicer.key = fd.read()
        fd = open(args.certificate_authority)
        CloudAlgoServicer.ca = fd.read()

    pb.cloud_algos_pb2_grpc.add_CloudAlgoServicer_to_server(cloudAlgoServicer, server)
    server.add_insecure_port(args.ip_port)
    server.start()
    log.info("Server started")
    log.withFields({"ip-port": args.ip_port}).info("Listening for requests")
    while True:
        time.sleep(5)

if __name__ == "__main__":
    serverProcess = multiprocessing.Process(target=serve)
    serverProcess.start()


