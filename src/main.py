import sys
import random
from factory import compressor_factory

def run_test(data, mode):
    print(f"\n=== TEST MODE: {mode} ===")
    print(f"Données d'entrée : {data}\n")

    compressor = compressor_factory(mode, data)

    try:
        compressed = compressor.compress(data)
        print("✅ Compression réussie :", compressed)

        decompressed = compressor.decompress(compressed)
        print("✅ Décompression :", decompressed)

        if decompressed == data:
            print("✅ Décompression correcte !")
        else:
            print("❌ Erreur de décompression !")

        # Test accès direct (si disponible)
        if hasattr(compressor, "get"):
            for i in range(len(data)):
                value = compressor.get(i, compressed)
                if value != data[i]:
                    print(f"❌ get({i}) = {value}, attendu {data[i]}")
                    break
            else:
                print("✅ Accès direct correct pour tous les éléments")

    except Exception as e:
        print("❌ Erreur :", e)

def load_data_from_file(filepath):
    """Charge une liste d'entiers depuis un fichier texte."""
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
      python main.py overflow
      python main.py crossing test_data.txt
    """
    if len(sys.argv) == 1:
        print("Modes disponibles : crossing | noCrossing | overflow")
        mode = input("Choisir un mode : ").strip()
        path = input("Chemin vers un fichier de test (optionnel) : ").strip()
        if path:
            data = load_data_from_file(path)
        else:
            data = [random.randint(0, 100) for _ in range(20)]
        run_test(data, mode)


    if len(sys.argv) < 2:
        print("Usage : python main.py [mode] [fichier (optionnel)]")
        sys.exit(1)

    mode = sys.argv[1]
    data = []

    if len(sys.argv) == 3:
        filepath = sys.argv[2]
        data = load_data_from_file(filepath)
    else:
        # Si aucun fichier, générer des données aléatoires
        data = [random.randint(0, 100) for _ in range(20)]

    run_test(data, mode)


if __name__ == "__main__":
    main()
