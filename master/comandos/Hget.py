import io
import subprocess


def hget(ruta):

    if str.find(ruta, '..') != -1:
        return 'Error: .. no esta soportado'
    else:
        process_oj = subprocess.run(['cat', '../carpeta/' + ruta + '.info'], capture_output=True, text=True)
        ###
        process_ht = subprocess.run(['cat', '../nodos/nodes'], capture_output=True, text=True)

        if(process_oj.stdout == 'None' or process_ht.stdout == 'None'):
            return 'Error: Ocurrio un error'
        else:

            object_vector = process_oj.stdout.split('\n')
            active_nodes = process_ht.stdout.split('\n')

            n = int(object_vector[2])
            indexO = list.index(object_vector, 'ORIGINAL')
            indexR = list.index(object_vector, 'REPLICATE')
            info = ''

            for i in range(n):
                if(object_vector[indexO + i + 1].split(' ')[0] not in active_nodes):
                    break
                
                if(i == n-1):
                    info += object_vector[indexO + i + 1]
                    return info
                else:
                    info += object_vector[indexO + i + 1] + '\n'

            info = '' 
            for i in range(n):
                if(object_vector[indexR + i + 1].split(' ')[0] not in active_nodes):
                    break

                if(i == n-1):
                    info += object_vector[indexR + i + 1]
                    return info
                else:
                    info += object_vector[indexR + i + 1] + '\n'

            return 'Error: No se puede acceder al archivo =('