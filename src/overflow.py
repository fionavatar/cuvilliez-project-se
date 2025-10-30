from outils import *
import math


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

def calculerMax(array):
    """
    Calcule :
    - k1 : nombre de bits nécessaires pour représenter le max (overflow area)
    - k2 : nombre de bits nécessaires qui couvre 80% des petites valeurs(zone principale)
    """
    if not array:
        raise ValueError("La liste ne doit pas être vide")

    # Conversion en binaire et calcul des longueurs
    listeBin = decimalToBinary(array)
    listeTaille = sorted([len(elem) for elem in listeBin])

    # k1 = max bits
    k1 = listeTaille[-1]
    #print(listeTaille[:-1])
    #on cherche la valeur qui couvre 80% des valeurs tout en faisant attention à l'overflow
    index = math.ceil(len(listeTaille[:-1])*0.8) - 1
    k2 = listeTaille[index]  

    return k1,k2

def overflowCompress(input):
    """
    Compression avec overflow en mots de 32 bits.
    Retourne une liste d'entiers compressés.
    """
    k1, k2 = calculerMax(input)
    listeBin = decimalToBinary(input)

    strBin = ""
    zoneP = []
    overflowArea = []

    for elem in listeBin:

        # Découpage sur 32 bits
        if len(strBin) + k2 + 1 > 32:
            zoneP.append(strBin)
            strBin = ""

        # si overflow on marque avec un flag '1' et sa position dans la partie overflow area
        if len(elem) > k2:
            overflowArea.append(padding(elem, k1))
            ind = bin(len(overflowArea) - 1)[2:].zfill(k2)
            strBin += '1' + ind
        else:
            strBin += '0' + padding(elem, k2)

    # Écriture de la zone d’overflow
    for e in overflowArea:
        if len(strBin) + k1 > 32:
            zoneP.append(strBin)

            strBin = ""
        strBin += e

    # Dernier mot (si incomplet)
    if strBin:
        zoneP.append(strBin)
    return [k1, k2, len(overflowArea)] + binaryToDecimal(zoneP)

    


def overflowDecompress(output):
    """
    Décompresse un tableau compressé avec overflowCompress().
    """
    k1, k2, nbOF = output[0], output[1], output[2]
    compList = output[3:]

    # Convertir chaque mot en binaire (32 bits)
    zoneP = [bin(x)[2:] for x in compList] 

    overflowArea = []

    for i in range(nbOF) :
        overflowArea = [(zoneP[-1])[-k1:]] + overflowArea
        zoneP[-1] = zoneP[-1][:-k1]

        if len(zoneP[-1]) == 0 :
            del(zoneP[-1])

    finalList = []
    
    # Lecture de la zone principale
    for elem in zoneP :
        elemList = []
        for j in range(len(elem),0,-(k2+1)) :
            start = max(0,j - (k2+1))
            block = padding(elem[start : j],(k2+1))
            flag = block[0]
            bits = block[1:]

            if flag == '0':
                elemList = [bits] + elemList
            else:
                index = int(bits, 2)
                if index < len(overflowArea):
                    elemList = [overflowArea[index]] + elemList

        finalList.extend(elemList)
       
    # Conversion finale
    finalList = [int(b, 2) for b in finalList]
    return finalList



def decoupe(s, k):
    """
    Découpe une chaîne binaire s en blocs de taille k en partant de la droite.
    Le premier bloc (à gauche) peut être plus court.
    """
    blocs = []
    while s:
        blocs.insert(0, s[-k:])  # prend k bits à droite
        s = s[:-k]
    return blocs



def overflowGet( i, array ) :
    """
    permet l’accès direct à l’élément i sans décompression complète

    Entrée :
    i un entier

    Sortie :
    l'élément à l'indice i
    """
    k1, k2, nbOF = array[0], array[1], array[2]
    compList = array[3:]

    indiceBloc = i // (32 // (k2 + 1))
    nbBlocsParMot = 32 // (k2 + 1)
    indiceMot = i % nbBlocsParMot   
   
    # Convertir elem en binaire 
    elem = bin(compList[indiceBloc])[2:] 
    mots = decoupe(elem,(k2+1))
    mot = padding(mots[indiceMot],(k2+1))
    flag = mot[0]
    bits = mot[1:]

    if flag == '0':
        return int(bits, 2)
    else:
        zoneP = [bin(x)[2:] for x in compList] 
        overflowArea = []
        #On isole la zone overflow
        for i in range(nbOF) :
            overflowArea = [(zoneP[-1])[-k1:]] + overflowArea
            zoneP[-1] = zoneP[-1][:-k1]
        if len(zoneP[-1]) == 0 :
            del(zoneP[-1])

        index = int(bits, 2)
        if index < len(overflowArea):
            return int(overflowArea[index],2)

    




if __name__ == "__main__":
    values = [5, 3, 7, 1, 2, 6] # Example values (6 values, each 3 bits)
    #data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 50, 75, 100, 0]
    #data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #data = [15, 3, 4, 23, 28, 1, 17, 18]
    #data = [75, 95, 95, 22, 40, 77, 67, 97, 17, 9, 91, 60, 24, 69, 96, 62, 7, 11, 65, 60, 24, 90, 44, 15, 52, 14, 7, 94, 50, 8, 48, 32, 0, 42, 37, 73, 98, 42, 10, 84, 19, 52, 76, 72, 56, 3, 92, 4, 37, 62]
    #data = [21, 11, 32, 39, 45, 80, 63, 3, 72, 2, 50, 27, 45, 12, 69, 43, 76, 70, 89, 51, 20, 55, 28, 72, 31, 73, 90, 20, 62, 67, 56, 65, 63, 75, 69, 71, 10, 69, 2, 97, 91, 29, 17, 57, 93, 74, 33, 46, 56, 67]
    #data = [1, 2, 3, 4, 6, 8, 9, 1024, 4, 5, 2048]
    data = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000]
    compressed = overflowCompress(data)
    print("Compressé :", compressed)

    decompressed = overflowDecompress(compressed)
    print("Décompressé :", decompressed)
    assert decompressed == data

    #print("get i = 0 -> 1 : ", overflowGet(0,compressed))
    #print("get i = 1 -> 2 : ", overflowGet(1,compressed))
    #print("get i = 2 -> 3 : ", overflowGet(2,compressed))
    #print("get i = 3 -> 4 : ", overflowGet(3,compressed))
    #print("get i = 4 -> 6 : ", overflowGet(4,compressed))
    #print("get i = 5 -> 8 : ", overflowGet(5,compressed))
    #print("get i = 6 -> 9 : ", overflowGet(6,compressed))
    #print("get i = 7 -> 1024 : ", overflowGet(7,compressed))
    #print("get i = 8 -> 4 : ", overflowGet(8,compressed))
    #print("get i = 9 -> 5 : ", overflowGet(9,compressed))
    #print("get i = 10 -> 2048 : ", overflowGet(10,compressed))
    
  
   
