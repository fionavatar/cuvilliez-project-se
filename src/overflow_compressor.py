
"""
We now want to perform compression with overflow areas. 
Indeed, if a single number in the initial array requires a large number of bits k and the other numbers require
 k' bits with k' < k, it is a waste to represent all numbers with k bits. 
 In this case, we can assign a special value to a compressed integer 
 that indicates that the true value is located elsewhere at a certain position in my table, called the overflow area.

For example, if we want to encode the numbers 1, 2, 3, 1024, 4, 5, and 2048. 
We can encode 1, 2, 3, and 4 using 3 bits and the other numbers using 11 bits at the end. 
Since we don't want to lose direct access, we must precalculate the number of integers in the overflow area and then integrate this into our encoding.
 Here, we have 2 integers in the overflow area, which requires 1 bit to be encoded. 
 We will use 1 bit of the encoding to express the fact that we are not directly representing a number but a position in the overflow area. 
 If 1 corresponds to the overflow area, 
 and x-y means that the first bit is x and the others are y, we will represent the sequence of numbers 1, 2, 3, 1024, 4, 5, 2048 
 as 0-1, 0-2, 0-3, 1-0, 0-4, 0-5, 1-1, 1024, 2048
"""

from .outils import *
import math

class OverflowCompressor:
    """Compression avec overflow"""

    def compress(self, data):
        if not data:
            return []
        return overflowCompress(data)

    def decompress(self, compressed):
        return overflowDecompress(compressed)

    def get(self, index, compressed):
        return overflowGet(index, compressed)


def calculerMax(array):
    """
    Calcule :
    - k1 : nombre de bits nécessaires pour représenter le max (overflow area)
    - k2 : nombre de bits nécessaires qui couvre 80% des petites valeurs
           tout en permettant d'encoder la position dans l'overflow
           k2 < 32 ce qui nécessite que toutes les grandes valeurs soient dans l'overflow
    """
    if not array:
        raise ValueError("La liste ne doit pas être vide")

    listeBin = decimalToBinary(array)
    listeTaille = sorted([len(elem) for elem in listeBin])

    k1 = listeTaille[-1]

    # k2 couvre 80% des petites valeurs
    index = math.ceil(len(listeTaille[:-1]) * 0.8) - 1
    k2 = listeTaille[index]

    # Vérifier le nombre d’éléments dans l’overflow
    nbOverflow = sum(1 for elem in listeBin if len(elem) > k2)
    if nbOverflow > 0:
        k_index = math.ceil(math.log2(nbOverflow))
        k2 = max(k2, k_index)  # s'assurer que k2 peut encoder l'indice de l'overflow

    return k1, k2


def overflowCompress(input):
    """
    Compression avec overflow en mots de 32 bits.
    Retourne une liste d'entiers compressés.
    """
    if not input :
        return []
    
    k1, k2 = calculerMax(input)
    if k2 >= 32: #on évite un dépassement et donc une division par zéro
        k2 = 31
    listeBin = decimalToBinary(input)

    strBin = ""
    zoneP = []
    overflowArea = []
    tailleDernier = 32

    for elem in listeBin:

        # Découpage sur 32 bits
        if len(strBin) + k2 + 1 > 32:
            strBin = strBin.ljust(32, '0')
            zoneP.append(strBin)
            strBin = ""

        # si overflow on marque avec un flag '1' et sa position dans la partie overflow area
        if len(elem) > k2:
            overflowArea.append(padding(elem, k1))
            ind = bin(len(overflowArea) - 1)[2:].zfill(k2)
            strBin += '1' + ind
        else:
            strBin += '0' + padding(elem, k2)

    if strBin:
        tailleDernier = len(strBin)
        strBin = strBin.ljust(32, '0')
        zoneP.append(strBin)

    # On code les overflow dans leurs propres blocs de 32 bits
    OFBin = ""
    for e in overflowArea:
        if len(OFBin) + k1 > 32:
            OFBin = OFBin.ljust(32, '0')
            zoneP.append(OFBin)
            OFBin = ""
        OFBin += e
    #Dernier mot 
    if len(OFBin)>0:

        OFBin = OFBin.ljust(32, '0')
        zoneP.append(OFBin)

    return [k1, k2, len(overflowArea), tailleDernier] + binaryToDecimal(zoneP)

    
