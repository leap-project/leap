"""
Server to listen to requests from the Coordinator and 
spawn processes responsible for iterative aggregation logic

1. Generate unique ID for UDF
2. grpc call to coordinator to get site map results
"""
import time
import argparse
import multiprocessing
import grpc
import concurrent.futures as futures
import pdb
import json
import sys
sys.path.append("../")

import ProtoBuf as pb
parser = argparse.ArgumentParser()
parser.add_argument("-ip", "--ipPort", default="127.0.0.1:60000", help="The ip and port this algorithm is listening to")
parser.add_argument("-cip", "--coordinatorIpPort", default="127.0.0.1:50001", help="The ip and port of the cloud coordinator")
args = parser.parse_args()

# Receives ComputeRequest from Coordinator
class CloudAlgoServicer(pb.cloud_algos_pb2_grpc.CloudAlgoServicer):
    def __init__(self, ipPort, coordinatorIpPort):        
        self.ipPort = ipPort
        self.coordinatorIpPort = coordinatorIpPort
        

        # super(CloudAlgoServicer, self).__init__() # Object ... doesn't do anythin
        self.id_to_thread = {}
        self.id_count = 0

    def _create_computation_request(self, req_id, req):
        request = pb.computation_msgs_pb2.MapRequest()
        request.id = req_id
        # TODO: Split cloud algo udf functions from site algos
        request.req = json.dumps(req)
        return request

    def _generate_req_id(self):
        # TODO: actually spawn child processes. thread is currently None
        self.id_to_thread[self.id_count] = None
        self.id_count += 1
        return self.id_count

    def Compute(self, request, context):
        print("Cloud-Algo : Got compute call")
        # TODO: This logic should eventually be ran in separate thread
        req = json.loads(request.req)
        print("Loading module...")
        exec(req["module"], globals())
        # print("Request in cloud_algo.Compute: {}".format(req))
        state = globals()["state"]
        stop = False
        
        # Generate algo_id
        req_id = self._generate_req_id()
        print("Generated cloud algo id: {}".format(req_id))
        with grpc.insecure_channel(self.coordinatorIpPort) as channel:
            coord_stub = pb.coordinator_pb2_grpc.CoordinatorStub(channel)
            print("Created coordinator stub")
            while not stop:
                map_results = []
                choice = choice_fn(state)
                print("Choice: {}".format(choice))
                request = self._create_computation_request(req_id, req)               
                print("Created map request")

                result = coord_stub.Map(request) # Computed remotely
                print("Received map results from cloud coordinator")

                map_results = json.loads(result.response)
                agg_result = agg_fn[choice](map_results)
                state = update_fn[choice](agg_result, state)
                stop = stop_fn(agg_result, state)
            
            res = pb.computation_msgs_pb2.ComputeResponse()
            res.response = json.dumps(post_fn(agg_result, state))
        print("returning response to client connector")
        return res

# Starts listening for RPC requests at the specified ip and
# port.
#
# No args
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb.cloud_algos_pb2_grpc.add_CloudAlgoServicer_to_server(CloudAlgoServicer(args.ipPort, args.coordinatorIpPort), server)
    server.add_insecure_port(args.ipPort)
    server.start()
    print("Cloud Algo : Server started")
    print("Cloud Algo : Listening at {}".format(args.ipPort))
    while True:
        time.sleep(1)

if __name__ == "__main__":
    serverProcess = multiprocessing.Process(target=serve)
    serverProcess.start()
