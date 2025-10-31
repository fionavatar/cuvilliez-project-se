"""
You must implement measures to time the execution of each function. 
Be sure to implement a protocol that you explain carefully,
which measures as accurately as possible the time taken by each function. 
Based on these times, you must calculate the transmission time for a latency t 
at which compression becomes worthwhile.

───────────────────────────────────────────────────────────────
PROTOCOL DE MESURE (explication du protocole mis en œuvre) :

1. Objectif :
   Évaluer précisément le temps de compression, de décompression et d’accès direct
   pour différents modes de compression, puis déterminer si la compression est rentable
   pour une latence donnée (t).

2. Méthodologie :
   - On utilise `time.perf_counter()` pour mesurer le temps écoulé avec une résolution fine
     (micro/nanosecondes selon le système).
   - Chaque fonction (`compress`, `decompress`, `get`) est chronométrée séparément.
   - Pour les accès directs, on calcule la moyenne sur 10 accès aléatoires.
   - On compare le temps total de transmission compressé vs non compressé.

3. Modèle de temps :
   Transmission sans compression :
       T_no_comp = latency_t + taille_originale
   Transmission avec compression :
       T_comp = compression_time + latency_t + taille_compressée + decompression_time

   Compression utile si T_comp < T_no_comp.
───────────────────────────────────────────────────────────────
"""

import time
import random
from src.factory import compressor_factory  # adapter si besoin : src.factory si ton projet est structuré ainsi


def benchmark_compression(data, latency_t):
    """
    Mesure les performances de compression pour les données fournies (data).
    Calcule le temps de transmission à partir d'une latence donnée (t).
    """

    modes = ["overflow", "crossing", "noCrossing"]
    print(f"\n________      Benchmark sur {len(data)} éléments     ________")

    for mode in modes:
        compressor = compressor_factory(mode, data)

        # --- Temps de compression ---
        start = time.perf_counter()
        compressed = compressor.compress(data)
        compression_time = time.perf_counter() - start

        # --- Temps de décompression ---
        start = time.perf_counter()
        decompressed = compressor.decompress(compressed)
        decompression_time = time.perf_counter() - start

        # --- Temps d’accès direct moyen (get) ---
        get_times = []
        for _ in range(10):
            i = random.randint(0, len(data) - 1)
            t0 = time.perf_counter()
            compressor.get(i, compressed)
            t1 = time.perf_counter()
            get_times.append(t1 - t0)
        avg_get_time = sum(get_times) / len(get_times)

        # --- Calcul du ratio de compression ---
        original_bits = len(data) * 32
        compressed_bits = len(compressed) * 32
        ratio = original_bits / compressed_bits if compressed_bits else float('inf')

        # --- Temps de transmission total ---
        T_no_comp = latency_t + len(data)
        T_comp = compression_time + latency_t + len(compressed) + decompression_time
        gain = T_no_comp - T_comp

        # --- Affichage ---
        print(f"{mode:10} | compress: {compression_time:.6f}s | decompress: {decompression_time:.6f}s | "
              f"avg get: {avg_get_time:.6f}s | taille compressée: {len(compressed)} mots")
        print(f"Compression ratio: {ratio:.2f}x | Gain de transmission: {gain:.6f}s")



if __name__ == "__main__":
    data = list(range(10000))
    latency_t = 0.05  # 50 ms
    benchmark_compression(data, latency_t)
