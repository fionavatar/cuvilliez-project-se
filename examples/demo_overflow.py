from src.overflow_compressor import OverflowCompressor

def main():
    # Exemple de données
    data = [1, 2, 3, 1024, 4, 5, 2048]

    compressor = OverflowCompressor()

    # Compression
    compressed = compressor.compress(data)
    print("Données compressées :", compressed)

    # Décompression
    decompressed = compressor.decompress(compressed)
    print("Données décompressées :", decompressed)

    # Vérification de l’accès direct
    print("\nAccès direct aux éléments :")
    for i in range(len(data)):
        value = compressor.get(i, compressed)
        print(f"Index {i}: {value}")

    # Vérification que la décompression complète correspond
    assert decompressed == data, "Erreur : décompression incorrecte"

if __name__ == "__main__":
    main()
