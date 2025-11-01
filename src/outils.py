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

import math

def decimalToBinary ( liste ) : #mieux d'utiliser bin(x)[2:]
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
        if binNb == "":
            binNb = '0'
        binList.append(binNb)

    return binList

def binaryToDecimal (listeB) : #mieux d'utiliser int(str,2)
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

def padding(nb, k) : #sinon nb.zfill(k)
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
    if maxValue == 0:
        return 1
    bin_str = ""
    while maxValue > 0:
        bin_str = str(maxValue % 2) + bin_str
        maxValue = maxValue // 2
    return len(bin_str)
    
    

# plus rapide
def calculerK(array):
    if not array:
        raise ValueError("La liste ne doit pas être vide")
    
    maxValue = max(array)
    if maxValue == 0 :
        k = 1
    else :
        k = math.floor(math.log2(maxValue)) + 1
    return k