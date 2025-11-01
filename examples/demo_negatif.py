import random
from src.negatif_compressor import NegatifCompressor

def run_test(name, data):
    compressor = NegatifCompressor()
    compressed = compressor.compress(data)
    decompressed = compressor.decompress(compressed)

    # Vérification du résultat
    success = decompressed == data

    # Vérification de l'accès direct
    direct_access_ok = True
    for i in range(len(data)):
        if compressor.get(i, compressed) != data[i]:
            direct_access_ok = False
            break

    if success and direct_access_ok:
        print(f"[OK] {name}")
    elif not success:
        print(f"[FAIL] {name} - Erreur de décompression")
        print(f"  attendu: {data}")
        print(f"  obtenu : {decompressed}")
    else:
        print(f"[FAIL] {name} - Erreur d'accès direct")


def main():
    tests = {
        "Petits positifs": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Petits négatifs": [-1, -2, -3, -4, -5, -6],
        "Mélange simple": [-1, 0, 45, -23456, 7865, -6, 0, 87, 0, 9, -1],
        "Grands nombres": [1, 2, 3, 1024, 65535, 999999, -1234567],
        "Zéros uniquement": [0, 0, 0, 0, 0],
        "Un seul élément positif": [42],
        "Un seul élément négatif": [-42],
        "Liste vide": [],
        "Alternance signes": [(-1)**i * i for i in range(1, 20)],
        "Doublons": [5, 5, 5, 5, 5],
        "Petits entiers avec zéro": [0, 1, -1, 2, -2, 3, -3],
        "Valeurs max 16 bits": [32767, -32768, 16384, -16384],
        "Overflow 32 bits": [2**31 - 1, -2**31, 2**30, -2**30],
        "Séquence croissante": list(range(0, 50)),
        "Séquence décroissante": list(range(50, 0, -1)),
        "Valeurs aléatoires petites": [random.randint(-100, 100) for _ in range(30)],
        "Valeurs aléatoires moyennes": [random.randint(-2**15, 2**15) for _ in range(30)],
        "Valeurs aléatoires grandes": [random.randint(-2**20, 2**20) for _ in range(30)],
        "Beaucoup de zéros": [0] * 100,
        "Grand tableau mixte": [random.randint(-10000, 10000) for _ in range(200)],
    }

    total = len(tests)
    ok = 0

    for name, data in tests.items():
        try:
            run_test(name, data)
            ok += 1
        except Exception as e:
            print(f"[ERROR] {name} - Exception : {e}")

    print(f"\nRésultats : {ok}/{total} tests réussis.")


if __name__ == "__main__":
    main()
