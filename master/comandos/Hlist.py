import subprocess
import io
import os


def hlist(ruta):
    if str.find(ruta, '..') != -1:
        return '.. no esta soportado'
    else:
        process = subprocess.run(['ls', '../carpeta/' + ruta], capture_output=True, text=True)
    
        if(process.stdout == 'None'):
            return 'Ocurrio un error'
        else:
            vector = str.split(process.stdout)
            list = ''

            for object in vector:
                if os.path.isdir('../carpeta/' + ruta + '/' + object):
                    list += object.split('.info')[0] + '/\n' ###
                else:    
                    with io.open('../carpeta/' + ruta + '/' + object, 'rb') as file:
                        list += file.readline().decode('utf-8').strip() + '\n'
                    file.close()
            
            return list[0:-1]          