def decoupe(s, k):
    """
    Découpe une chaîne binaire s en blocs de taille k en partant de la gauche.
    Le dernier bloc (à droite) peut être plus court dans ce cas il s'agit seulement du padding.
    """
    blocs = []
    while s:
        blocs.append( s[:k])  # prend k bits à droite
        s = s[k:]
    return blocs


def nbBloccsOverflow(k1, nbOF):
    """
    Calcule le nombre exact de blocs de 32 bits nécessaires pour stocker nbOF entiers
    de k1 bits chacun, sans crossing et avec padding à la fin de chaque bloc.
    """
    bits_used = 0
    blocs = 1 if nbOF > 0 else 0
    for _ in range(nbOF):
        if bits_used + k1 > 32:
            blocs += 1
            bits_used = 0
        bits_used += k1
    return blocs


def overflowDecompress(output):
    """
    Décompresse un tableau compressé avec overflowCompress().
    """
    if not output :
        return []
    
    k1, k2, nbOF, tailleDernier = output[0], output[1], output[2], output[3]
    compList = output[4:]
    compList = [bin(x)[2:].zfill(32) for x in compList]
    nbTabOF = nbBloccsOverflow(k1, nbOF)

    if nbTabOF > 0:
        zoneP = compList[:-nbTabOF]
        tail = compList[-nbTabOF:]
    else:
        zoneP = compList[:]
        tail = []

    overflowArea = []

    for i in range(nbOF) :
        if len(tail[0]) < k1 :
            del(tail[0])
        overflowArea.append((tail[0])[:k1])
        tail[0] = (tail[0])[k1:]

    # découper le dernier mot selon la taille du dernier bloc
    if zoneP:  # vérifier qu'il y a des mots
        zoneP[-1] = zoneP[-1][:tailleDernier]
     # Convertir chaque mot en binaire 32 bits avec padding à gauche
    finalList = []
    # Lecture de la zone principale
    for elem in zoneP :
   
        elemList = []
        for j in range(0,len(elem),(k2+1)) :
            block = elem[j : j + (k2+1)]
            if(len(block) == (k2+1)) :
                flag = block[0]
                bits = block[1:]

                if flag == '0':
                    elemList += [bits] 
                else:
                    index = int(bits, 2)
                    if index < len(overflowArea):
                        elemList += [overflowArea[index]] 

        finalList.extend(elemList)
       
    # Conversion finale
    finalList = [int(b, 2) for b in finalList]
    return finalList



def overflowGet( i, array ) :
    """
    permet l’accès direct à l’élément i sans décompression complète

    Entrée :
    i un entier

    Sortie :
    l'élément à l'indice i
    """
    k1, k2, nbOF, tailleDernier = array[0], array[1], array[2], array[3]
    compList = array[4:]

    indiceBloc = i // (32 // (k2 + 1))
    nbBlocsParMot = 32 // (k2 + 1)
    indiceMot = i % nbBlocsParMot   
   
    # Convertir elem en binaire 
    elem = bin(compList[indiceBloc])[2:].zfill(32)
    mots = decoupe(elem,(k2+1))

    mot = mots[indiceMot]
    flag = mot[0]
    bits = mot[1:]
   
    if flag == '0':
        return int(bits, 2)
    else:
        nbTabOF = nbBloccsOverflow(k1, nbOF)
        tail = compList[-nbTabOF:]
        tail = [bin(x)[2:].zfill(32) for x in tail]
        overflowArea = []
       
        for i in range(nbOF) :
            if len(tail[0]) < k1 :
                del(tail[0])
            overflowArea.append((tail[0])[:k1])
            tail[0] = (tail[0])[k1:]


        index = int(bits, 2)
        if index < len(overflowArea):
            return int(overflowArea[index],2)

