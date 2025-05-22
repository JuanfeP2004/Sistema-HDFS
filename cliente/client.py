import grpc
import commands_pb2
import commands_pb2_grpc
import node_pb2
import node_pb2_grpc
import subprocess
import glob

'''
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
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = node_pb2_grpc.CommandsStub(channel)
        #response = stub.GetInfo(node_pb2.CommandRequest(parameter = ''))
        #response = stub.Remove(node_pb2.CommandRequest(parameter = 'p00'))
        #response = stub.Put(node_pb2.CommandRequest(parameter = 'p01/auth_image_2f456q-ab'))
        response = stub.Get(node_pb2.CommandRequest(parameter = 'p00'))
        print("Respuesta del servidor:", response.message)

        #response = ''
        #response += stub.Add(node_pb2.CommandRequest(parameter = 'volumen2/tarea.docx?262')).message
        #response += stub.Add(node_pb2.CommandRequest(parameter = 'volumen2/imagen.png?1024')).message
        #response += stub.Add(node_pb2.CommandRequest(parameter = 'volumen/exposicion.pptx?3000')).message
        #print("Respuesta del servidor:", response)
'''

def runAccess(ruta):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Access(commands_pb2.CommandRequest(parameter = ruta))

        if(str.find(response.message, 'Error: ') != -1): 
            return ['', response.message]

        return [response.message, '']
    
def runList(ruta):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.List(commands_pb2.CommandRequest(parameter = ruta))
        return response.message

def runMkdir(ruta):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Mkdir(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runRmdir(ruta):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Rmdir(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runGet(ruta):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Get(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runAdd(ruta):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Add(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runRemove(ruta):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Remove(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    

def runGetData(vector, name):
    name = ''
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = node_pb2_grpc.CommandsWorkStub(channel)


        for partition in vector:
            response = stub.Get(node_pb2.CommandRequestWork(parameter = str.split(partition, ' ')[1]))
            #name = str.split(response.message, '-')[0]
        
            #subprocess.run([
            #    'scp', '-i', 'clave',
            #    'download/',
            #    'datanode@10.0.0.x:/worker/output/' + response.message
            #])

        with open(name, 'wb') as out_file:
            for file_name in sorted(glob.glob('download/*')):
                with open(file_name, 'rb') as in_file:
                    out_file.write(in_file.read())

        return 'Se descargo ' + name


def getCommand(input):

    try:
        auxiliar = str.split(input, ' ')

        if(len(auxiliar) != 2): return 'mala sintax'

        comando = auxiliar[0]
        ruta = auxiliar[1]

        if(comando == 'cd'):
            return runAccess(ruta)
        elif comando == 'ls':
            return runList(ruta)
        elif comando == 'mkdir':
            return runMkdir(ruta)
        elif comando == 'rmdir':
            return runRmdir(ruta)
        elif comando == 'get':
            partitions = str.split(runGet(ruta), '\n')
            file = str.split(ruta, '/')[-1]
            return runGetData(partitions, file)



        elif comando == 'add':
            return runAdd(ruta)
        elif comando == 'rm':
            return runRemove(ruta)
        else:
            return 'comando no conocido'
        
    except Exception as e:
        return 'Error del sistema' + str(e)



#Access, Add, Remove, Get, List, MKdir, Rmdir
if __name__ == '__main__':
    #run()

    loop = True
    ruta = ''

    while(loop):
        
        command = input('Sistema HDFS:/' + ruta + '$ ')

        if command == 'exit':
            break
        
        elif(command[0:2] == 'cd'):
            aux_cd = getCommand(command)
            if(aux_cd == 'Error del sistema'): 
                print(aux_cd)
                continue
            
            if(aux_cd[1] != ''): 
                print(aux_cd[1])
            else:
                ruta = aux_cd[0]

        else:
            print(getCommand(command))




