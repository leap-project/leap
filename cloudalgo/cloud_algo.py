# File for a program that listens to requests from clients
# and runs some of the 8 abstract functions in leap.

import time
import grpc
import concurrent.futures as futures
import json
import logging
import pickle
from pylogrus import PyLogrus, TextFormatter, JsonFormatter
import utils.env_manager as env_manager

from proto import cloud_algos_pb2_grpc
from proto import computation_msgs_pb2
from proto import coordinator_pb2_grpc

class CloudAlgo():
    def __init__(self, config_path):
        self.config = self.get_config(config_path)

        # Setup logging tool
        logging.setLoggerClass(PyLogrus)
        logger = logging.getLogger(__name__)  # type: PyLogrus
        logger.setLevel(logging.DEBUG)
        
        formatter = TextFormatter(datefmt='Z', colorize=True)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        
        jsonformatter = JsonFormatter(datefmt='Z')
        fh = logging.FileHandler("logs/cloudalgo.log", 'w+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(jsonformatter)
        
        logger.addHandler(ch)
        logger.addHandler(fh)
        self.log = logger.withFields({"node": "cloud-algo"})
           

    # Loads the file with the configurations for the cloud algo
    #
    # config_path: The file path to the config file
    def get_config(self, config_path):
        with open(config_path) as json_file:
            data = json_file.read()
            config = json.loads(data)
            return config


    # Starts listening for RPC requests at the specified ip and
    # port.
    #
    # No args
    def serve(self):
        cloudAlgoServicer = CloudAlgoServicer(self.config['ip_port'], self.config['coordinator_ip_port'], self.config, self.log)
        maxMsgLength = 1024 * 1024 * 1024
        opts = [("grpc.keepalive_time_ms", 5000), 
                ("grpc.keepalive_timeout_ms", 1000), 
                ("grpc.keepalive_permit_without_calls", True),
                ("grpc.http2.max_ping_strikes", 0)]
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=opts)

        if self.config["secure_with_tls"] == "y":
            fd = open(self.config["cert"], "rb")
            cloudAlgoServicer.cert = fd.read()
            fd = open(self.config["key"], "rb")
            cloudAlgoServicer.key = fd.read()
            fd = open(self.config["certificate_authority"], "rb")
            cloudAlgoServicer.ca = fd.read()

            creds = grpc.ssl_server_credentials(((cloudAlgoServicer.key, cloudAlgoServicer.cert), ), root_certificates=cloudAlgoServicer.ca)
            cloud_algos_pb2_grpc.add_CloudAlgoServicer_to_server(cloudAlgoServicer, server)
            server.add_secure_port(self.config["ip_port"], creds)
        else:
            cloud_algos_pb2_grpc.add_CloudAlgoServicer_to_server(cloudAlgoServicer, server)
            server.add_insecure_port((self.config["ip_port"]))

        server.start()
        self.log.info("Server started")
        self.log.withFields({"ip-port": self.config["ip_port"]}).info("Listening for requests")
        while True:
            time.sleep(5)


