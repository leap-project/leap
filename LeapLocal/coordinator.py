import pdb
from localsite import SiteResponse
""" Local implementation of coordinator
Delegates compute request to local sites
"""

class CoordinatorResponse():
    def __init__(self):
        self.responses = []

class LocalCoordinator():
    def __init__(self, sites):
        self.sites = sites
    
    def Map(self, site_request):
        agg_result = []
        for site in self.sites:
            site_response = site.Map(site_request, None)
            agg_result.append(site_response)
        coord_response = CoordinatorResponse()
        coord_response.responses = agg_result
        return coord_response