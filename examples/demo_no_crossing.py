from src.no_crossing_compressor import NoCrossingCompressor

def main():
    # Exemple de données
    data = [10, 20, 30, 40, 50, 1000, 2000]

    compressor = NoCrossingCompressor()

    # Compression
    compressed = compressor.compress(data)
    print("Données compressées :", compressed)

    # Décompression
    decompressed = compressor.decompress(compressed)
    print("Données décompressées :", decompressed)

    # Accès direct
    print("\nAccès direct aux éléments :")
    for i in range(len(data)):
        value = compressor.get(i, compressed)
        print(f"Index {i}: {value}")

    # Vérification
    assert decompressed == data, "Erreur : décompression incorrecte"

if __name__ == "__main__":
    main()
