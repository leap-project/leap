# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import availability_msgs_pb2 as proto_dot_availability__msgs__pb2
from proto import computation_msgs_pb2 as proto_dot_computation__msgs__pb2
from proto import selector_verification_msgs_pb2 as proto_dot_selector__verification__msgs__pb2


class SiteConnectorStub(object):
    """RPC service at a site connector that will handle requests from site algorithms
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Map = channel.stream_stream(
                '/proto.SiteConnector/Map',
                request_serializer=proto_dot_computation__msgs__pb2.MapRequestChunk.SerializeToString,
                response_deserializer=proto_dot_computation__msgs__pb2.MapResponseChunk.FromString,
                )
        self.SiteAvailable = channel.unary_unary(
                '/proto.SiteConnector/SiteAvailable',
                request_serializer=proto_dot_availability__msgs__pb2.SiteAvailableReq.SerializeToString,
                response_deserializer=proto_dot_availability__msgs__pb2.SiteAvailableRes.FromString,
                )
        self.VerifySelector = channel.unary_unary(
                '/proto.SiteConnector/VerifySelector',
                request_serializer=proto_dot_selector__verification__msgs__pb2.SelectorVerificationReq.SerializeToString,
                response_deserializer=proto_dot_selector__verification__msgs__pb2.SelectorVerificationRes.FromString,
                )


class SiteConnectorServicer(object):
    """RPC service at a site connector that will handle requests from site algorithms
    """

    def Map(self, request_iterator, context):
        """Relays a computation request from the coordinator to appropriate algorithm in site
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SiteAvailable(self, request, context):
        """Pinged by the coordinator to determine whether a site is available
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifySelector(self, request, context):
        """Sends a request to the site to verify the selector
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SiteConnectorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Map': grpc.stream_stream_rpc_method_handler(
                    servicer.Map,
                    request_deserializer=proto_dot_computation__msgs__pb2.MapRequestChunk.FromString,
                    response_serializer=proto_dot_computation__msgs__pb2.MapResponseChunk.SerializeToString,
            ),
            'SiteAvailable': grpc.unary_unary_rpc_method_handler(
                    servicer.SiteAvailable,
                    request_deserializer=proto_dot_availability__msgs__pb2.SiteAvailableReq.FromString,
                    response_serializer=proto_dot_availability__msgs__pb2.SiteAvailableRes.SerializeToString,
            ),
            'VerifySelector': grpc.unary_unary_rpc_method_handler(
                    servicer.VerifySelector,
                    request_deserializer=proto_dot_selector__verification__msgs__pb2.SelectorVerificationReq.FromString,
                    response_serializer=proto_dot_selector__verification__msgs__pb2.SelectorVerificationRes.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'proto.SiteConnector', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SiteConnector(object):
    """RPC service at a site connector that will handle requests from site algorithms
    """

    @staticmethod
    def Map(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/proto.SiteConnector/Map',
            proto_dot_computation__msgs__pb2.MapRequestChunk.SerializeToString,
            proto_dot_computation__msgs__pb2.MapResponseChunk.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SiteAvailable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.SiteConnector/SiteAvailable',
            proto_dot_availability__msgs__pb2.SiteAvailableReq.SerializeToString,
            proto_dot_availability__msgs__pb2.SiteAvailableRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def VerifySelector(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/proto.SiteConnector/VerifySelector',
            proto_dot_selector__verification__msgs__pb2.SelectorVerificationReq.SerializeToString,
            proto_dot_selector__verification__msgs__pb2.SelectorVerificationRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
