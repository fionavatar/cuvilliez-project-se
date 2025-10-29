from dataCompressing import *
import math

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
    listeBin = [padding(elem, k) for elem in decimalToBinary(input)]

    compressedList = []
    strBin = ""

    for elem in listeBin :
        if len(strBin) + k > 32 :
            compressedList.append(strBin.ljust(32, '0'))
            strBin =""
        strBin += elem
    tailleDernier = len(strBin)  # nombre réel de bits dans le dernier mot
    compressedList.append(strBin.ljust(32,'0'))

    return [k, tailleDernier] + binaryToDecimal(compressedList)


def noCrossingDecompress(output):
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




if __name__ == "__main__":
    values = [5, 3, 7, 1, 2, 6] # Example values (6 values, each 3 bits)
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 50, 75, 100, 0]
    #data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #data = [15, 3, 4, 23, 28, 1, 17, 18]
    #data = [75, 95, 95, 22, 40, 77, 67, 97, 17, 9, 91, 60, 24, 69, 96, 62, 7, 11, 65, 60, 24, 90, 44, 15, 52, 14, 7, 94, 50, 8, 48, 32, 0, 42, 37, 73, 98, 42, 10, 84, 19, 52, 76, 72, 56, 3, 92, 4, 37, 62]
    #data = [21, 11, 32, 39, 45, 80, 63, 3, 72, 2, 50, 27, 45, 12, 69, 43, 76, 70, 89, 51, 20, 55, 28, 72, 31, 73, 90, 20, 62, 67, 56, 65, 63, 75, 69, 71, 10, 69, 2, 97, 91, 29, 17, 57, 93, 74, 33, 46, 56, 67]

    print("il faut :")
    print((32//calculerK(data)), "entiers")
    print(data)
    print("Méthode no crossing allowed")
    comp = noCrossingCompress(data)
    print(comp)
    print(noCrossingDecompress(comp))
    print(noCrossingGet(20,comp)) 
    print(noCrossingGet(21,comp))
    print(noCrossingGet(22,comp))
  
   
