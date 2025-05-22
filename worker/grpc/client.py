import grpc
import node_pb2
import node_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = node_pb2_grpc.CommandsWorkStub(channel)
        #response = stub.GetInfo(node_pb2.CommandRequestWork(parameter = ''))
        #response = stub.Remove(node_pb2.CommandRequestWork(parameter = 'p00'))
        #response = stub.Put(node_pb2.CommandRequestWork(parameter = 'p01/auth_image_2f456q-ab'))
        response = stub.Get(node_pb2.CommandRequestWork(parameter = 'p00'))
        print("Respuesta del servidor:", response.message)

#Access, Add, Remove, Get, List, MKdir, Rmdir
if __name__ == '__main__':
    run()