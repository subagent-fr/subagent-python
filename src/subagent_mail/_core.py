"""Transport HTTP du SDK : un POST par opération. Bibliothèque standard seulement."""
from __future__ import annotations

import http.client
import json
import os
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Mapping, Optional

from ._version import __version__
from .errors import SubagentConnectionError, SubagentError

BASE_URL = "https://api.subagent.fr"
ENV_KEY = "SUBAGENT_KEY"
ENV_BASE_URL = "SUBAGENT_BASE_URL"

# Réponses d'un mandataire devant le service, sans corps d'erreur Subagent.
_PASSERELLE = (502, 503, 504)


class Transport:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 2,
    ) -> None:
        # Une clé donnée l'emporte sur l'environnement ; "" veut dire « sans clé », même si SUBAGENT_KEY existe.
        self.api_key = (api_key if api_key is not None else os.environ.get(ENV_KEY)) or None
        self.base_url = (base_url or os.environ.get(ENV_BASE_URL) or BASE_URL).rstrip("/")
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))
        self.attente = 0.5  # secondes avant le premier réessai, doublées ensuite

    def post(
        self,
        operation: str,
        arguments: Mapping[str, Any],
        *,
        idempotency_key: Optional[str] = None,
        rejouable: bool = False,
    ) -> Dict[str, Any]:
        """Appelle `POST /v1/{operation}` et rend le résultat de l'opération.

        `rejouable` : l'appel peut être rejoué sans risque de doublon (lecture seule, ou clé
        d'idempotence). Seul un appel rejouable est réessayé, et seulement quand le serveur
        n'a pas répondu ; un refus du serveur n'est jamais réessayé.
        """
        corps = json.dumps(
            {nom: valeur for nom, valeur in arguments.items() if valeur is not None},
            ensure_ascii=False,
        ).encode("utf-8")
        entetes = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "subagent-mail-python/" + __version__,
        }
        if self.api_key:
            entetes["Authorization"] = "Bearer " + self.api_key
        if idempotency_key is not None:
            entetes["Idempotency-Key"] = idempotency_key
        url = "%s/v1/%s" % (self.base_url, operation)
        essais = 1 + (self.max_retries if rejouable else 0)
        for essai in range(essais):
            dernier = essai == essais - 1
            requete = urllib.request.Request(url, data=corps, headers=entetes, method="POST")
            try:
                with urllib.request.urlopen(requete, timeout=self.timeout) as reponse:
                    return _objet(reponse.read(), reponse.status)
            except urllib.error.HTTPError as erreur:
                refus = _refus(erreur.read(), erreur.code)
                if refus is not None:
                    raise refus from None
                if erreur.code in _PASSERELLE and not dernier:
                    time.sleep(self.attente * (2 ** essai))
                    continue
                raise SubagentConnectionError(
                    "Réponse inattendue du serveur (HTTP %d), sans corps d'erreur Subagent." % erreur.code,
                    status=erreur.code,
                ) from None
            except (urllib.error.URLError, http.client.HTTPException, OSError) as erreur:
                if not dernier:
                    time.sleep(self.attente * (2 ** essai))
                    continue
                suite = (
                    ""
                    if rejouable
                    else " L'appel n'a pas été réessayé : il a pu aboutir. Relisez l'état avant de"
                    " recommencer, ou rejouez-le avec la même idempotency_key."
                )
                raise SubagentConnectionError(
                    "Pas de réponse de %s (%s).%s" % (self.base_url, getattr(erreur, "reason", erreur), suite)
                ) from erreur
        raise AssertionError("inatteignable")  # pragma: no cover


def _objet(corps: bytes, statut: int) -> Dict[str, Any]:
    try:
        valeur = json.loads(corps.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        valeur = None
    if not isinstance(valeur, dict):
        raise SubagentConnectionError("Réponse illisible du serveur (HTTP %d)." % statut, status=statut)
    return valeur


def _refus(corps: bytes, statut: int) -> Optional[SubagentError]:
    """Le refus du serveur, s'il a la forme {"error": {"code", "message", "hint"}}."""
    try:
        valeur = json.loads(corps.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    erreur = valeur.get("error") if isinstance(valeur, dict) else None
    if not isinstance(erreur, dict) or not isinstance(erreur.get("code"), str):
        return None
    return SubagentError(
        status=statut,
        code=erreur["code"],
        message=str(erreur.get("message") or ""),
        hint=erreur.get("hint") if isinstance(erreur.get("hint"), str) else None,
    )
