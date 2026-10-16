import pytest
from queenbee import conn, close_incident

@pytest.fixture(autouse=True)
def setup_database():
    """Prépare la base de données avec un incident critique ouvert."""
    conn.execute("DELETE FROM incident")
    conn.execute("INSERT INTO incident (id, ip, status) VALUES (42, '192.168.1.50', 'open')")
    conn.commit()

def test_faille_5_broken_authorization():
    """
    Prouve la FAILLE-5 : Absence de contrôle d'autorisation.
    Un utilisateur sans privilèges ('guest_user') ne devrait pas pouvoir modifier le statut.
    """
    # 1. Un utilisateur non autorisé tente de clore l'incident
    attacker_user = "guest_user"
    incident_id_to_exploit = 42

    # 2. Exécution de l'action par l'attaquant
    # Le test s'attend à ce qu'une exception de type PermissionError soit levée.
    # Si le code vulnérable s'exécute sans erreur, le bloc 'with pytest.raises' échouera.
    with pytest.raises(PermissionError, match="Accès refusé"):
        close_incident(user=attacker_user, incident_id=incident_id_to_exploit)

    # 3. Preuve supplémentaire : Vérification dans la base de données
    # Si le statut est passé à 'closed', la faille est confirmée.
    cursor = conn.execute("SELECT status FROM incident WHERE id = ?", (incident_id_to_exploit,))
    status = cursor.fetchone()[0]
    
    # Dans le code vulnérable actuel, cette assertion échouera car le statut aura été modifié.
    assert status == "open", "La faille est présente : un utilisateur non autorisé a pu clore l'incident."
