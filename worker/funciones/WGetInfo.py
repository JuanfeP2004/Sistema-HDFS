import os
import subprocess

def GetInfo():

    texto = '' #Falta la IP 10.0.0.5 10.0.0.7 10.0.0.9
    particiones = subprocess.run(['ls', '../node/'], capture_output=True, text=True).stdout

    for particion in str.split(particiones):

        archivos = [f for f in os.listdir('../node/' + particion + '/') 
                    if os.path.isfile(os.path.join('../node/' + particion + '/', f))]
    
        if not archivos:
            texto += particion + ' '

    return texto[0:-1]
