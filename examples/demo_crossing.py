from src.crossing_compressor import CrossingCompressor

def main():
    # Exemple de données
    data = [5, 3, 7, 1, 2, 6, 1024, 2048]

    compressor = CrossingCompressor()

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
