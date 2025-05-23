import os


def haccess(ruta):
    if str.find(ruta, '..') != -1:
        return 'Error: .. no esta soportado'
    else:
    
        if os.path.exists('../carpeta/' + ruta) and os.path.isdir('../carpeta/' + ruta):

            if(ruta[len(ruta)-1] == '/'): return ruta
            return ruta + '/'
        else:
            return "Error: La ruta no existe"