import pdb
import json

from CloudAlgo.cloud_algo import CloudAlgoServicer
from LeapLocal.localsite import SiteResponse
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

    def _get_coord_stub(self):
        return self.coord

    def _get_response_obj(self):
        return SiteResponse()

