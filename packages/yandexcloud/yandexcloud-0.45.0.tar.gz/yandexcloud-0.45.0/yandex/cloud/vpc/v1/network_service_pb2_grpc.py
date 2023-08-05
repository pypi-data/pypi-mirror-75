# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud.vpc.v1 import network_pb2 as yandex_dot_cloud_dot_vpc_dot_v1_dot_network__pb2
from yandex.cloud.vpc.v1 import network_service_pb2 as yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2


class NetworkServiceStub(object):
  """A set of methods for managing Network resources.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Get = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/Get',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.GetNetworkRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__pb2.Network.FromString,
        )
    self.List = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/List',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworksRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworksResponse.FromString,
        )
    self.Create = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/Create',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.CreateNetworkRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.Update = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/Update',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.UpdateNetworkRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.Delete = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/Delete',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.DeleteNetworkRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )
    self.ListSubnets = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/ListSubnets',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkSubnetsRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkSubnetsResponse.FromString,
        )
    self.ListOperations = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/ListOperations',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkOperationsRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkOperationsResponse.FromString,
        )
    self.Move = channel.unary_unary(
        '/yandex.cloud.vpc.v1.NetworkService/Move',
        request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.MoveNetworkRequest.SerializeToString,
        response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
        )


class NetworkServiceServicer(object):
  """A set of methods for managing Network resources.
  """

  def Get(self, request, context):
    """Returns the specified Network resource.

    Get the list of available Network resources by making a [List] request.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def List(self, request, context):
    """Retrieves the list of Network resources in the specified folder.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Create(self, request, context):
    """Creates a network in the specified folder using the data specified in the request.
    Method starts an asynchronous operation that can be cancelled while it is in progress.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Update(self, request, context):
    """Updates the specified network.
    Method starts an asynchronous operation that can be cancelled while it is in progress.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Delete(self, request, context):
    """Deletes the specified network.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListSubnets(self, request, context):
    """Lists subnets from the specified network.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListOperations(self, request, context):
    """Lists operations for the specified network.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Move(self, request, context):
    """Move network to another folder.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_NetworkServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Get': grpc.unary_unary_rpc_method_handler(
          servicer.Get,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.GetNetworkRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__pb2.Network.SerializeToString,
      ),
      'List': grpc.unary_unary_rpc_method_handler(
          servicer.List,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworksRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworksResponse.SerializeToString,
      ),
      'Create': grpc.unary_unary_rpc_method_handler(
          servicer.Create,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.CreateNetworkRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'Update': grpc.unary_unary_rpc_method_handler(
          servicer.Update,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.UpdateNetworkRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'Delete': grpc.unary_unary_rpc_method_handler(
          servicer.Delete,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.DeleteNetworkRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
      'ListSubnets': grpc.unary_unary_rpc_method_handler(
          servicer.ListSubnets,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkSubnetsRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkSubnetsResponse.SerializeToString,
      ),
      'ListOperations': grpc.unary_unary_rpc_method_handler(
          servicer.ListOperations,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkOperationsRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.ListNetworkOperationsResponse.SerializeToString,
      ),
      'Move': grpc.unary_unary_rpc_method_handler(
          servicer.Move,
          request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_network__service__pb2.MoveNetworkRequest.FromString,
          response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'yandex.cloud.vpc.v1.NetworkService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
