# → Chaque alerte devient un incident, puis on prévient tous les abonnés.
def ingerer(self, evenements: Sequence[EvenementSecurite]) -> list[Incident]:
    crees: list[Incident] = []
    for alerte in self._regle.evaluer(evenements):  # Stratégie
        incident = Incident(alerte=alerte)
        self._incidents.ajouter(incident)         # port de sortie
        for notificateur in self._notificateurs:  # Observateur
            notificateur.notifier(alerte)
        crees.append(incident)
    return crees
