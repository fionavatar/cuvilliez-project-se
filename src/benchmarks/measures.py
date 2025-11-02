import time
import random
from src.factory import compressor_factory  # adapte le chemin si besoin


def benchmark_compression(data, latency_t, mode=None):
    """
    Mesure les performances de compression pour les données fournies.
    Si 'mode' est précisé, seul ce mode est testé, sinon tous les modes.
    """
    modes = ["overflow", "crossing", "noCrossing", "negatif"]

    if mode:
        if mode not in modes:
            raise ValueError(f"Mode inconnu '{mode}'. Modes valides : {modes}")
        modes_to_test = [mode]
    else:
        modes_to_test = modes

    print(f"\nBenchmark sur {len(data)} éléments — latence : {latency_t:.3f}s")
    print(f"Modes testés : {', '.join(modes_to_test)}\n")

    for mode in modes_to_test:
        compressor = compressor_factory(mode, data)

        start = time.perf_counter()
        compressed = compressor.compress(data)
        compression_time = time.perf_counter() - start

        start = time.perf_counter()
        decompressed = compressor.decompress(compressed)
        decompression_time = time.perf_counter() - start

        get_times = []
        for _ in range(10):
            i = random.randint(0, len(data) - 1)
            t0 = time.perf_counter()
            compressor.get(i, compressed)
            get_times.append(time.perf_counter() - t0)
        avg_get_time = sum(get_times) / len(get_times)

        original_bits = len(data) * 32
        compressed_bits = len(compressed) * 32
        ratio = original_bits / compressed_bits if compressed_bits else float("inf")

        T_no_comp = latency_t + len(data)
        T_comp = compression_time + latency_t + len(compressed) + decompression_time
        gain = T_no_comp - T_comp

        print(f"{mode:10} | compress: {compression_time:.6f}s | decompress: {decompression_time:.6f}s "
              f"| get: {avg_get_time:.6f}s | taille: {len(compressed)} | ratio: {ratio:.2f}x "
              f"| gain: {gain:.6f}s")


if __name__ == "__main__":
    data = list(range(10000))
    latency_t = 0.05

    # Exemple : benchmark d’un seul mode
    # benchmark_compression(data, latency_t, mode="crossing")

    # Benchmark de tous les modes
    benchmark_compression(data, latency_t)
