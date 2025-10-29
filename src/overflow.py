from dataCompressing import *
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


def overflowCompress ( input ) :
    """
    compresse int[] input

    entree : input un tableau d'entiers décimaux
    sortie : un tableau d'entiers décimaux (compressé)
    """
    listeBin = decimalToBinary(input)
    longest_string = max(listeBin, key=len)
    print(longest_string)


def overflowDecompress( output ) :
    """
    decompresse int[] output
    """


def overflowGet( i, array ) :
    """
    permet l’accès direct à l’élément i sans décompression complète

    Entrée :
    i un entier

    Sortie :
    l'élément à l'indice i
    """
