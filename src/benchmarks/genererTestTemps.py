import random
import time
from factory import compressor_factory

def test_compression_functions():
    # Configurations de test standard
    test_cases = [
       
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [15, 3, 4, 23, 28, 1, 17, 18],
        [random.randint(0, 100) for _ in range(50)],
        [random.randint(0, 200) for _ in range(100)],
        [0]*10 + [1]*10 + [50, 75, 100, 0],
        [1]*50,
        list(range(1000)),
        [random.randint(0, 1000) for _ in range(500)],
    ]

    # Tests stress avec très grandes listes
    stress_tests = [
        list(range(10000)),  # 10k éléments
        [random.randint(0, 10000) for _ in range(50000)],  # 50k aléatoires
        [random.randint(0, 1000) for _ in range(100000)],  # 100k aléatoires
        list(range(500000)),  # 500k éléments croissants
        [random.randint(0, 2000) for _ in range(1000000)],  # 1 million aléatoires
    ]

    modes = ['crossing', 'noCrossing','overflow']


    for mode in modes:
        print(f"\n--- TEST MODE: {mode} ---\n")
        for idx, case in enumerate(test_cases + stress_tests):
            print(f"Test case {idx+1} (len={len(case)})")
            
            compressor = compressor_factory(mode, case)
            
            start = time.time()
            compressed = compressor.compress(case)
            end = time.time()
            compression_time = end - start

            start = time.time()
            decompressed = compressor.decompress(compressed)
            end = time.time()
            decompression_time = end - start
            
            # Vérification complète
            if decompressed == case:
                print("Décompression correcte")
            else:
                print("Erreur de décompression")


        # Accès direct sur 10 éléments aléatoires
            get_times = []
        
            # Test accès direct sur un échantillon pour performance
            sample_indices = [0, len(case)//4, len(case)//2, 3*len(case)//4, len(case)-1] if len(case) > 5 else range(len(case))
            access_errors = 0
            for i in sample_indices:
                t0 = time.time()
                value = compressor.get(i, compressed)
                t1 = time.time()
                get_times.append(t1-t0)
                if value != case[i]:
                    access_errors += 1
                    print(f"Erreur get({i}): attendu {case[i]}, obtenu {value}")
            
            if access_errors == 0:
                print("Accès direct correct pour tous les indices testés\n")
            else:
                print(f"{access_errors} erreurs dans l'accès direct\n")

if __name__ == "__main__":
    test_compression_functions()
