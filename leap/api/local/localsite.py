# The class that defines a local site in LEAP.

import pdb
import pandas as pd
import json
import numpy as np
from sitealgo.site_algo import SiteAlgoServicer


class SiteResponse:
    def __init__(self):
        self.response = None


class LocalSiteAlgoServicer(SiteAlgoServicer):
    def __init__(self, site_id):
        self.live_requests = {}
        self.site_id = site_id

    def _get_response_obj(self):
        return SiteResponse()


if __name__=="__main__":
    pdb.set_trace()
