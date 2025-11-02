import random
from src.overflow_compressor import OverflowCompressor
from src.crossing_compressor import CrossingCompressor
from src.no_crossing_compressor import NoCrossingCompressor

def test_random_compression(num_tests=5, max_size=100, max_value=1000):
    """
    Effectue des tests aléatoires sur les compresseurs Overflow, Crossing et NoCrossing.
    - num_tests : nombre de tableaux aléatoires à générer
    - max_size : taille maximale d'un tableau
    - max_value : valeur maximale possible d'un élément
    """
    random.seed(42)  # reproductibilité

    compressors = {
        "overflow": OverflowCompressor(),
        "crossing": CrossingCompressor(),
        "noCrossing": NoCrossingCompressor()
    }

    for test_idx in range(1, num_tests + 1):
        size = random.randint(5, max_size)
        data = [random.randint(0, max_value) for _ in range(size)]
        print(f"\n--- Test aléatoire #{test_idx} (taille={size}) ---")
        print("Données originales (10 premières valeurs) :", data[:10], "..." if len(data) > 10 else "")

        for name, compressor in compressors.items():
            compressed = compressor.compress(data)
            decompressed = compressor.decompress(compressed)

            # Vérification de la décompression complète
            if decompressed == data:
                print(f"{name:10}  Décompression correcte")
            else:
                print(f"{name:10}  Erreur de décompression")
                print("Décompressé :", decompressed)

            # Vérification de l'accès direct get()
            access_errors = 0
            for i, val in enumerate(data):
                value = compressor.get(i, compressed)
                if value != val:
                    access_errors += 1
                    print(f" {name} get({i}): attendu {val}, obtenu {value}")

            if access_errors == 0:
                print(f"{name:10} Accès direct correct pour tous les éléments")
            else:
                print(f"{name:10}  {access_errors} erreurs dans l'accès direct")

            print(f"{name:10} Taille compressée : {len(compressed)} mots de 32 bits")

if __name__ == "__main__":
    test_random_compression(num_tests=5, max_size=50, max_value=500)
