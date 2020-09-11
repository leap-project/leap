# This file contains the code for the server that listens
# to requests from a coordinator. It also operates the logic
# for running the algorithms.
#
# - config: The path to the config file for the site algo
#


import grpc
import time
import pandas
import concurrent.futures as futures
import redcap
import json
import logging
from pylogrus import PyLogrus, TextFormatter
import utils.env_manager as env_manager
import cloudalgo.functions.privacy as leap_privacy
import csv
import requests
import numpy as np

import proto as pb
from proto import site_algos_pb2_grpc
from proto import computation_msgs_pb2
from proto import availability_msgs_pb2
from proto import selector_verification_msgs_pb2
from sitealgo import rc_sql_gen, codes

# Setup logging tool
logging.setLoggerClass(PyLogrus)
logger = logging.getLogger(__name__) 
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

# Class for starting a site algo
class SiteAlgo():

    def __init__(self, config_path):
        self.config = self.get_config(config_path)


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
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        cert = None
        key = None
        ca = None

        # If secure flag is on only run encrypted connections
        if self.config["secure_with_tls"] == "y":
            fd = open(self.config["cert"], "rb")
            cert = fd.read()
            fd = open(self.config["key"], "rb")
            key = fd.read()
            fd = open(self.config["certificate_authority"], "rb")
            ca = fd.read()

            creds = grpc.ssl_server_credentials(((key, cert), ), root_certificates=ca)
            site_algos_pb2_grpc.add_SiteAlgoServicer_to_server(SiteAlgoServicer(self.config["ip_port"], self.config["connector_ip_port"], self.config), server)
            server.add_secure_port(self.config["ip_port"], creds)
        else:
            site_algos_pb2_grpc.add_SiteAlgoServicer_to_server(SiteAlgoServicer(self.config["ip_port"], self.config["connector_ip_port"], self.config), server)
            server.add_insecure_port(self.config["ip_port"])

        server.start()
        log.info("Server started")
        log.info("Listening at " + self.config["ip_port"])
        while True:
            time.sleep(5)



