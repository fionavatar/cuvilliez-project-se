

data = [ 1, 14, 67, 35, 89]

def nombreBits ( l ) :
    """
    Calcule le nombre de bits nécessaire à la conpression.
    En entrée :
    l : array d'entiers
    En sortie :
    k : un entier
    """
    k = 0
    for elem in l :
        c = elem
        bin = ""
        i = 0
        while c > 1 :
            bin = bin + str(c%2)
            c = c // 2
            i+=1
        if c > k :
            k = c
    return c 


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