# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import snitch_pb2 as snitch__pb2


class SnitchStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SnitchUser = channel.unary_unary(
                '/snitch.Snitch/SnitchUser',
                request_serializer=snitch__pb2.Message.SerializeToString,
                response_deserializer=snitch__pb2.MessageResponse.FromString,
                )


class SnitchServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SnitchUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SnitchServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SnitchUser': grpc.unary_unary_rpc_method_handler(
                    servicer.SnitchUser,
                    request_deserializer=snitch__pb2.Message.FromString,
                    response_serializer=snitch__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'snitch.Snitch', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Snitch(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SnitchUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/snitch.Snitch/SnitchUser',
            snitch__pb2.Message.SerializeToString,
            snitch__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
