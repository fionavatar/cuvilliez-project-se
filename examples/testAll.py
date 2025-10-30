import random
from outils import *
from crossing_compressor import *
from no_crossing_compressor import *
from overflow_compressor import *

def generate_test_cases():
    return [
        [],  # tableau vide (à tester si on gère l'erreur)
        [0],  # un seul élément
        [1]*10,  # tous identiques
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [15, 3, 4, 23, 28, 1, 17, 18],
        [15, 3, 0, 23, 0, 1, 0, 18, 56, 34],
        [random.randint(0, 10) for _ in range(50)],  # petits nombres
        [random.randint(0, 1000) for _ in range(50)],  # valeurs plus grandes
        [0]*10 + [1]*10 + [50, 75, 100, 0],
        [1, 2, 3, 4, 6, 8, 9, 1024, 4, 5, 2048],  # overflow spécifique
        [random.randint(0, 2**10) for _ in range(100)],  # overflow possible
        [2**15, 2**10, 1, 0, 2**5, 2**20],  # valeurs extrêmes
    ]

def test_compression_functions():
    test_cases = generate_test_cases()
    modes = ['crossing', 'noCrossing', 'overflow']

    for mode in modes:
        print(f"\n--- TEST MODE: {mode} ---\n")
        for idx, case in enumerate(test_cases):
            print(f"Test case {idx+1}: {case}")

            # Compression
            try:
                if mode == 'crossing':
                    compressed = crossingCompress(case)
                    decompressed = crossingDecompress(compressed)
                elif mode == 'noCrossing':
                    compressed = noCrossingCompress(case)
                    decompressed = noCrossingDecompress(compressed)
                else:  # overflow
                    compressed = overflowCompress(case)
                    decompressed = overflowDecompress(compressed)
            except Exception as e:
                print(f"❌ Erreur lors de la compression/decompression: {e}")
                continue

            # Vérification complète
            if decompressed == case:
                print("✅ Décompression correcte")
            else:
                print("❌ Erreur de décompression")
                print("Résultat:", decompressed)

            # Test accès direct
            access_errors = 0
            for i in range(len(case)):
                try:
                    if mode == 'crossing':
                        value = crossingGet(i, compressed)
                    elif mode == 'noCrossing':
                        value = noCrossingGet(i, compressed)
                    else:
                        value = overflowGet(i, compressed)

                    if value != case[i]:
                        access_errors += 1
                        print(f"❌ Erreur get({i}): attendu {case[i]}, obtenu {value}")
                except Exception as e:
                    access_errors += 1
                    print(f"❌ Exception get({i}): {e}")

            if access_errors == 0:
                print("✅ Accès direct correct pour tous les éléments\n")
            else:
                print(f"❌ {access_errors} erreurs dans l'accès direct\n")

if __name__ == "__main__":
    test_compression_functions()
