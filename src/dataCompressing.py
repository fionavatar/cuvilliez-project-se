"""
Data compressing for speed up transmission
 
The transmission of integer arrays is one of the central problems of the internet.
In this project, you are asked to study different transmission modes based on integer compression.
The idea is to compress an integer array in order to have fewer integers to transmit, then decompress the integers after transmission.

Normally each integer take 32 bits but if the value is not superior at 100
(7 bits are enough) you can divide by at least 4 the total size  with compressinf

cas limite nb = O maxValue = 0 donc k = 1
nb negatif attention
valeur très grande à isoler -> overflow
"""
#1 Determine the size of each element. Understand how many bits each piece of information requires
#2 Allocate a Buffer Create in wich you will store you packed data
#3 Pack the bits Use bitwise operations to combine the data into the buffer
#4 unpack the bits Reverse the process when you need to access the stored data

import math

def decimalToBinary ( liste ) :
    """
    Convertit les nombres d'une liste de décimal en binairre

    entrée : une liste d'entiers décimaux
    sortie : une liste d'entiers binaires
    """
    binList = []
    for elem in liste :
        nb = elem
        binNb = ""
        while nb > 0 :
            binNb = str(nb%2) + binNb
            nb = nb // 2
        
        binList.append(binNb)
    print(binList)
    return binList

def binaryToDecimal (listeB) :
    """
    Convertit les nombres d'une liste de binaire en décimal

    entrée : une liste d'entiers binaires
    sortie : une liste d'entiers décimaux
    """
    decList = []
    for elem in listeB :
        decNb = 0
        for i in range(len(elem)) :
            decNb = decNb + int(elem[i])*(2**(len(elem)-1-i))
        decList.append(decNb)
    return decList

def padding(nb, k) :
    binNb = nb
    if len(binNb) < k :
            binNb = (k-len(binNb))*'0' +binNb
    return binNb
    
# trop lent ?
def nombreBits ( liste ) :
    """
    Calcule le nombre de bits nécessaire à la conpression. 
    Astuce on a uniquement besoin de calculer pour l'entier max.
    Pour les entiers positifs uniquement.

    En entrée :
    l : array d'entiers

    En sortie :
    k : un entier
    """
    maxValue = max(liste)
    if maxValue == 0 :
        k = 1
    else :
        bin = ""
        while maxValue > 0 :
            bin = bin + str(maxValue%2)
            maxValue = maxValue // 2
            k = len(bin)
    return k
    
    

# plus rapide
def calculerK(array):
    maxValue = max(array)
    if maxValue == 0 :
        k = 1
    else :
        k = math.floor(math.log2(maxValue)) + 1
    return k


# 1er mode de compression
"""
crossing allowed — les entiers compressés peuvent s’étendre sur deux mots de sortie 
(ex : un entier commence dans la fin d’un mot de 32 bits et continue dans le mot suivant).
"""

def crossingCompress ( input ) :
    """
    compresse int[] input

    entree : input un tableau d'entiers décimaux
    sortie : un tableau d'entiers décimaux (compressé)
    """
    k = calculerK(input)
    listeBin = decimalToBinary(input)
   
    compressedList = []
    strBin = ""
    i = 0
    for elem in listeBin :
        elemP = padding(elem, k)
        for c in elemP :
            if i == 32 :
                compressedList.append(strBin)
                i = 1
                strBin = c

            else :
                strBin = strBin + c
                i += 1
    
    compressedList.append(strBin)  
    print(compressedList)
    return ([k]+binaryToDecimal(compressedList))
     
 

def crossingDecompress( output ) :
    """
    decompresse int[] output
    """

    k, compList = output[0], output[1:]
    compList = decimalToBinary(compList)

    if len(compList) > 1:
        head = compList[:(-1)]
        tail = compList[-1]
        
    else :
        head = compList
        tail = ""

    binNb = ""

    for elem in head :
        elem = padding(elem, 32)
        print(elem)
        elemList = []
        binNn = ""
        for i in range(32) : 
            if len(binNb) == k :
                elemList.append(binNb)
                binNb = elem[i]
            else : 
                binNb += elem[i]

    if len(binNb) == k :
        elemList.append(binNb)
        binNb=""
    print(elemList)
    
    tailList = []
    binNbTail = ""
    
    for j in range(len(tail)-1, -1, -k):
        print(j)
        if (j-k+1) < 0 :
            binNbTail = tail[0 : j+1]
            binNb = binNb + padding(binNbTail,(k-len(binNb)))
            tailList.append(binNb)
        elif j == 0 :
            binNbTail = tail[0]
            binNb = binNb + padding(binNbTail,(k-len(binNb)))
            tailList.append(binNb)
        else :
            tailList.append(tail[j-k+1 : j+1])
    tailList.reverse()
    elemList = elemList + tailList

    return binaryToDecimal(elemList) 
    




#2ème mode de compression   
"""
no crossing — chaque entier compressé doit être entièrement contenu 
dans un mot de sortie (donc on peut gaspiller bits et aligner).
"""

def noCrossingCompress( input ) :
    """
    compresse int[] input

    entree : input un tableau d'entiers décimaux
    sortie : un tableau d'entiers décimaux (compressé)
    """
    k = calculerK(input)
    nb = math.floor(32/k)
    listeBin = decimalToBinary(input)

    compressedList = []
    strBin = ""
    i = 0
    for elem in listeBin :
        if i == k :
            compressedList.append(strBin)
            strBin = padding(elem, k)
            i = 1
        else :
            strBin = strBin + padding(elem, k)
            i+=1
    compressedList.append(strBin)
    return ([k]+binaryToDecimal(compressedList))


def noCrossingDecompress( output ) :
    """
    decompresse int[] output
    """
    k, compList = output[0], output[1:]
    compList = decimalToBinary(compList)
    finalList = []
    for elem in compList :
        elemList = []
        for i in range(len(elem)-1, -1, -k ):
            if (i-k+1) < 0 :
                elemList.append(elem[0 : i+1])
            elif i == 0 :
                elemList.append(elem[0])
            else :
                elemList.append(elem[i-k+1 : i+1])
        elemList.reverse()
        finalList = finalList + elemList
    return binaryToDecimal(finalList)       

def get( i, k, array ) :
    """
    permet l’accès direct à l’élément i sans décompression complète

    Entrée :
    i un entier

    Sortie :
    l'élément à l'indice i
    """



if __name__ == "__main__":
    values = [5, 3, 7, 1, 2, 6] # Example values (6 values, each 3 bits)
    data = [ 15, 3, 4, 23, 28, 1, 17, 18]
    #print(nombreBits([1, 2, 3, 4, 5]))  # ➜ 3
    #print(nombreBits([12, 25, 31]))     # ➜ 5
    #print(nombreBits([0, 0, 0]))        # ➜ 1

    #print(calculerK([1, 2, 3, 4, 5]))  # ➜ 3
    #print(calculerK([12, 25, 31]))     # ➜ 5
    #print(calculerK([0, 0, 0]))        # ➜ 1
    #print(calculerK([ 15, 3, 4, 23, 28, 1, 17, 18]))        # ➜ 7


    #print(decimalToBinary ( [ 1, 14, 67, 35, 89] ))

    print("il faut :")
    print((32//calculerK([ 15, 3, 4, 23, 28, 1, 17, 18])), "entiers")
    print("Méthode no crossing allowed")
    comp = noCrossingCompress(data)
    print(comp)
    print(noCrossingDecompress(comp))
    print("Méthode  crossing allowed")
    compC = crossingCompress ( data )
    print(compC)
    print(crossingDecompress(compC))