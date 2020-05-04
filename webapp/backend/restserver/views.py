from django.http import Http404

# from django.conf import settings
# import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import api.leap as leap
import api.leap_fn as leap_fn
import api.codes as codes
import cloudalgo.functions as cloud_functions

class ComputeView(APIView):
    """
    API endpoint that sends requests from the web portal to
    the LEAP infrastructure.
    """
    def post(self, request, format=None):
        leap_predef = None
        if request.dp:
            leap_predef = leap_fn.PrivatePredefinedFunction(codes.PRIVATE_SITE_COUNT_ALGO, epsilon=1, delta=0)
        else:
            leap_predef = leap_fn.PredefinedFunction(codes.COUNT_ALGO)

            selector = "[age] > 50 and [bmi] < 25"
            leap_predef.selector = selector
            dist_leap = leap.DistributedLeap(leap_predef)
            print(dist_leap.get_result())

        return Response(status=status.HTTP_200_OK)

class SitesView(APIView):
    """
    API endpoint that gets information about the sites registered
    in LEAP.
    """

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)
