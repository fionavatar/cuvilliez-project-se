from factory import compressor_factory
import random

# Choix du mode
mode = "overflow"
compressor = compressor_factory(mode)

data = [0, 1, 2, 3, 1024, 4, 5, 2048]

compressed = compressor.compress(data)
print("Compressed:", compressed)

decompressed = compressor.decompress(compressed)
print("Decompressed:", decompressed)

for i in range(len(data)):
    print(f"get({i}) =", compressor.get(i, compressed))
