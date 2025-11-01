from .outils import *


#2ème mode de compression   
"""
no crossing — chaque entier compressé doit être entièrement contenu 
dans un mot de sortie (donc on peut gaspiller bits et aligner).
"""

class NoCrossingCompressor:
    """Compression no crossing allowed"""

    def compress(self, data):
        if not data:
            return []
        return noCrossingCompress(data)

    def decompress(self, compressed):
        return noCrossingDecompress(compressed)

    def get(self, index, compressed):
        return noCrossingGet(index, compressed)


def noCrossingCompress( input ) :
    """
    compresse int[] input

    entree : input un tableau d'entiers décimaux
    sortie : un tableau d'entiers décimaux (compressé)
    """
    if not input :
        return []
    
    k = calculerK(input)
    listeBin = [padding(elem, k) for elem in decimalToBinary(input)]

    compressedList = []
    strBin = ""
    
    tailleDernier = 32
    for elem in listeBin :
        if len(strBin) + k > 32 :
            compressedList.append(strBin.ljust(32, '0'))
            strBin =""
        strBin += elem
    tailleDernier = len(strBin)  # nombre réel de bits dans le dernier mot
    compressedList.append(strBin.ljust(32,'0'))

    return [k, tailleDernier] + binaryToDecimal(compressedList)


def noCrossingDecompress(output):

    if not output :
        return []

    k, tailleDernier = output[0], output[1]
    compList = output[2:]
    
    # convertir chaque mot en binaire avec 32 bits
    compList = [padding(b, 32) for b in decimalToBinary(compList)]
    
    # découper le dernier mot selon la taille du dernier bloc
    compList[-1] = compList[-1][:tailleDernier]
    
    finalList = []
    for elem in compList:
        elemList = []
        for i in range(0,len(elem),k):
            block = elem[i:i+k]
            if len(block) == k:
                elemList.append(block)
        finalList += elemList

    return binaryToDecimal(finalList)



def noCrossingGet( i, array ) :
    
    k, tailleDernier = array[0], array[1]
    compList = array[2:]
    indice = i * k       # position du premier bit de l'entier
    indiceBloc = i // (32 // k)
    indiceMot = indice % 32   
    if indiceBloc == len(compList) - 1 :
        a = noCrossingDecompress([k, tailleDernier, compList[indiceBloc]])
    else :
        a = noCrossingDecompress([k, 32, compList[indiceBloc]])

    return a[(i % (32 // k))]

 
