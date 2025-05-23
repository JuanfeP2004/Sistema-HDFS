import subprocess


def hrmdir(ruta):
    if str.find(ruta, '..') != -1:
        return '.. no esta soportado'
    elif ruta == '' or str.find(ruta, '.') != -1:
        return 'no se puede borrar la misma carpeta'
    else:
        process = subprocess.run(['rmdir', '../carpeta/' + ruta])
        if(process.stdout == 'None'):
            return process.stderr
        else:
            return 'Se elimino la carpeta correctamente'