import pytest
from queenbee import call_enrichment_service


def test_faille_6_unauthenticated_inter_service_call():
  """Prouve la FAILLE-6 : Appel inter-services sans authentification mutuelle.

  Le service d'enrichissement répond aveuglément à n'importe quel composant qui
  l'interroge, sans exiger de preuve d'identité (jeton, clé, certificat mTLS).
  """
  target_ip = "8.8.8.8"

  # 1. Un appelant totalement anonyme / non authentifié invoque le service
  try:
    response = call_enrichment_service(ip=target_ip)
  except TypeError:
    pytest.fail(
        "Le service requiert déjà des paramètres d'authentification cachés."
    )

  # 2. Preuve de la faille : Le service renvoie les données sans lever d'exception de sécurité
  assert isinstance(
      response, dict
  ), "Le service n'a pas renvoyé un format attendu."
  assert (
      "reputation" in response
  ), "Le service n'a pas traité la demande de l'appelant anonyme."

  # Si aucune exception n'est levée (comme un PermissionError), la faille est validée :
  # N'importe qui sur le réseau peut consommer ou usurper ce service.
