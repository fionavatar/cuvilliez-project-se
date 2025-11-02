from src.no_crossing_compressor import NoCrossingCompressor
from src.benchmarks.measures import benchmark_compression


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

    latency_t = 0.05  # ex : 50 ms
    benchmark_compression(data, latency_t, "noCrossing")

    # Vérification
    assert decompressed == data, "Erreur : décompression incorrecte"

if __name__ == "__main__":
    main()