# RPC Service for Site Algos
class SiteAlgoServicer(site_algos_pb2_grpc.SiteAlgoServicer):
    def __init__(self, ip_port, connector_ip_port, config):
        self.ip_port = ip_port
        self.connector_ip_port = connector_ip_port
        self.config = config
        self.live_requests = {}
        self.localDataCache = {}


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
            leap_type = request.leap_type
            if leap_type == computation_msgs_pb2.LeapTypes.UDF:
                env = env_manager.SiteUDFEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.LAPLACE_UDF:
                env = env_manager.SiteUDFEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.EXPONENTIAL_UDF:
                env = env_manager.SiteExponentialUDFEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.PREDEFINED:
                env = env_manager.SitePredefinedEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.PRIVATE_PREDEFINED:
                env = env_manager.SitePrivatePredefinedEnvironment()
            elif leap_type == computation_msgs_pb2.LeapTypes.FEDERATED_LEARNING:
                env = env_manager.SiteFederatedLearningEnvironment()
            env.set_env(globals(), req, request.id, request)
            log.withFields({"request-id": request.id}).info("Loaded all necessary environment")
            map_result = self.map_logic(request)
            res = self._get_response_obj()
            res.response = map_result
            self.live_requests.pop(request.id)
            return res
        except BaseException as e:
            log.withFields({"request-id": request.id}).error(e)
            raise e


    # RPC asking if site algo is available. Returns site
    # available response when pinged.
    #
    # request: A protobuf checking for availability
    # context: Boilerplate for grpc containing the context
    #          of the RPC."""
    def SiteAvailable(self, request, context):
        log.info("Received request checking for availability")
        res = availability_msgs_pb2.SiteAvailableRes()
        res.site.available = True
        return res

    # This function implements selector validation.
    # See api/selector_verification_example.py
    #
    # request: A protobuf with a selector to verify
    # context: Boilerplate for grpc containing the context
    #          of the RPC.
    def VerifySelector(self, request, context):
        log.info("Recieved request to verify selector")
        res = selector_verification_msgs_pb2.SelectorVerificationRes()
        res.siteId = request.siteId
        selector = request.selector
        if (request.isSelectorString): 
            #TODO: test string for valid REDCap getData filter format
            res.success = True
            res.error = "None - selector is a string"
        else:
            try:
                selector_object = json.loads(selector)
            except ValueError as e:
                res.success = False
                res.error = "Invalid JSON encoding, check for special characters"

            if selector_object["type"] == codes.SQL:
                gen_fn = rc_sql_gen.generator_map[selector_object["sql_func"]](selector_object["sql_options"])
                validation_res = gen_fn["validate"]()
                res.success = validation_res["valid"]
                if res.success:
                    res.error = "None"
                else:
                    res.error = validation_res["error"] 

            elif selector_object["type"] == codes.DEFAULT:
                if ("filter" in selector_object) and (type(selector_object["filter"]) != "string"):
                    res.success = False
                    res.error = "filter must be a correctly formatted string"
                elif "fields" in selector_object:
                    if (type(selector_object["fields"]) == "list") and (not (all(isinstance(item, str) for item in selector_object["fields"]))):
                        res.success = False
                        res.error = "all field names must be string values"
                    elif (type(selector_object["fields"]) != "string"):
                        res.success = False
                        res.error = "fields is not a list or a string"
            else:
                res.success = False
                res.error = "Type of selector is invalid"
        return res
        
    # Gets the protobuf message for a map response
    #
    # No args
    def _get_response_obj(self):
        return computation_msgs_pb2.MapResponse()


    # Chooses the appropriate map function to run, gets the
    # data, and computes the map function on the data.
    #
    # request: Request containing the functions to be run.
    def map_logic(self, request):
        req_id = request.id
        req = json.loads(request.req)
        
        state = req["state"]
                
        choice = choice_fn(state)
        data = self.get_data(req_id, req)
        if 'dataprep_fn' in globals():
            log.withFields({"request-id": req_id}).info("Applying dataprep func")
            data = dataprep_fn(data)
        
        # Adding logic for private udf functions
        leap_type = request.leap_type
        if leap_type == computation_msgs_pb2.LeapTypes.LAPLACE_UDF:
            # Compute sensitivity: maximum difference in score function
            epsilon = req["epsilon"]
            delta = req["delta"]
            target_attribute = req["target_attribute"]
            map_result = leap_privacy.dynamic_laplace(epsilon, delta, target_attribute, map_fn[choice], data, state)
        elif leap_type == computation_msgs_pb2.LeapTypes.EXPONENTIAL_UDF:
            epsilon = req["epsilon"]
            delta = req["delta"]
            target_attribute = req["target_attribute"]
            map_result = leap_privacy.exponential(epsilon, delta, target_attribute, score_fn[choice], data, state)
        else:
            log.withFields({"request-id": req_id}).info("Applying map func")
            map_result = map_fn[choice](data, state)
        return map_result


    # Gets the data from the database
    #
    # req_id: Request ID of leap request
    # req: A leap request containing the selector to retrieve
    #      the data.
    def get_data(self, req_id, req):
        selector = req["selector"]

        # Note: this is only for old examples
        if (type(selector) == str):
            return pandas.read_csv("data.csv")

        useLocalData = ("useLocalData" in selector.keys()) and (selector["useLocalData"])
        if useLocalData and ("data"+str(req_id) in self.localDataCache.keys()):
            data = self.localDataCache["data"+str(req_id)]
        else:
            data = self.get_data_from_src(selector)
            if useLocalData:
                self.localDataCache["data"+str(req_id)] = data
        return data


    # Gets the data from a database or csv file and returns
    # the records to perform a computation on.
    #
    # selector: the options for retrieving data from the request
    def get_data_from_src(self, selector):
        if self.config["csv_true"] == "1" or selector["type"] == "csv":
            return self.get_csv_data(selector)
        else:
            return self.get_redcap_data(redCapUrl, redCapToken, selector)


    # Gets data from a CSV file. If the selector contains 
    # a source, then use that, else use the default data file.
    #
    # selector: the options for retrieving data from the request
    def get_csv_data(self, selector):
        # if a custom source is provied, use that
        if ("src" in selector.keys()):
            url = selector["src"]
            data = pandas.read_csv(url)
        else:
            data = pandas.read_csv("data.csv")
        return data


    # Contacts a redCap project and returns the filtered records
    # from this project
    #
    # url: Url of the RedCap project
    # token: Token used to access RedCap project given in the url
    # selector: the full selector object from the request
    def get_redcap_data(self, url, token, selector):
        if selector["type"] == "default":
            return self.get_redcap_data_result(selector.get("filter", ""), selector.get("fields", ""))
        elif selector["type"] == "sql":
            query_gen_func = rc_sql_gen.generator_map[selector["sql_func"]](selector["sql_options"])
            query = query_gen_func["generate"]()
            return self.get_redcap_query_result(query)
        return None

    # Contacts a redCap project and returns the filtered records
    # from this project
    #
    # filter_logic: The filter to be applied to the results.
    # selected_fields: A list of fields (table columns) to retrieve from REDCap.
    def get_redcap_data_result(self, filter_logic = "", selected_fields = ""):
        # Use the external module to get filtered data
        log.info("Getting data from REDCap")
        url = self.config["redcap_url"] + "/?type=module&prefix=leap_connector&NOAUTH&page=getData"
        form_data = {'auth': self.config["redcap_auth"], 'pid': self.config["redcap_pid"], 'filters': filter_logic, 'fields': selected_fields}
        r = requests.post(url, data = form_data)
        jsondata = json.loads(r.text)

        # if successful, return data as a dataframe
        if (jsondata['success'] == True):
            df = pandas.DataFrame(jsondata['data'])
            df = df.dropna().infer_objects()
            log.info("Successfully retrieved data from REDCap")
            return df
        
        # if it failed, return None
        log.error("Failed to retrieve data from REDCap:")
        log.error(jsondata["error"])
        return None

    # Runs the query on REDCap and gets the result of the query as a dataframe
    #
    # query: the SQL query that will run on REDCap
    def get_redcap_query_result(self, query):
        log.info("Getting data from REDCap query")

        url = self.config["redcap_url"] + "/?type=module&prefix=leap_connector&NOAUTH&page=getQueryResult"
        form_data = {'auth': self.config["redcap_auth"], 'query': query}
        r = requests.post(url, data = form_data)
        jsondata = json.loads(r.text)

        # if successful, return data as a dataframe
        if (jsondata['success'] == True):
            df = pandas.DataFrame(jsondata['data'])
            log.info("Successfully executed SQL query and retrieved data from REDCap")
            return df
        
        log.error("Failed to query REDCap:")
        log.error(jsondata["error"])
        return None