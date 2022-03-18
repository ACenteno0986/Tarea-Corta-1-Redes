import os
import zipfile

def comprimirArchivo():
    file_zip = zipfile.ZipFile('test/archive.atm', 'w')
    
    for folder, subfolders, files in os.walk('test'):
        for file in files:
            file_zip.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder,file), 'test'), compress_type = zipfile.ZIP_DEFLATED)
 
    file_zip.close()


def descomprimirArchivo():
    fantasy_zip = zipfile.ZipFile('test/archive.atm')
    fantasy_zip.extractall('test/files')
    fantasy_zip.close()
comprimirArchivo()

descomprimirArchivo()