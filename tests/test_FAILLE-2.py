import time
import pytest
from queenbee import is_valid_username

def test_faille_2_redos_vulnerability():
    """
    Prouve la FAILLE-2 : ReDoS (Regular Expression Denial of Service).
    L'expression r"^([a-zA-Z0-9]+\s?)*$" combine un quantificateur interne '+'
    et un quantificateur externe '*' avec un espace optionnel '\s?'.
    Un texte long ne se terminant pas par un caractère valide fige le thread.
    """
    # Une chaîne valide ou invalide très courte s'exécute instantanément
    start_safe = time.perf_counter()
    is_valid_username("admin123")
    duration_safe = time.perf_counter() - start_safe
    
    # Construction de la charge utile ReDoS (Evil String)
    # Répétition de caractères alphanumériques suivis d'un caractère invalide (ex: '!') à la fin
    payload = "a" * 30 + "!"
    
    # Mesure du temps d'exécution sur la chaîne malveillante
    start_attack = time.perf_counter()
    is_valid_username(payload)
    duration_attack = time.perf_counter() - start_attack
    
    # Preuve de la faille : l'attaque prend plusieurs ordres de grandeur plus de temps
    # qu'une exécution normale (souvent > 1 seconde pour seulement 30 caractères)
    assert duration_attack > 0.5, f"Le calcul s'est terminé trop vite ({duration_attack:.4f}s). L'expression n'est pas vulnérable."
    assert duration_attack > (duration_safe * 1000), "L'augmentation du temps n'est pas exponentielle."
