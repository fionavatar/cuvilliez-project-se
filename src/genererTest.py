import random
from outils import *
from crossing_compressor import *
from no_crossing_compressor import *

def test_compression_functions():
    # Configurations de test
    test_cases = [
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [15, 3, 4, 23, 28, 1, 17, 18],
        [random.randint(0, 100) for _ in range(50)],
        [random.randint(0, 200) for _ in range(100)],
        [0]*10 + [1]*10 + [50, 75, 100, 0],
    ]

    modes = ['crossing', 'noCrossing']

    for mode in modes:
        print(f"\n--- TEST MODE: {mode} ---\n")
        for idx, case in enumerate(test_cases):
            print(f"Test case {idx+1}: {case}")
            
            # Compression
            if mode == 'crossing':
                compressed = crossingCompress(case)
                decompressed = crossingDecompress(compressed)
            else:
                compressed = noCrossingCompress(case)
                decompressed = noCrossingDecompress(compressed)

            # Vérification complète
            if decompressed == case:
                print("✅ Décompression correcte")
            else:
                print("❌ Erreur de décompression")
                print("Résultat:", decompressed)

            # Test accès direct
            access_errors = 0
            for i in range(len(case)):
                if mode == 'crossing':
                    value = crossingGet(i, compressed)
                else:
                    value = noCrossingGet(i, compressed)
                if value != case[i]:
                    access_errors += 1
                    print(f"❌ Erreur get({i}): attendu {case[i]}, obtenu {value}")
            
            if access_errors == 0:
                print("✅ Accès direct correct pour tous les éléments\n")
            else:
                print(f"❌ {access_errors} erreurs dans l'accès direct\n")

if __name__ == "__main__":
    test_compression_functions()
