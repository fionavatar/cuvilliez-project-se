# Software Engineering Project 2025 — Data Compression for Faster Transmission

Ce projet étudie la transmission de **tableaux d'entiers** via différents modes de compression.
L'objectif est de réduire le nombre d'entiers transmis tout en gardant **l'accès direct aux données** après compression.

## Modes de compression

- `crossing` : un entier peut être écrit sur deux blocs consécutifs
- `noCrossing` : pas de chevauchement possible
- `overflow` : basé sur la logique de `noCrossing` mais utilise une **table d’overflow** pour optimiser le stockage des entiers très grands

## Benchmarks

Des benchmarks sont implémentés pour mesurer :
- le temps de compression (`compress()`)
- le temps de décompression (`decompress()`)
- le temps moyen d’accès direct (`get()`)
- le ratio de compression et le gain de transmission

**Latence simulée** : 5 ms

## Dépendances

- Python 3
- Librairies standard : `random`, `time`, `sys`, `math`

## Usage

```bash
python3 src.main.py [mode] [fichier_optionnel]
```

Modes disponibles : crossing | noCrossing | overflow

Exemple d'utilisation : 
```bash
python3 -m examples.demo_no_crossing
```
```bash
python3 -m examples.testAll
```
```bash
python3 -m src.main crossing ./tests/data7.txt
```
Tester des tableaux avec des négatifs :
```bash
python3 -m examples.demo_negatif
``