from concurrent import futures
import grpc
import commands_pb2
import commands_pb2_grpc

import os
import sys

ruta_archivo = os.path.dirname( __file__ )
ruta_config = os.path.join( ruta_archivo, '..')
sys.path.append( ruta_config )

from comandos.Hmkdir import hmkdir
from comandos.Hrmdir import hrmdir
from comandos.Hlist import hlist
from comandos.Hget import hget
from comandos.Haccess import haccess
from comandos.Hadd import hadd
from comandos.Hrem import hrem

class CommandsService(commands_pb2_grpc.CommandsServicer):
    def Access(self, request, context):
        msg = haccess(request.parameter)
        return commands_pb2.CommandReply(message=msg)
    
    def Add(self, request, context):
        msg = hadd(request.parameter)
        return commands_pb2.CommandReply(message=msg)
    
    def Get(self, request, context):
        msg = hget(request.parameter)
        return commands_pb2.CommandReply(message=msg)
    
    def List(self, request, context):
        msg = hlist(request.parameter)
        return commands_pb2.CommandReply(message=msg)
    
    def Mkdir(self, request, context):
        msg = hmkdir(request.parameter)
        return commands_pb2.CommandReply(message=msg)
    
    def Remove(self, request, context):
        msg = hrem(request.parameter)
        return commands_pb2.CommandReply(message=msg)
    
    def Rmdir(self, request, context):
        msg = hrmdir(request.parameter)
        return commands_pb2.CommandReply(message=msg)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    commands_pb2_grpc.add_CommandsServicer_to_server(CommandsService(), server=server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC corriendo...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
