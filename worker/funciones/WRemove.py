import os
import subprocess

def Remove(partition):

    if not os.path.exists('../node/' + partition):
        return 'no se encontro la particion'
    
    archivos = [f for f in os.listdir('../node/' + partition) if os.path.isfile(os.path.join('../node/' + partition, f))]
    
    if not archivos:
        return 'No hay un archivo en la particion'


    for archivo in os.listdir('../node/' + partition):
        os.remove(os.path.join('../node/' + partition, archivo))
    
    return 'OK'

#split -b 256000 auth_image.jpg auth_image_2f456q-