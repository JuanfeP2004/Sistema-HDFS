import grpc
import commands_pb2
import commands_pb2_grpc
import node_pb2
import node_pb2_grpc
import subprocess
import os
import glob



def runAccess(ruta):
    with grpc.insecure_channel('10.0.0.6:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Access(commands_pb2.CommandRequest(parameter = ruta))

        if(str.find(response.message, 'Error: ') != -1): 
            return ['', response.message]

        return [response.message, '']
    
def runList(ruta):
    with grpc.insecure_channel('10.0.0.6:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.List(commands_pb2.CommandRequest(parameter = ruta))
        return response.message

def runMkdir(ruta):
    with grpc.insecure_channel('10.0.0.6:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Mkdir(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runRmdir(ruta):
    with grpc.insecure_channel('10.0.0.6:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Rmdir(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runGet(ruta):
    with grpc.insecure_channel('10.0.0.6:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Get(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runAdd(ruta):
    with grpc.insecure_channel('10.0.0.6:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Add(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    
def runRemove(ruta):
    with grpc.insecure_channel('10.0.0.6:50051') as channel:
        stub = commands_pb2_grpc.CommandsStub(channel)       
        response = stub.Remove(commands_pb2.CommandRequest(parameter = ruta))
        return response.message
    

def runGetData(partition, location):
    with grpc.insecure_channel(location + ':50051') as channel:
        stub = node_pb2_grpc.CommandsWorkStub(channel)

        response = stub.Get(node_pb2.CommandRequestWork(parameter = partition))
        name = str.split(response.message, '-')[0]
        print(response.message)
        subprocess.run([
            'scp', '-i', 'clave',
            'download/',
            'datanode@' + location + ':/worker/output/' + response.message
        ])

def runAddData(partition, location, file):
    with grpc.insecure_channel(location + ':50051') as channel:
        stub = node_pb2_grpc.CommandsWorkStub(channel)

        subprocess.run([
            'scp', '-i', 'clave',
            'upload/' + file,
            'datanode@' + location + ':/worker/replica/replica_par/'
        ])

        response = stub.Put(node_pb2.CommandRequestWork(parameter = partition + '/' + file))

def runRemoveData(partition, location):
    with grpc.insecure_channel(location + ':50051') as channel:
        stub = node_pb2_grpc.CommandsWorkStub(channel)

        response = stub.Remove(node_pb2.CommandRequestWork(parameter = partition))

def runSendReplica(info, location):
    
    with open('replica', 'w') as file:
        file.write(info)

    subprocess.run([
            'scp', '-i', 'clave',
            'replica',
            'datanode@' + location + ':/worker/replica/'
        ])

    with grpc.insecure_channel(location + ':50051') as channel: #location + '50051'
        stub = node_pb2_grpc.CommandsWorkStub(channel)

        response = stub.ReplicatePut(node_pb2.CommandRequestWork(parameter = ''))

def runRemoveReplica(info, location):
    with open('replica', 'w') as file:
        file.write(info)

    subprocess.run([
            'scp', '-i', 'clave',
            'replica',
            'datanode@' + location + ':/worker/replica/'
        ])

    with grpc.insecure_channel(location + ':50051') as channel: #location + '50051'
        stub = node_pb2_grpc.CommandsWorkStub(channel)

        response = stub.ReplicateRemove(node_pb2.CommandRequestWork(parameter = ''))



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

            get = runGet(ruta)

            if(str.find(get, 'Error:') != -1): return get

            partitions = str.split(get, '\n')

            file = str.split(ruta, '/')[-1]

            for partition in partitions:
                runGetData(str.split(partition, ' ')[1], file) #Cambiar por el servidor
            
            with open(file, 'wb') as out_file:
                for file_name in sorted(glob.glob('download/*')):
                    with open(file_name, 'rb') as in_file:
                        out_file.write(in_file.read())

                out_file.close()

            return 'Se descargo ' + file

        elif comando == 'add':

            file = str.split(ruta, '/')[-1]
            if not os.path.exists('files/' + file): return 'No existe el archivo para subir'

            tamanio = os.path.getsize("files/" + file) / 1000
            bytes = 256000

            get = runAdd(ruta + '?' + tamanio) #Se agrega en el Directorio y se devuelve el archivo
            if(str.find(get, 'Error:') != -1): return get

            info = str.split(get, '\n')
            n = int(info[2])
            id = info[1]

            subprocess.run(['split', '-b', str(bytes), 'files/' + file, file + '_' + id + '-'])
            list = subprocess.run(['ls', 'files/'], capture_output=True, text=True)
            partitions = str.split(list.stdout)

            indexO = list.index(info, 'ORIGINAL')
            indexR = list.index(info, 'REPLICATE')

            replicate_info = ''
            last_host = ''

            #Se agrega los nodos a replicar y se elije el ultimo host del original para enviarlo
            for i in range(n):
                runAddData(info[indexO + i + 1].split(' ')[1], info[indexO + i + 1].split(' ')[0], partitions[i])
                if(i==n): 
                    replicate_info += info[indexR + i + 1]
                    last_host = info[indexO + i + 1].split(' ')[0]
                else: replicate_info += info[indexR + i + 1] + '\n'
            
            #Se le envia la replica a los servidores especificados
            runSendReplica(replicate_info, last_host)

            return 'Se subio el archivo correctamente'
        
        elif comando == 'rm':

            get = runRemove(ruta) #Se borra en el directorio y se devuelve el archivo
            if(str.find(get, 'Error:') != -1): return get

            #Se agrega los nodos a replicar y se elije el ultimo host del original para enviarlo
            for i in range(n):
                runRemoveData(info[indexO + i + 1].split(' ')[1], info[indexO + i + 1].split(' ')[0])
                if(i==n): 
                    replicate_info += info[indexR + i + 1]
                    last_host = info[indexO + i + 1].split(' ')[0]
                else: replicate_info += info[indexR + i + 1] + '\n'
            
            #Se le envia la replica a los servidores especificados
            runRemoveReplica(replicate_info, last_host)

            return 'Se elimino el archivo correctamente'
        
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
