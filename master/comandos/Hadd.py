import os
import subprocess
import math
import random
import string

partition = 256

#ruta/archivo?tamanio
def hadd(ruta):

    if str.find(ruta, '..') != -1:
        return 'Error: .. no esta soportado'

    auxiliar = str.split(ruta, '?')
    tamanio = int(auxiliar[1])
    ubicacion = auxiliar[0]

    auxiliar_file = str.split(ubicacion, '/')
    archivo = auxiliar_file[len(auxiliar_file)-1]

    nombre = str.split(archivo, '.')[0]

    if not os.path.exists('../carpeta/' + str.split(ubicacion, archivo)[0] + "/"):
        return 'Error: la ruta no existe'
    
    if os.path.exists('../carpeta/' + ubicacion + '.info'): ####
        return 'Error: el archivo ya existe'

    process_ht = subprocess.run(['cat', '../nodos/nodes'], capture_output=True, text=True)
    process_par = subprocess.run(['cat', '../nodos/nodes_par'], capture_output=True, text=True)

    if(process_ht.stdout == 'None' or process_par.stdout == 'None'):
        return 'Error: Ocurrio un error'

    hosts = str.split(process_par.stdout, '\n')
    number_p = math.ceil(tamanio / partition)

    restant_par = number_p
    info = ''
    updated_host = ''

    info += archivo + '\n' + generar_id(12) + '\n' + str(number_p) + '\n'

    used_host = []

    info += 'ORIGINAL\n'

    #Guardar el original
    while(restant_par > 0):

        host = findLessBusy(hosts)

        if (len(host) == 0):
            return 'Error: El archivo es muy grande para guardarlo'
        
        used_host.append(host[0])
        new_host = host.copy()

        for i in range(len(host)-1):

            info += host[0] + ' ' + host[i+1] + '\n'
            updated_host += host[0] + ' ' + host[i+1] + '\n'
            restant_par -= 1
            new_host.remove(host[i+1])

            #Si termina en una maquina
            if(restant_par == 0):               
                hosts[hosts.index(' '.join(host))] = ' '.join(new_host)
                #host = new_host
                break
        
        if(restant_par == 0): break
        #Si requiere de otra maquina, se vacia la antigua
        hosts[hosts.index(' '.join(host))] = ' '.join(new_host)


    #Guardar la copia
    remaining_hosts = hosts.copy()
    restant_par = number_p

    #Se eliminan los host que ya se usaron para la replica
    for used in used_host:
        for host in hosts:
            if(str.split(host, ' ')[0] == used):
                remaining_hosts.remove(host)
    

    info += 'REPLICATE\n'

    #La replicacion
    while(restant_par > 0):

        host = findLessBusy(remaining_hosts)

        if (len(host) == 0):
            return 'Error: No hay espacio para replicar el archivo'
        
        #used_host.append(host[0])
        new_host = host.copy()

        for i in range(len(host)-1):

            info += host[0] + ' ' + host[i+1] + '\n'
            updated_host += host[0] + ' ' + host[i+1] + '\n'
            restant_par -= 1
            new_host.remove(host[i+1])


            #Si termina en una maquina
            if(restant_par == 0):               
                hosts[hosts.index(' '.join(host))] = ' '.join(new_host)
                remaining_hosts[remaining_hosts.index(' '.join(host))] = ' '.join(new_host)
                break
        
        if(restant_par == 0): break
        #Si requiere de otra maquina, se vacia la antigua
        hosts[hosts.index(' '.join(host))] = ' '.join(new_host)
        remaining_hosts[remaining_hosts.index(' '.join(host))] = ' '.join(new_host)

    #print(hosts)

    with open('../carpeta/' + ubicacion + '.info', 'w', encoding='utf-8') as file: ####
        file.write(info[0:-1])

    updateHosts(updated_host[0:-1])

    return info #ACTUALIZAR EL ARCHIVOS DE LAS PARTICIONES

def findLessBusy(partitions):

    less = ''
    less_number = 0

    for host in partitions:
        new_host = str.split(host, ' ')
        if len(new_host)-1 > less_number:
            less = new_host
            less_number = len(new_host)-1
    return less

def generar_id(length=12):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=length))

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
                if(block in actual_partition):
                    actual_partition.remove(block)
        
        update += ' '.join(actual_partition) + '\n'

    if(len(update) != 0): update = update[0:-1]

    with open('../nodos/nodes_par', 'w') as nodes:
        nodes.write(update)

    nodes.close() 


#10.0.0.2 p08 p09
#10.0.0.4
#10.0.0.6 p01 p02 p03 p04 p05 p06 p07 p10 

#print(hadd('volumen/imagen666.jpg?500'))
#print(updateHosts('10.0.0.2 p08\n10.0.0.2 p09\n10.0.0.4 p04\n10.0.0.6 p01\n10.0.0.6 p02'))
