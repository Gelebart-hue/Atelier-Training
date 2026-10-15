"""Jour 2/3 — entrées malveillantes aux ports d'entrée + test par propriétés (Hypothesis)."""

import contextlib
import json
import time

import pytest
from hypothesis import given
from hypothesis import strategies as st

from queenbee.adapters.inbound.agent_api import UnauthenticatedError, parse_agent_message, sign
from queenbee.adapters.inbound.log_parser import parse_sshd_line
from queenbee.adapters.inbound.threat_feed import ThreatFeedTranslator
from queenbee.bootstrap import build_app
from queenbee.config import ConfigError, SettingsBuilder, settings_from_env
from queenbee.domain.model import DomainError



# → 1 000 alertes envoyées, le SOC n'en reçoit que 3.
def test_abus_limiteur_absorbe_inondation() -> None:
    espion, instant = NotificateurEspion(), [0.0]
    limite = NotificateurDebitLimite(espion, max_par_fenetre=3,
                                     fenetre_s=60,
                                     horloge=lambda: instant[0])
    for _ in range(1_000):              # l'attaquant inonde
        limite.notifier(alerte)
    assert len(espion.recus) == 3       # le SOC reste lisible
    assert limite.rejetees == 997       # et l'excès est tracé
    instant[0] = 61.0                   # fenêtre suivante
    limite.notifier(alerte)
    assert len(espion.recus) == 4