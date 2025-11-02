import sys
from src.factory import compressor_factory
from src.benchmarks.measures import benchmark_compression

def run_test(data, mode):
    print(f"\n________  MODE : {mode}   ________")
    print(f"Données d'entrée : {data}\n")

    compressor = compressor_factory(mode, data)

    try:
        compressed = compressor.compress(data)
        print("Compression réussie :", compressed)

        decompressed = compressor.decompress(compressed)
        print("Décompression :", decompressed)

        if decompressed == data:
            print("Décompression correcte !")
        else:
            print("Erreur de décompression !")

        # Test accès direct avec get() pour tous les éléments
        for i in range(len(data)):
            value = compressor.get(i, compressed)
            if value != data[i]:
                print(f"get({i}) = {value}, attendu {data[i]}")
                break
        else:
            print("Accès direct correct pour tous les éléments")

    except Exception as e:
        print("Erreur :", e)

def load_data_from_file(filepath):
    """Charge une liste d'entiers depuis un fichier texte"""
    try:
        with open(filepath, "r") as f:
            content = f.read().strip()
        if not content:
            raise ValueError("Le fichier est vide !")
        return [int(x) for x in content.split()]
    except Exception as e:
        print(f"Erreur de lecture du fichier : {e}")
        sys.exit(1)

def main():
    """
    Usage :
      python3 -m src.main.py [mode] [fichier_optionnel]
    """
    if len(sys.argv) < 2:
        print("Usage : python3 -m src.main.py [mode] [fichier_optionnel]")
        print("Modes disponibles : crossing | noCrossing | overflow | negatif")
        sys.exit(1)

    mode = sys.argv[1]

    # Chargement des données
    if len(sys.argv) == 3:
        filepath = sys.argv[2]
        data = load_data_from_file(filepath)
    else:
        data = [1, 2, 3, 1024, 4, 5, 2048]

    # Test fonctionnel
    run_test(data, mode)

    # Mesure de performance
    latency_t = 0.05  # ex : 50 ms à changer si nécessaire
    benchmark_compression(data, latency_t,mode) #benchmark pour le mode demandé

if __name__ == "__main__":
    main()
