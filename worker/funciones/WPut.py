import os
import subprocess

partition = 256

def Put(ruta):

    auxiliar = str.split(ruta, '/')
    partition = auxiliar[0]
    archivo = auxiliar[1]

    if not os.path.exists('../archivos/' + archivo):
        return 'no se encontro el archivo'
    if not os.path.exists('../node/' + partition):
        return 'no se encontro la particion'
    
    archivos = [f for f in os.listdir('../node/' + partition) if os.path.isfile(os.path.join('../node/' + partition, f))]
    
    if archivos:
        return 'Ya hay un archivo en la particion'

    if (os.path.getsize('../archivos/' + archivo) / 1000 > 256):
        return 'El archivo es mayor a 256KB'

    subprocess.run([
        'cp', 
        '../archivos/' + archivo, 
        '../node/' + partition + '/'], 
        capture_output=True, text=True)
    
    return 'OK'


#split -b 256000 auth_image.jpg auth_image_2f456q-