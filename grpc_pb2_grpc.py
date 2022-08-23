# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import grpc_pb2 as grpc__pb2


class LiveMessagerStub(object):
    """The greeting service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.HandleJsonMsg = channel.unary_unary(
                '/LiveProto.LiveMessager/HandleJsonMsg',
                request_serializer=grpc__pb2.StringMsg.SerializeToString,
                response_deserializer=grpc__pb2.StringMsg.FromString,
                )
        self.ServerStringRouter = channel.stream_stream(
                '/LiveProto.LiveMessager/ServerStringRouter',
                request_serializer=grpc__pb2.StringMsg.SerializeToString,
                response_deserializer=grpc__pb2.StringMsg.FromString,
                )


class LiveMessagerServicer(object):
    """The greeting service definition.
    """

    def HandleJsonMsg(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServerStringRouter(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LiveMessagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'HandleJsonMsg': grpc.unary_unary_rpc_method_handler(
                    servicer.HandleJsonMsg,
                    request_deserializer=grpc__pb2.StringMsg.FromString,
                    response_serializer=grpc__pb2.StringMsg.SerializeToString,
            ),
            'ServerStringRouter': grpc.stream_stream_rpc_method_handler(
                    servicer.ServerStringRouter,
                    request_deserializer=grpc__pb2.StringMsg.FromString,
                    response_serializer=grpc__pb2.StringMsg.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LiveProto.LiveMessager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LiveMessager(object):
    """The greeting service definition.
    """

    @staticmethod
    def HandleJsonMsg(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LiveProto.LiveMessager/HandleJsonMsg',
            grpc__pb2.StringMsg.SerializeToString,
            grpc__pb2.StringMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ServerStringRouter(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/LiveProto.LiveMessager/ServerStringRouter',
            grpc__pb2.StringMsg.SerializeToString,
            grpc__pb2.StringMsg.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
