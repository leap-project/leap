import pdb
import json
import utils

from CloudAlgos.cloud_algo import CloudAlgoServicer

# data template for site request
class SiteRequest():
    def __init__(self):
        self.id = None
        self.req = None

class LocalCloudAlgoServicer(CloudAlgoServicer):
    def __init__(self, coord):
        self.coord = coord
        self.id_count = 0
        self.live_requests = {}

    def _create_computation_request(self, req_id, req, state):
        request = SiteRequest()
        request.id = req_id
        req = req.copy()
        req["state"] = state
        request.req = json.dumps(req)
        return request

    def Compute(self, request):
        post_result = self._compute_logic(request, self.coord)
        return json.dumps(post_result)