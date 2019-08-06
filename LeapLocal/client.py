import pdb 
import utils
import json

class CloudRequest():
    def __init__(self):
        self.req = None

class Client():
    def __init__(self, cloud):
        self.cloud = cloud        
    
    def send_request(self, u_module):
        filter = "[age] > 50 and [bmi] < 25" # select everything

        request = CloudRequest()
        req = {}
        req["module"] = u_module 
        req["filter"] = filter
        request.req = json.dumps(req)

        result = self.cloud.Compute(request)
        print("Result: {}".format(result))
        return result
