# → Un blocage annulable, et un incident aux étapes imposées.
@dataclass(slots=True)
class CommandeBlocageIp:                   # Commande
    parefeu: Parefeu
    ip: str
    def __post_init__(self) -> None:
        ipaddress.ip_address(self.ip)      # pas de chaîne brute
    def executer(self) -> None: self.parefeu.bloquer(self.ip)
    def annuler(self) -> None:    self.parefeu.debloquer(self.ip)
 
_TRANSITIONS = {                           # État (table)
    OUVERT:  {TRIE},
    TRIE:    {CONFINE, CLOS},
    CONFINE: {CLOS},
    CLOS:    set(),                        # état final
}
def passer_a(self, nouveau: StatutIncident) -> None:
    if nouveau not in _TRANSITIONS[self.statut]:
        raise ErreurDomaine(f"{self.statut} -> {nouveau} interdit")
    self.statut = nouveau
