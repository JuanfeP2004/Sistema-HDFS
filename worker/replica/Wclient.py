import grpc
import node_pb2
import node_pb2_grpc
import os
import subprocess

def ReplicatePut(nodo):

    process = subprocess.run(['ls', 'replica/replica_par/'], capture_output=True, text=True).stdout
    partitions = str.split(process, ' ')

    with open('../replica/replica', 'r') as file:

        for partition in range(len(partitions)):
                
            #subprocess.run([
                #    'scp', '-i', 'clave',
                #    '../replica/replica_par/' + partitions[partition],
                #    'datanode@' + text[0] + ':/worker/archivos/'
                #])

            text = file.readline().strip().split(' ')
            route = text[1] + '/' + partitions[partition]

            with grpc.insecure_channel('localhost:50061') as channel: #text[0] + ':50051'
                stub = node_pb2_grpc.CommandsWorkStub(channel)
                response = stub.Put(node_pb2.CommandRequestWork(parameter = route))

    return 'OK'

def ReplicateRemove(nodo):

    with open('../replica/replica', 'r') as file:

        linea = file.readline()

        while linea:
            text = linea.strip().split(' ')

            with grpc.insecure_channel('localhost:50061') as channel: #text[0] + ':50051'
                stub = node_pb2_grpc.CommandsWorkStub(channel)
                response = stub.Remove(node_pb2.CommandRequestWork(parameter = text[1]))
    
    return 'OK'

