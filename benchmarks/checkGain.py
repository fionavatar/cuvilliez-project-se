original_bits = len(data) * 32
compressed_bits = len(compressed) * 32
ratio = original_bits / compressed_bits
print(f"Compression ratio: {ratio:.2f}x")

#Si ton ratio > 1, tu as vraiment compressé (tu utilises moins de bits).