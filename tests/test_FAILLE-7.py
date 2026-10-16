import time
import pytest
from queenbee import check_token

def test_faille_7_timing_vulnerability():
    """
    Prouve la FAILLE-7 : Vulnérabilité aux attaques temporelles (Timing Attack).
    L'opérateur '==' s'arrête au premier caractère faux, créant une fuite d'information.
    """
    # Nombre d'itérations pour lisser les variations de l'OS et stabiliser les mesures
    ITERATIONS = 200_000

    # Charge utile A : Aucun caractère en commun (Échec immédiat)
    bad_payload = "xxxxxxxxxxxx"
    
    # Charge utile B : Premier caractère correct ('q'), le reste faux (Échec après 1 étape)
    semi_correct_payload = "qxxxxxxxxxxx"

    # 1. Mesure du temps pour un échec au premier caractère
    start_bad = time.perf_counter()
    for _ in range(ITERATIONS):
        check_token(bad_payload)
    end_bad = time.perf_counter() - start_bad

    # 2. Mesure du temps pour un échec au deuxième caractère
    start_semi = time.perf_counter()
    for _ in range(ITERATIONS):
        check_token(semi_correct_payload)
    end_semi = time.perf_counter() - start_semi

    # Preuve de la faille : Le traitement avec le premier caractère valide 
    # prend plus de temps de manière mesurable.
    différence = end_semi - start_bad
    
    assert end_semi > end_bad, (
        f"Pas de fuite temporelle détectée ({différence:.6f}s). "
        "L'opérateur n'évalue peut-être pas à temps variable ou les itérations sont insuffisantes."
    )
