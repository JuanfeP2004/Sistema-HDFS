from concurrent import futures
import grpc
import node_pb2
import node_pb2_grpc

import os
import sys

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )

from funciones.WGetInfo import GetInfo
from funciones.WGet import Get
from funciones.WPut import Put
from funciones.WRemove import Remove
from replica.Wclient import ReplicatePut, ReplicateRemove

class CommandsWorkService(node_pb2_grpc.CommandsWorkServicer):
    def GetInfo(self, request, context):
        msg = GetInfo()
        return node_pb2.CommandReplyWork(message=msg)
    
    def Get(self, request, context):
        msg = Get(request.parameter)
        return node_pb2.CommandReplyWork(message=msg)
    
    def Put(self, request, context):
        msg = Put(request.parameter)
        return node_pb2.CommandReplyWork(message=msg)

    def Remove(self, request, context):
        msg = Remove(request.parameter)
        return node_pb2.CommandReplyWork(message=msg)
    
    def ReplicatePut(self, request, context):
        msg = ReplicatePut(request.parameter)
        return node_pb2.CommandReplyWork(message=msg)
    
    def ReplicateRemove(self, request, context):
        msg = ReplicateRemove(request.parameter)
        return node_pb2.CommandReplyWork(message=msg)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node_pb2_grpc.add_CommandsWorkServicer_to_server(CommandsWorkService(), server=server)
    server.add_insecure_port('[::]:50051') #Cambiar a 50051 en produccion
    print("Servidor gRPC corriendo...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()