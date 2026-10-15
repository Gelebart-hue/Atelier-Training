# → Une ligne de journal devient un événement, sinon elle est refusée.
LIGNE_MAX = 512       # borne AVANT la regex
 
_SSHD = re.compile(   # ancrée, sans quantificateur imbriqué
    r"(?P<horo>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})"
    r" sshd: (?P<resultat>Failed|Accepted) password for "
    r"(?P<nom>[a-z_][a-z0-9_.-]{0,31}) from (?P<ip>[0-9a-fA-F:.]{2,45})")
 
def analyser_ligne_sshd(ligne: str) -> EvenementSecurite:
    if len(ligne) > LIGNE_MAX:
        raise ErreurDomaine("ligne trop longue")
    corresp = _SSHD.fullmatch(ligne.strip())
    if corresp is None:
        raise ErreurDomaine("format non reconnu")
    return EvenementSecurite(           # le domaine revalide
        ip_source=corresp["ip"], utilisateur=corresp["nom"],
        action="connexion_echouee" if corresp["resultat"] == "Failed"
               else "connexion_ok",
        horodatage=datetime.fromisoformat(corresp["horo"]))