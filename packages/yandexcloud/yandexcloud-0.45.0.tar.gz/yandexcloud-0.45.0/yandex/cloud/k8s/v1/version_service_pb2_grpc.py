# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from yandex.cloud.k8s.v1 import version_service_pb2 as yandex_dot_cloud_dot_k8s_dot_v1_dot_version__service__pb2


class VersionServiceStub(object):
  """A set of methods for managing Kubernetes versions.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.List = channel.unary_unary(
        '/yandex.cloud.k8s.v1.VersionService/List',
        request_serializer=yandex_dot_cloud_dot_k8s_dot_v1_dot_version__service__pb2.ListVersionsRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_k8s_dot_v1_dot_version__service__pb2.ListVersionsResponse.FromString,
        )


class VersionServiceServicer(object):
  """A set of methods for managing Kubernetes versions.
  """

  def List(self, request, context):
    """Retrieves the list of versions in the specified release channel.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_VersionServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'List': grpc.unary_unary_rpc_method_handler(
          servicer.List,
          request_deserializer=yandex_dot_cloud_dot_k8s_dot_v1_dot_version__service__pb2.ListVersionsRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_k8s_dot_v1_dot_version__service__pb2.ListVersionsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'yandex.cloud.k8s.v1.VersionService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
