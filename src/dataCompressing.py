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
    return binList

def binaryToDecimal (listeB ) :
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

def compress( input ) :
    """
    compresse int[] input

    entree : input un tableau d'entiers décimaux
    sortie : un tableau d'entiers décimaux (compressé)
    """
    listeBin = decimalToBinary(input)
    k = calculerK(input)
    nb = math.floor(32/k)

    compressedList = []
    strBin = ""
    i = 0
    for elem in listeBin :
        if i == k :
            compressedList.append(strBin)
            strBin = ""
            i = 0
        else :
            strBin = strBin + elem
            i+=1
    compressedList.append(strBin)
    print(compressedList)



def decompress( output ) :
    """
    decompresse int[] output
    """

#2ème mode de compression   
"""
no crossing — chaque entier compressé doit être entièrement contenu 
dans un mot de sortie (donc on peut gaspiller bits et aligner).
"""

def get( i ) :
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
    print(nombreBits([1, 2, 3, 4, 5]))  # ➜ 3
    print(nombreBits([12, 25, 31]))     # ➜ 5
    print(nombreBits([0, 0, 0]))        # ➜ 1

    print(calculerK([1, 2, 3, 4, 5]))  # ➜ 3
    print(calculerK([12, 25, 31]))     # ➜ 5
    print(calculerK([0, 0, 0]))        # ➜ 1
    print(calculerK([ 15, 3, 4, 23, 28, 1, 17, 18]))        # ➜ 7

    print(decimalToBinary ( values ))
    print(decimalToBinary ( data ))
    #print(decimalToBinary ( [ 1, 14, 67, 35, 89] ))

    print("il faut :")
    print(math.floor(32/calculerK([ 15, 3, 4, 23, 28, 1, 17, 18])), "entiers")
    compress(data)
    print(binaryToDecimal(['1111111001011111100', '1000110010']))