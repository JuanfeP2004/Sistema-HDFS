import os
import subprocess

def hrem (ruta):
    if str.find(ruta, '..') != -1:
        return 'Error: .. no esta soportado'
    else:

        if os.path.exists('../carpeta/' + ruta + '.info'):

            process_oj = subprocess.run(['cat', '../carpeta/' + ruta + '.info'], capture_output=True, text=True)
            ####
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

                info += 'ORIGINAL\n'
                for i in range(n):
                    if(object_vector[indexO + i + 1].split(' ')[0] not in active_nodes):
                        return 'Error: No se puede borrar el archivo'
                
                    info += object_vector[indexO + i + 1] + '\n'

                info += 'REPLICATE\n'
                for i in range(n):
                    if(object_vector[indexR + i + 1].split(' ')[0] not in active_nodes):
                        return 'Error: No se puede borrar el archivo'

                    if(i == n-1):
                        info += object_vector[indexR + i + 1]
                    else:
                        info += object_vector[indexR + i + 1] + '\n'

                subprocess.run(['rm', '../carpeta/' + ruta + '.info']) ####

                updateHosts(info=info)

                return info #YA

        else:
            return "Error: La ruta no existe"
        
def updateHosts(info):
    process_par = subprocess.run(['cat', '../nodos/nodes_par'], capture_output=True, text=True)
    partitions = str.split(process_par.stdout, '\n')
    modifications = str.split(info, '\n')

    update = ''

    for partition in partitions:
        actual_partition = str.split(partition, ' ')
        host = actual_partition[0]

        for mod in modifications:
            actual_host = str.split(mod, ' ')[0]
            block = str.split(mod, ' ')[1]

            if(host == actual_host):
                if(block not in actual_partition):
                    actual_partition.append(block)
        
        update += ' '.join(actual_partition) + '\n'

    if(len(update) != 0): update = update[0:-1]

    with open('../nodos/nodes_par', 'w') as nodes:
        nodes.write(update)

    nodes.close() 


#10.0.0.2 p08 p09
#10.0.0.4
#10.0.0.6 p01 p02 p03 p04 p05 p06 p07 p10
    
#print(updateHosts('10.0.0.2 p08\n10.0.0.4 p01\n10.0.0.6 p08\n10.0.0.4 p02\n10.0.0.4 p03'))