from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ComputeView(APIView):
    """
    API endpoint that sends requests from the web portal to
    the LEAP infrastructure.
    """
    def post(self, request, format=None):
        print("Got POST for compute")
        return Response(status=status.HTTP_200_OK)

class SitesView(APIView):
    """
    API endpoint that gets information about the sites registered
    in LEAP.
    """

    def get(self, request, format=None):
        print("Got GET for sites")
        return Response(status=status.HTTP_200_OK)