# GRPC service for cloud algos
class CloudAlgoServicer(cloud_algos_pb2_grpc.CloudAlgoServicer):
    def __init__(self, ip_port, coordinator_ip_port, config, log):
        self.id_count = 0
        self.live_requests = {}
        self.ip_port = ip_port
        self.coordinator_ip_port = coordinator_ip_port
        self.config = config
        self.cert = None
        self.key = None
        self.ca = None
        self.log = log


    # Coordinates computations across multiple local sites and returns result to client
    #   req["module"]: stringified python module containing
    #     * map_fn: a list of map(data, site_state) that returns local computations at each iteration
    #     * agg_fn: a list of agg(map_results, cloud_state) used to aggregate results from each site
    #     * update_fn: a list of update(agg_result, site_state, cloud_state) used to update the site and cloud states
    #     * choice_fn(site_state): selects the appropriate map/agg_fn depending on the state
    #     * stop_fn(agg_result, site_state, cloud_state): returns true if stopping criterion is met
    #     * post_fn(agg_result, site_state, cloud_state): final processing of the aggregated result to return to client
    #     * data_prep(data): converts standard data schema from each site to be compatible with map_fn
    #     * prep(site_state): initialization for the cloud
    #     * site_state: state that is passed to the sites
    #     * cloud_state: state that is only used by the cloud
    #
    #   req["filter"]: query filter string to get dataset of interest


    # Grpc service call for the cloud algo to compute some
    # algorithm.
    #
    # request: The algorithm to be computed
    # context: Grpc boilerplate
    def Compute(self, request, context):
        self.log.withFields({"request-id": request.id}).info("Received a computation request.")
        try:
            req = json.loads(request.req)
            sites = request.sites

            leap_type = request.leap_type
            if leap_type == computation_msgs_pb2.LeapTypes.UDF:
                env = env_manager.CloudUDFEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.LAPLACE_UDF:
                env = env_manager.CloudUDFEnvironment() # LaplaceUDF does not change cloud api logic
            elif leap_type == computation_msgs_pb2.LeapTypes.EXPONENTIAL_UDF:
                env = env_manager.CloudUDFEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.PREDEFINED:
                env = env_manager.CloudPredefinedEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.PRIVATE_PREDEFINED:
                env = env_manager.CloudPrivatePredefinedEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.FEDERATED_LEARNING:
                env = env_manager.CloudFedereatedLearningEnvironment()
            
            env.set_env(globals(), req, request.id, request)

            result, eps, delt = self._compute_logic(req, sites, request)
        
            res = computation_msgs_pb2.ComputeResponse()
            res.response = json.dumps(result)
            if 'epsilon' in req:
                res.eps = eps
                res.private = True
            if 'delta' in req:
                res.delt = delt
                res.private = True

        except grpc.RpcError as e:
            self.log.withFields({"request-id": request.id}).error(e.details())
            raise e
        except BaseException as e:
            self.log.withFields({"request-id": request.id}).error(e)
            raise e

        return res


    # Takes a request and the state and creates a request to
    # be sent to the coordinator that grpc understands.
    #
    # req_body: The body of the request containing the functions
    #           to be executed.
    # state: The state that will go in the request.
    # sites: The sites to be queries
    # req: Protobuf request
    def _create_map_request(self, req_body, state, sites, req):
        request = computation_msgs_pb2.MapRequest()
        req_body = req_body.copy()
        req_body["state"] = state
        request.req = json.dumps(req_body)
        request.id = req.id
        request.leap_type = req.leap_type
        request.algo_code = req.algo_code
        request.sites.extend(sites)

        return request

    # Gets the grpc stub to send a message to the coordinator.
    def _get_coord_stub(self):
        channel = None 
        opts = [("grpc.keepalive_time_ms", 10000), ("grpc.keepalive_timeout_ms", 1000), ("grpc.keepalive_permit_without_calls", True)]
        maxMsgLength = 271000000 
        if self.config["secure_with_tls"] == "y":
            creds = grpc.ssl_channel_credentials(root_certificates=self.ca, private_key=self.key, certificate_chain=self.cert)
            opts.append(('grpc.ssl_target_name_override', self.config["coord_cn"]))
            channel = grpc.secure_channel(self.coordinator_ip_port, creds, 
                    options=opts)
        else:
            channel = grpc.insecure_channel(self.coordinator_ip_port, options=opts)
       
        coord_stub = coordinator_pb2_grpc.CoordinatorStub(channel)
        return coord_stub


    # Extracts map responses from a stream
    #
    # chunks: Stream of chunks from grpc call
    def _extract_chunks(self, chunks):
        buf = bytes() 
        
        for chunk in chunks:
            buf += chunk.chunk

        responses = computation_msgs_pb2.MapResponses()
        responses.ParseFromString(buf)
        return responses 

    def _get_chunks_to_send(self, request):
        chunk_size = 64 * 1024
        buf = request.SerializeToString()
        chunks = []
        for curr_byte in range(0, len(buf), chunk_size):
            if curr_byte + chunk_size > len(buf):
                chunk = computation_msgs_pb2.MapRequestChunk()
                chunk.chunk = buf[curr_byte: len(buf)]
                chunks.append(chunk)
            else:
                chunk = computation_msgs_pb2.MapRequestChunk()
                chunk.chunk = buf[curr_byte: curr_byte + chunk_size]
                chunks.append(chunk)
        
        return chunks

    def _generate_chunk_iterator(self, chunks):
        for chunk in chunks:
            yield chunk
        

    # Contains the logic for aggregating and performing the
    # general algorithmic portion of Leap that happens in the
    # cloud.
    #
    # req: The request from a client.
    # req_id: The id of the request.
    # coord_stub: The stub used to send a message to the
    #             coordinator.
    # sites: The sites where the map function will run
    def _compute_logic(self, req_body, sites, req):
        state = init_state_fn()
        stop = False
        eps = 0
        delt = 0
    
        
        while not stop:
            currTime = time.time_ns()
            self.log.withFields({"request-id": req.id, "unix-nano": currTime}).info("StartIter")
            map_results = []
            # Choose which map/agg/update_fn to use
            choice = choice_fn(state)
            site_request = self._create_map_request(req_body, state, sites, req)
            # Get result from each site through coordinator
            coord_stub = self._get_coord_stub()
            chunks = self._get_chunks_to_send(site_request) 
            chunk_iterator = self._generate_chunk_iterator(chunks)
            results = coord_stub.Map(chunk_iterator)
            results = self._extract_chunks(results)
            eps, delt = self.accumulate_priv_values(req_body, eps, delt, len(results.responses))
            extracted_responses = self._extract_map_responses(results.responses)
            # Aggregate results from each site
            agg_result = agg_fn[choice](extracted_responses)
            # Update the state
            state = update_fn[choice](agg_result, state)
            # Decide to stop or continue
            currTime = time.time_ns()
            self.log.withFields({"request-id": req.id, "unix-nano": currTime}).info("ValStart")
            acc = self.get_validation_loss()
            currTime = time.time_ns()
            self.log.withFields({"request-id": req.id, "unix-nano": currTime}).info("ValEnd")
            self.log.withFields({"request-id": req.id, "accuracy": float(acc)}).info("Acc")
            currTime = time.time_ns()
            self.log.withFields({"request-id": req.id, "unix-nano": currTime}).info("EndIter")
            stop = stop_fn(agg_result, state)
         
        post_result = postprocessing_fn(agg_result, state)
     
        return post_result, eps, delt

    def accumulate_priv_values(self, req, eps, delt, num_results):
        if 'epsilon' in req:
            eps += req['epsilon'] * num_results
        if 'delta' in req:
            delt += req['delta'] * num_results
        return eps, delt

    
    def get_validation_loss(self):
        _, dataloader_val = get_dataloader(hyperparams, [])
        val_loss = self.measure_acc(dataloader_val, model)
        return val_loss
   

    def measure_acc(self, dataloader, ml_model):
        with torch.no_grad():
            val_sum = 0
            val_total = 0
            for i, (X, Y) in enumerate(dataloader, 0):
                target = Y
                image = X
        
                output = ml_model(image)
                correct_sum, total = self.acc_sum(output, target)
                val_sum += correct_sum
                val_total += total
            print("Acc: " + str(val_sum / val_total))
            return val_sum / val_total
    
    def acc_sum(self, pred, target):
        with torch.no_grad():
            pred_softmax = torch.log_softmax(pred, dim=1)
            _, pred_tags = torch.max(pred_softmax, dim=1)
            correct_pred = (pred_tags == target).float()
            return correct_pred.sum(), len(correct_pred)
        
    
    # Extracts the protobuf responses into a list.
    #
    # pb_responses: Response message from protobuf.
    def _extract_map_responses(self, pb_responses):
        responses = []
        for r in pb_responses:
            responses.append(r.response)
        return responses
