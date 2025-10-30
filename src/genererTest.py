import random
from outils import *
from crossing_compressor import *
from no_crossing_compressor import *
from overflow_compressor import *

def test_compression_functions():
    # Seed pour reproductibilité
    random.seed(42)

    # Configurations de test
    test_cases = [
        [],  # Tableau vide
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [15, 3, 4, 23, 28, 1, 17, 18],
        [random.randint(0, 100) for _ in range(50)],
        [random.randint(0, 200) for _ in range(100)],
        [0]*10 + [1]*10 + [50, 75, 100, 0],
        [1000]*20,  # Tous identiques, overflow garanti
        [2**i for i in range(20)],  # Valeurs très grandes
    ]

    modes = ['crossing', 'noCrossing', 'overflow']

    for mode in modes:
        print(f"\n=== TEST MODE: {mode} ===\n")
        for idx, case in enumerate(test_cases):
            print(f"Test case {idx+1}: {case if len(case)<=10 else str(case[:10])+'...'}")
            
            # Compression
            if mode == 'crossing':
                compressed = crossingCompress(case)
                decompressed = crossingDecompress(compressed)
            else:
                compressed = noCrossingCompress(case)
                decompressed = noCrossingDecompress(compressed)

            print(f"Taille compressée: {len(compressed)} mots de 32 bits")

            # Vérification complète
            if decompressed == case:
                print("✅ Décompression correcte")
            else:
                print("❌ Erreur de décompression")
                print("Résultat:", decompressed)

            # Test accès direct
            access_errors = 0
            for i, expected in enumerate(case):
                if mode == 'crossing':
                    value = crossingGet(i, compressed)
                else:
                    value = noCrossingGet(i, compressed)
                if value != expected:
                    access_errors += 1
                    print(f"❌ Erreur get({i}): attendu {expected}, obtenu {value}")
            
            if access_errors == 0:
                print("✅ Accès direct correct pour tous les éléments\n")
            else:
                print(f"❌ {access_errors} erreurs dans l'accès direct\n")


if __name__ == "__main__":
    test_compression_functions()
