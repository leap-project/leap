# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import computation_msgs_pb2 as proto_dot_computation__msgs__pb2


class CloudAlgoStub(object):
    """RPC service at a cloud algo that performs the necessary computation.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Compute = channel.unary_unary(
                '/proto.CloudAlgo/Compute',
                request_serializer=proto_dot_computation__msgs__pb2.ComputeRequest.SerializeToString,
                response_deserializer=proto_dot_computation__msgs__pb2.ComputeResponse.FromString,
                )


class CloudAlgoServicer(object):
    """RPC service at a cloud algo that performs the necessary computation.
    """

    def Compute(self, request, context):
        """Performs the appropriate computation at the host algo and returns the result.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CloudAlgoServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Compute': grpc.unary_unary_rpc_method_handler(
                    servicer.Compute,
                    request_deserializer=proto_dot_computation__msgs__pb2.ComputeRequest.FromString,
                    response_serializer=proto_dot_computation__msgs__pb2.ComputeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.CloudAlgo', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CloudAlgo(object):
    """RPC service at a cloud algo that performs the necessary computation.
    """

    @staticmethod
    def Compute(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.CloudAlgo/Compute',
            proto_dot_computation__msgs__pb2.ComputeRequest.SerializeToString,
            proto_dot_computation__msgs__pb2.ComputeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)