import sys
sys.path.append("../../")
import grpc
from proto import availability_msgs_pb2
from proto import coordinator_pb2_grpc

def get_available_sites(coordinator_ip_port, secure=False, key=None, cert=None, ca=None, coord_cn=None):
    channel = None

    if secure:
        creds = grpc.ssl_channel_credentials(root_certificates=ca, private_key=key, certificate_chain=cert)
        channel = grpc.secure_channel(coordinator_ip_port, creds, options=(('grpc.ssl_target_name_override', coord_cn,),))
    else:
        channel = grpc.insecure_channel(coordinator_ip_port)

    coord_stub = coordinator_pb2_grpc.CoordinatorStub(channel)
    sites_available_req = availability_msgs_pb2.SitesAvailableReq()
    res = coord_stub.SitesAvailable(sites_available_req)
    return res