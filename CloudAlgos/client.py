import grpc
import argparse
import sys
sys.path.append("../")
import pdb
import json

import inspect

import CloudAlgos.functions.count_fn as count_fn
import CloudAlgos.functions.sum_fn as sum_fn
import CloudAlgos.functions.fl_fn as fl_fn
import CloudAlgos.functions.var_fn as var_fn

import ProtoBuf as pb
# pb.computation_msgs_pb2

parser = argparse.ArgumentParser()
parser.add_argument("-cip", "--cloud_algos_ip_port", default='127.0.0.1:70000', help="The ip and port of the cloudAlgos")
args = parser.parse_args()

""" Client is responsible for making the rpc call to the cloud algorithm server
"""
class Client():
    def __init__(self, ipPort):
        print("Initializing Client")
        self.cloud_algos_ip_port = ipPort

    """ Creates protobuf computation request
    """
    def _create_computation_request(self, u_module, filter):
        request = pb.computation_msgs_pb2.ComputeRequest()
        req = {}
        req["module"] = u_module
        req["filter"] = filter
        request.req = json.dumps(req)
        return request

    """ RPC call to cloud_algos
    u_module: stringified python module containing
        * map_fn: a list of map(data, site_state) that returns local computations at each iteration
        * agg_fn: a list of agg(map_results, cloud_state) used to aggregate results from each site
        * update_fn: a list of update(agg_result, site_state, cloud_state) used to update the site and cloud states
        * choice_fn(site_state): selects the appropriate map/agg_fn depending on the state
        * stop_fn(agg_result, site_state, cloud_state): returns true if stopping criterion is met
        * post_fn(agg_result, site_state, cloud_state): final processing of the aggregated result to return to client
        * data_prep(data): converts standard data schema from each site to be compatible with map_fn
        * prep(site_state): initialization for the cloud
        * site_state: state that is passed to the sites
        * cloud_state: state that is only used by the cloud
    
    filter: query filter string to get dataset of interest
    """
    def send_request(self, u_module, filter):
        print("Sending request from client")
        # Sets up the connection so that we can make RPC calls
        with grpc.insecure_channel(args.cloud_algos_ip_port) as channel:
            stub = pb.cloud_algos_pb2_grpc.CloudAlgoStub(channel)

            req = self._create_computation_request(u_module, filter)
            result = stub.Compute(req) # Computed remotely

            if hasattr(result, "err"):
                print(result.err)

            result = json.loads(result.response)


            print("Received response")
            print(result)
        return result


def client_request():
    # Create connector. TODO: Decide how client request will talk to connector
    client = Client(args.cloud_algos_ip_port)

    # Get source code for map, agg, update, etc
    # module = inspect.getsource(count_fn)
    # module = inspect.getsource(var_fn)
    module = inspect.getsource(fl_fn)
    filter = "[age] > 50 and [bmi] < 25"
    client.send_request(module, filter)


if __name__ == "__main__":
    client_request()

