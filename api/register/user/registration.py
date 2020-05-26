import grpc
import proto
from proto import user_msgs_pb2
from proto import coordinator_pb2_grpc


def register_user(username, password, coordinator_ip_port, secure=False, key=None, cert=None, ca=None, coord_cn=None):
    channel = None

    if secure:
        creds = grpc.ssl_channel_credentials(root_certificates=ca, private_key=key, certificate_chain=cert)
        channel = grpc.secure_channel(coordinator_ip_port, creds, options=(('grpc.ssl_target_name_override', coord_cn,),))
    else:
        channel = grpc.insecure_channel(coordinator_ip_port)

    coord_stub = coordinator_pb2_grpc.CoordinatorStub(channel)
    user_registration_req = user_msgs_pb2.UserRegReq()
    user_registration_req.user.username = username
    user_registration_req.user.password = password
    res = coord_stub.RegisterUser(user_registration_req)
    return res

def authenticate_user(username, password, coordinator_ip_port, secure=False, key=None, cert=None, ca=None, coord_cn=None):
    channel = None

    if secure:
        creds = grpc.ssl_channel_credentials(root_certificates=ca, private_key=key, certificate_chain=cert)
        channel = grpc.secure_channel(coordinator_ip_port, creds, options=(('grpc.ssl_target_name_override', coord_cn,),))
    else:
        channel = grpc.insecure_channel(coordinator_ip_port)

    coord_stub = coordinator_pb2_grpc.CoordinatorStub(channel)
    user_authentication_req = user_msgs_pb2.UserAuthReq()
    user_authentication_req.user.username = username
    user_authentication_req.user.password = password
    res = coord_stub.AuthUser(user_authentication_req)

    return res