import grpc
import node_pb2
import node_pb2_grpc
import subprocess
import os

def run(node):

    try:

        text = ''

        with grpc.insecure_channel(node + ':50051') as channel:

            stub = node_pb2_grpc.CommandsStub(channel)

            response = stub.GetInfo(node_pb2.CommandRequest(parameter = ''))
            text = response.message
    
        return text
    
    except:
        return 'error'

if __name__ == '__main__':

    process = subprocess.run(['cat', 'hosts.conf'], capture_output=True, text=True)

    nodos = process.stdout.split('\n')
    nodos_totales = ''
    nodos_particiones = ''

    for nodo in nodos:

        particiones = run(nodo)

        if(particiones != 'error'):
            nodos_particiones += nodo + ' ' + particiones + '\n'
            nodos_totales += nodo + '\n'

    with open('nodes', 'w') as file:
        file.write(nodos_totales)

    with open('nodes_par', 'w') as file:
        file.write(nodos_particiones)
