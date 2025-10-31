from .outils import *

# 1er mode de compression
"""
crossing allowed — les entiers compressés peuvent s’étendre sur deux mots de sortie 
(ex : un entier commence dans la fin d’un mot de 32 bits et continue dans le mot suivant).
"""

class CrossingCompressor:
    """Compression crossing allowed"""

    def compress(self, data):
        if not data:
            return []
        return crossingCompress(data)

    def decompress(self, compressed):
        return crossingDecompress(compressed)

    def get(self, index, compressed):
        return crossingGet(index, compressed)


def crossingCompress ( input ) :
    """
    compresse int[] input

    entree : input un tableau d'entiers décimaux
    sortie : un tableau d'entiers décimaux (compressé)
    """
    if not input :
        return []
    
    k = calculerK(input)
    listeBin = decimalToBinary(input)
   
    compressedList = []
    strBin = ""

    for elem in listeBin :
        elemP = padding(elem, k)
        for c in elemP :
            if len(strBin) == 32 :
                compressedList.append(strBin)
                strBin = ""
            strBin += c
    compressedList.append(strBin)  
    tailleDernier = len(strBin)  # nombre réel de bits dans le dernier mot
    
    return [k, tailleDernier] + binaryToDecimal(compressedList)


 
def crossingDecompress( output ) :
    """
    Décompresse int[] output (mode crossing allowed)

    entrée :  output un tableau d'entiers décimaux (compressé)
    sortie :  un tableau d'entiers décimaux
    """
    if not output :
        return []
    
    k, tailleDernier = output[0], output[1]
    compList = output[2:]
    compList = decimalToBinary(compList)

    # Séparer head et tail
    if len(compList) > 1:
        head = compList[:(-1)]   
    else :
        head = []
    tail = str(compList[-1])#tail ne fait pas forcément 32 bits complets donc on sépare 

    binNb = ""
    elemList = []
    #On s'occupe du head dans un premier temps
    for elem in head :
        elem = padding(elem, 32)
        for i in range(32) : 
            binNb += elem[i]
            if len(binNb) == k :
                elemList.append(binNb)
                binNb = ""
    
    tailList = []
    #On parcourt de gauche à droite  
    tail = padding(tail, tailleDernier)
    for j in range(len(tail)-1, -1, -k):
        start = max(0, j-k+1)
        block = tail[start:j+1] 
        #si le bloc n'est pas complet, on concatène avec ce qu'il nous reste de binNb avec le padding potentiellement manquant 
        if len(block) < k :
            block = binNb + padding(block,(k-len(binNb)))
        tailList.append(block)
    tailList.reverse() #on remet les éléments dans l'ordre 
    elemList +=  tailList

    return binaryToDecimal(elemList) 



def crossingGet(i, array):
    """
    Accès direct à l’élément i sans décompression complète
    Mode crossing allowed.
    """
    k, tailleDernier = array[0], array[1]
    blocs = array[2:]

    bit_index = i * k
    bloc_index = bit_index // 32
    bit_offset = bit_index % 32

    # Bloc courant
    if bloc_index < len(blocs) - 1:
        bloc = bin(blocs[bloc_index])[2:].zfill(32)
    else:  # dernier bloc
        bloc = bin(blocs[bloc_index])[2:].zfill(tailleDernier)

    if bit_offset + k <= len(bloc):  # entier dans un seul bloc
        bits = bloc[bit_offset:bit_offset + k]
    else:  # entier traverse deux blocs
        if bloc_index + 1 < len(blocs) - 1:
            bloc_suiv = bin(blocs[bloc_index + 1])[2:].zfill(32)
        else:  # dernier bloc
            bloc_suiv = bin(blocs[bloc_index + 1])[2:].zfill(tailleDernier)
        remaining = k - (len(bloc) - bit_offset)
        bits = bloc[bit_offset:] + bloc_suiv[:remaining]

    return int(bits, 2)

