from src.crossing_compressor import CrossingCompressor
from src.benchmarks.measures import benchmark_compression

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

    latency_t = 0.05  # ex : 50 ms
    benchmark_compression(data, latency_t, "crossing")

    # Vérification
    assert decompressed == data, "Erreur : décompression incorrecte"

if __name__ == "__main__":
    main()
