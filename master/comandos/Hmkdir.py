import subprocess


def hmkdir(ruta):

    if str.find(ruta, '..') != -1:
        return '.. no esta soportado'
    else:
        process = subprocess.run(['mkdir', '../carpeta/' + ruta])
        if(process.stderr == 'None'):
            return process.stderr
        else:
            return 'Se creo la carpeta correctamente'