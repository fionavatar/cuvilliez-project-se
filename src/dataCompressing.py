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

# trop lent ?
def nombreBits ( l ) :
    """
    Calcule le nombre de bits nécessaire à la conpression. 
    Astuce on a uniquement besoin de calculer pour l'entier max.
    Pour les entiers positifs uniquement.

    En entrée :
    l : array d'entiers

    En sortie :
    k : un entier
    """
    binTab = []
    k = 0
    for elem in l :

        if elem == 0 :
            k = 1
            binTab.append('0')
        else :
            c = elem
            bin = ""
            while c > 0 :
                bin = bin + str(c%2)
                c = c // 2
        
            if len(bin) > k :
                k = len(bin)
            binTab.append(''.join(reversed(bin)))

    return k, binTab

# plus rapide

def compute_k(array):
    max_val = max(array)
    return math.floor(math.log2(max_val)) + 1 if max_val > 0 else 1


def get( i ) :
    """
    permet l’accès direct à l’élément i sans décompression complète

    Entrée :
    i un entier

    Sortie :
    l'élément à l'indice i
    """


# 1er mode de compression
"""
crossing allowed — les entiers compressés peuvent s’étendre sur deux mots de sortie 
(ex : un entier commence dans la fin d’un mot de 32 bits et continue dans le mot suivant).
"""

def compress( input ) :
    """
    compresse int[] input
    """

def decompress( output ) :
    """
    decompresse int[] output
    """

#2ème mode de compression   
"""
no crossing — chaque entier compressé doit être entièrement contenu 
dans un mot de sortie (donc on peut gaspiller bits et aligner).
"""

if __name__ == "__main__":
    values = [5, 3, 7, 1, 2, 6] # Example values (6 values, each 3 bits)
    data = [ 1, 14, 67, 35, 89]
    data = [ 12, 25, 31]
    print(nombreBits([1, 2, 3, 4, 5]))  # ➜ 3
    print(nombreBits([12, 25, 31]))     # ➜ 5
    print(nombreBits([0, 0, 0]))        # ➜ 1

    print(compute_k([1, 2, 3, 4, 5]))  # ➜ 3
    print(compute_k([12, 25, 31]))     # ➜ 5
    print(compute_k([0, 0, 0]))        # ➜ 1
