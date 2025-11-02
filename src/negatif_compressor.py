from .outils import *
import math

class NegatifCompressor:
    """Compression des entiers négatifs ou/et positifs avec overflow"""

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
    """
    if not array:
        raise ValueError("La liste ne doit pas être vide")

    array = ([abs(elem) for elem in array])
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
        k2 = min(k2, 31)  # k2+1 ≤ 32

    return k1, (k2 +1) 


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
    

    strBin = ""
    zoneP = []
    overflowArea = []

    tailleDernier = 32

    for elem in input:
        if elem < 0 :
            signe = '1'
        else :
            signe = '0' 
        binElem = bin(abs(elem))[2:]
        # Découpage sur 32 bits
        if len(strBin) + k2 + 1 > 32:
            strBin = strBin.ljust(32, '0')
            zoneP.append(strBin)
            strBin = ""

        # si overflow on marque avec un flag '1' et sa position dans la partie overflow area
        if len(binElem) > (k2 - 1):
            overflowArea.append(padding(binElem, k1))
            ind = bin(len(overflowArea) - 1)[2:].zfill(k2-1)
            strBin += '1' + signe + ind
        else:
            strBin += '0' + signe + padding(binElem, k2-1)
       
        
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


def nbBlocsOverflow(k1, nbOF):
    """Calcule le nombre exact de blocs de 32 bits nécessaires pour stocker nbOF entiers
       de k1 bits chacun, avec padding à la fin de chaque bloc."""
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
  
    nbTabOF = nbBlocsOverflow(k1, nbOF)

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
        for j in range(0,len(elem),(k2+1)) :
            block = elem[j : j + (k2+1)]
            if(len(block) == (k2+1)) :
                flag = block[0]
                signe = block[1] # '1' négatif '0' positif
                bits = block[2:]
    
                if flag == '0':
                    if signe == '1' :
                        val = - int(bits, 2) 
                    else : 
                        val = int(bits, 2) 

                else:
                    index = int(bits, 2)
                    if index < len(overflowArea):
                        if signe == '1' :
                            val = - int(overflowArea[index], 2) 
                        else : 
                            val = int(overflowArea[index], 2) 
          
                finalList.append(val)
       

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
    signe = mot[1]
    bits = mot[2:]
   
    if flag == '0':
        if signe == '1' :
            return - int(bits, 2)
        else : 
            return  int(bits, 2)

    else:
        nbTabOF = nbBlocsOverflow(k1, nbOF)
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
            if signe == '1' :
                return -int(overflowArea[index],2)
            else : 
                return int(overflowArea[index],2)


if __name__ == "__main__":
    data = [ -1, 0, 45, -23456, 7865, -6, 0 , 87, 0, 9, -1]
    comp = overflowCompress(data)
    print(comp)
    decomp = overflowDecompress(comp)
    print(decomp)
    print(overflowGet(0,comp))
    print(overflowGet(1,comp))
    print(overflowGet(2,comp))
    print(overflowGet(3,comp))
    print(overflowGet(4,comp))
    print(overflowGet(5,comp))
    print(overflowGet(6,comp))
    print(overflowGet(7,comp))