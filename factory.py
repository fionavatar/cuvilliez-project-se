from src.overflow_compressor import OverflowCompressor
from src.crossing_compressor import CrossingCompressor
from src.no_crossing_compressor import NoCrossingCompressor


def compressor_factory(mode: str, data=None):
    """
    Retourne un objet de compression selon le mode.
    Si data est fourni, vérifie que la liste n'est pas vide.
    """
    if data is not None and len(data) == 0:
        raise ValueError("Le tableau fourni est vide !")

    if mode == "overflow":
        return OverflowCompressor()
    elif mode == "crossing":
        return CrossingCompressor()
    elif mode == "noCrossing":
        return NoCrossingCompressor()
    else:
        raise ValueError(f"Mode inconnu: {mode}")
