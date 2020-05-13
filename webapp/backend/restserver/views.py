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
        return HttpResponse(sites)
