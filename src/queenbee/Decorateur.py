# → On laisse passer quelques alertes par minute et on compte le surplus.
class NotificateurDebitLimite:     # même interface que Notificateur
    def __init__(self, cible: Notificateur, max_par_fenetre: int,
                 fenetre_s: float, horloge=time.monotonic) -> None:
        self._cible, self._max = cible, max_par_fenetre
        self._fenetre, self._horloge = fenetre_s, horloge
        self._debut, self._compte, self.rejetees = horloge(), 0, 0
 
    def notifier(self, alerte: Alerte) -> None:
        instant = self._horloge()
        if instant - self._debut >= self._fenetre:
            self._debut, self._compte = instant, 0
        if self._compte >= self._max:
            self.rejetees += 1     # compté, jamais silencieux
            return
        self._compte += 1
        self._cible.notifier(alerte)
 
notificateur = NotificateurAudite(NotificateurDebitLimite(Console(), 30, 60))
