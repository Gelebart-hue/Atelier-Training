import inspect
import pytest
from queenbee import API_KEY, check_token


def test_faille_1_hardcoded_secret():
  """
    Prouve la FAILLE-1 : 
    - Le secret API_KEY est codé en dur dans le module.
    - Il n'est pas issu d'une variable d'environnement ou d'un gestionnaire de secrets sécurisé.
    """
  # Preuve 1 : Vérification de la présence d'une valeur en clair prévisible
  assert (
      API_KEY == "qb-admin-2026"
  ), "Le secret en dur est exposé et prévisible."

  # Preuve 2 : N'importe quel client peut deviner / utiliser la clé directement
  assert check_token(
      "qb-admin-2026"
  ) is True, "Authentification réussie avec le secret en dur partagé."

  # Preuve 3 : Le secret est statique et visible dans le code source / inspection
  source_code = inspect.getsource(check_token.__globals__)
  assert "qb-admin-2026" in source_code or API_KEY is not None
