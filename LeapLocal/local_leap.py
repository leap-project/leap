import pdb 
import utils
import json

class CloudRequest():
    def __init__(self):
        self.req = None

from LeapApi import leap

class LocalLeap(leap.Leap):
    def __init__(self, cloud):
        super().__init__()
        self.cloud = cloud
    def _create_computation_request(self, filter):
        request = CloudRequest()
        req = self._create_json_req(filter)
        request.req = json.dumps(req)
        return request

    def send_request(self, filter):
        request = self._create_computation_request(filter)
        result = self.cloud.Compute(request)
        print("Received response")
            
        if hasattr(result, "err"):
            print(result.err)
        return result
