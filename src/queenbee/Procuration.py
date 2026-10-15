# → Un garde vérifie le rôle avant toute lecture.
class Notificateur(Protocol):  # 1 rôle = 1 méthode
    def notifier(self, alerte: Alerte) -> None: ...
 
class ProcurationLecture:      # lecture seule
    def __init__(self, cible, qui: Identite):
        self._cible, self._qui = cible, qui
 
    def lister_ouverts(self) -> list[Incident]:
        if not self._qui.roles & ROLES_LECTURE:
            raise ErreurAccesRefuse(self._qui.nom)
        return self._cible.lister_ouverts()
