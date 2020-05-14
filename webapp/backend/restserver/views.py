from django.http import Http404
from django.http import HttpResponse

from rest_framework.views import APIView
from api.availability.available import get_available_sites

import json
import api.leap as leap
import api.leap_fn as leap_fn
import api.codes as codes

config = None
with open("../../config/webapp_config.json") as json_file:
    data = json_file.read()
    config = json.loads(data)

class ComputeView(APIView):
    """
    API endpoint that sends requests from the web portal to
    the LEAP infrastructure.
    """
    def post(self, request, format=None):
        leap_predef = None
        body = json.loads(request.body)
        if body['dp']:
            leap_predef = leap_fn.PrivatePredefinedFunction(codes.PRIVATE_SITE_COUNT_ALGO, epsilon=1, delta=0)
        else:
            leap_predef = leap_fn.PredefinedFunction(codes.COUNT_ALGO)

        leap_predef.selector = body['selector']

        dist_leap = leap.DistributedLeap(leap_predef)
        result = dist_leap.get_result()
        return HttpResponse(result)

class SitesView(APIView):
    """
    API endpoint that gets information about the sites registered
    in LEAP.
    """
    def get(self, request, format=None):
        sites = get_available_sites(config["coordinator_ip_port"])
        list_of_sites = {'sites': []}
        for res in sites.responses:
            if res.site.available:
                parsed_site = {'site_id': res.site.site_id, 'available': True}
            else:
                parsed_site = {'site_id': res.site.site_id, 'available': False}

            list_of_sites['sites'].append(parsed_site)
        list_of_sites = json.dumps(list_of_sites)
        return HttpResponse(list_of_sites)
