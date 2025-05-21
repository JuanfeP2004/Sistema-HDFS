import grpc
import commands_pb2
import commands_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)
        #response = stub.Mkdir(commands_pb2.CommandRequest(parameter = 'volumen42'))
        #response = stub.Rmdir(commands_pb2.CommandRequest(parameter = ''))
        #response = stub.List(commands_pb2.CommandRequest(parameter = 'volumen2'))
        #response = stub.Access(commands_pb2.CommandRequest(parameter = 'volumen2/'))
        #response = stub.Get(commands_pb2.CommandRequest(parameter = 'volumen2/imagen.png'))
        #response = stub.Remove(commands_pb2.CommandRequest(parameter = 'volumen2/imagen.png'))
        #response = stub.Add(commands_pb2.CommandRequest(parameter = 'volumen2/tarea.docx?62'))
        #print("Respuesta del servidor:", response.message)

        response = ''
        response += stub.Add(commands_pb2.CommandRequest(parameter = 'volumen2/tarea.docx?262')).message
        response += stub.Add(commands_pb2.CommandRequest(parameter = 'volumen2/imagen.png?1024')).message
        response += stub.Add(commands_pb2.CommandRequest(parameter = 'volumen/exposicion.pptx?3000')).message
        print("Respuesta del servidor:", response)

#Access, Add, Remove, Get, List, MKdir, Rmdir
if __name__ == '__main__':
    run()
