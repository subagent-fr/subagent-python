"""Le comportement du client contre le faux serveur : clé, refus, idempotence, réessais.

    python -m unittest discover -s tests -v
"""
import asyncio
import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from faux_serveur import CLE_AGENT, CLE_HUMAIN, DESTINATAIRE_BLOQUE, OPERATIONS, FauxServeur  # noqa: E402

from subagent_mail import (  # noqa: E402
    CODES,
    AsyncSubagent,
    Subagent,
    SubagentConnectionError,
    SubagentError,
    __version__,
)

BOITE = "inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95"
MESSAGE = "msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48"
ENVOI = dict(inbox_id=BOITE, to="nadia.morel@exemple.com", subject="Rendez-vous de jeudi", text="Bonjour, …")


class AvecServeur(unittest.TestCase):
    def setUp(self):
        self.serveur = FauxServeur().demarrer()
        self.addCleanup(self.serveur.arreter)
        self.client = Subagent(CLE_AGENT, base_url=self.serveur.url)
        self.client._transport.attente = 0  # pas d'attente entre deux réessais pendant les tests


class Cle(AvecServeur):
    def test_la_cle_part_en_en_tete_authorization(self):
        self.client.inbox_status()
        entetes = self.serveur.derniere["entetes"]
        self.assertEqual(entetes["Authorization"], "Bearer " + CLE_AGENT)
        self.assertEqual(entetes["User-Agent"], "subagent-mail-python/" + __version__)
        self.assertEqual(entetes["Content-Type"], "application/json")

    def test_la_cle_se_lit_dans_l_environnement(self):
        ancien = {nom: os.environ.get(nom) for nom in ("SUBAGENT_KEY", "SUBAGENT_BASE_URL")}
        os.environ["SUBAGENT_KEY"] = CLE_AGENT
        os.environ["SUBAGENT_BASE_URL"] = self.serveur.url
        try:
            Subagent().inbox_status()
        finally:
            for nom, valeur in ancien.items():
                os.environ.pop(nom, None) if valeur is None else os.environ.__setitem__(nom, valeur)
        self.assertEqual(self.serveur.derniere["entetes"]["Authorization"], "Bearer " + CLE_AGENT)

    def test_sans_cle_seule_l_inscription_passe(self):
        client = Subagent("", base_url=self.serveur.url)
        self.assertIsNone(client.api_key)
        with self.assertRaises(SubagentError) as refus:
            client.inbox_status()
        self.assertEqual((refus.exception.status, refus.exception.code), (401, "unauthorized"))
        self.assertIn("sign_up", refus.exception.hint)

        inscription = client.sign_up(username="atelier-exemple", human_email="marie@exemple.fr")
        self.assertNotIn("Authorization", self.serveur.derniere["entetes"])
        self.assertEqual(inscription["api_key"], CLE_AGENT)
        # La clé rendue par sign_up sert aux appels suivants du même client.
        self.assertEqual(client.api_key, CLE_AGENT)
        client.verify(otp_code="482913")
        self.assertEqual(self.serveur.derniere["entetes"]["Authorization"], "Bearer " + CLE_AGENT)

    def test_une_cle_inconnue_est_refusee(self):
        with self.assertRaises(SubagentError) as refus:
            Subagent("sak_inconnue", base_url=self.serveur.url).inbox_status()
        self.assertEqual(refus.exception.code, "unauthorized")


class Refus(AvecServeur):
    def test_un_refus_porte_code_message_et_piste(self):
        with self.assertRaises(SubagentError) as refus:
            self.client.send_email(**dict(ENVOI, to=DESTINATAIRE_BLOQUE))
        erreur = refus.exception
        self.assertEqual(erreur.status, 422)
        self.assertEqual(erreur.code, "recipient_suppressed")
        self.assertIn(DESTINATAIRE_BLOQUE, erreur.message)
        self.assertTrue(erreur.hint)
        self.assertEqual(str(erreur), "recipient_suppressed : %s Piste : %s" % (erreur.message, erreur.hint))
        self.assertIn(erreur.code, CODES)
        self.assertEqual(CODES[erreur.code], erreur.status)

    def test_un_agent_ne_valide_pas_son_brouillon(self):
        with self.assertRaises(SubagentError) as refus:
            self.client.approve_message(message_id=MESSAGE)
        self.assertEqual((refus.exception.status, refus.exception.code), (403, "forbidden"))
        self.assertIn("approve", refus.exception.message)
        # La clé d'un humain, elle, porte approve.
        valide = Subagent(CLE_HUMAIN, base_url=self.serveur.url).approve_message(message_id=MESSAGE)
        self.assertEqual(valide["id"], MESSAGE)

    def test_un_refus_n_est_jamais_reessaye(self):
        with self.assertRaises(SubagentError):
            self.client.send_email(**dict(ENVOI, to=DESTINATAIRE_BLOQUE), idempotency_key="cle-1")
        self.assertEqual(self.serveur.connexions, 1)

    def test_un_parametre_inconnu_est_refuse_par_le_serveur(self):
        with self.assertRaises(SubagentError) as refus:
            self.client.call("send_email", dict(ENVOI, thread_id="thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814"))
        self.assertEqual(refus.exception.code, "invalid_argument")
        self.assertIn("thread_id", refus.exception.message)

    def test_une_operation_inconnue(self):
        with self.assertRaises(SubagentError) as refus:
            self.client.call("envoyer_un_fax")
        self.assertEqual((refus.exception.status, refus.exception.code), (404, "unknown_operation"))

    def test_espace_non_verifie(self):
        self.serveur.verifie = False
        with self.assertRaises(SubagentError) as refus:
            self.client.send_email(**ENVOI)
        self.assertEqual(refus.exception.code, "space_unverified")
        self.assertIn("verify", refus.exception.hint)

    def test_chaque_code_du_registre_est_connu_du_sdk(self):
        self.assertEqual(len(CODES), 84)
        for code in ("recipient_suppressed", "duplicate_recipient", "idempotency_conflict", "unauthorized", "forbidden"):
            self.assertIn(code, CODES)


class Arguments(AvecServeur):
    def test_un_argument_absent_ne_part_pas(self):
        self.client.send_email(**ENVOI, html=None, requires_approval=None)
        self.assertEqual(self.serveur.derniere["arguments"], ENVOI)

    def test_brouillon(self):
        resultat = self.client.send_email(**ENVOI, requires_approval=True)
        self.assertEqual(resultat["message"]["status"], "draft")
        self.assertIsNone(resultat["estimated_send_at"])


class Idempotence(AvecServeur):
    def test_la_cle_d_idempotence_part_en_en_tete(self):
        self.client.send_email(**ENVOI, idempotency_key="rdv-jeudi-nadia-morel")
        self.assertEqual(self.serveur.derniere["entetes"]["Idempotency-Key"], "rdv-jeudi-nadia-morel")
        self.assertEqual(self.serveur.derniere["arguments"]["idempotency_key"], "rdv-jeudi-nadia-morel")

    def test_rejouer_ne_cree_rien(self):
        premier = self.client.send_email(**ENVOI, idempotency_key="rdv-jeudi-nadia-morel")
        second = self.client.send_email(**ENVOI, idempotency_key="rdv-jeudi-nadia-morel")
        self.assertFalse(premier["replayed"])
        self.assertTrue(second["replayed"])
        self.assertEqual(second["message"]["id"], premier["message"]["id"])

    def test_meme_cle_autre_contenu_refus_explicite(self):
        self.client.send_email(**ENVOI, idempotency_key="rdv-jeudi-nadia-morel")
        with self.assertRaises(SubagentError) as refus:
            self.client.send_email(**dict(ENVOI, text="Autre texte."), idempotency_key="rdv-jeudi-nadia-morel")
        self.assertEqual((refus.exception.status, refus.exception.code), (409, "idempotency_conflict"))

    def test_reply_to_thread_aussi(self):
        self.client.reply_to_thread(thread_id="thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814", text="Merci.", idempotency_key="reponse-1")
        self.assertEqual(self.serveur.derniere["entetes"]["Idempotency-Key"], "reponse-1")


class Reessais(AvecServeur):
    def test_une_lecture_est_reessayee_quand_le_serveur_ne_repond_pas(self):
        self.serveur.pannes = 2
        etat = self.client.inbox_status()
        self.assertIn("inboxes", etat)
        self.assertEqual(self.serveur.connexions, 3)

    def test_un_envoi_sans_cle_d_idempotence_n_est_pas_reessaye(self):
        self.serveur.pannes = 1
        with self.assertRaises(SubagentConnectionError) as panne:
            self.client.send_email(**ENVOI)
        self.assertEqual(self.serveur.connexions, 1)
        self.assertIn("idempotency_key", str(panne.exception))

    def test_un_envoi_avec_cle_d_idempotence_est_reessaye(self):
        self.serveur.pannes = 1
        resultat = self.client.send_email(**ENVOI, idempotency_key="rdv-jeudi-nadia-morel")
        self.assertEqual(self.serveur.connexions, 2)
        self.assertEqual(resultat["message"]["to"], ENVOI["to"])

    def test_une_reponse_de_mandataire_n_est_pas_un_refus(self):
        self.serveur.passerelles = 1
        with self.assertRaises(SubagentConnectionError) as panne:
            self.client.send_email(**ENVOI)
        self.assertEqual(panne.exception.status, 502)
        self.serveur.passerelles = 1
        self.assertIn("items", self.client.list_threads())  # lecture : réessayée

    def test_max_retries_zero(self):
        client = Subagent(CLE_AGENT, base_url=self.serveur.url, max_retries=0)
        self.serveur.pannes = 1
        with self.assertRaises(SubagentConnectionError):
            client.inbox_status()
        self.assertEqual(self.serveur.connexions, 1)

    def test_delai_depasse(self):
        self.serveur.lenteur = 0.5
        client = Subagent(CLE_AGENT, base_url=self.serveur.url, timeout=0.05, max_retries=0)
        with self.assertRaises(SubagentConnectionError):
            client.inbox_status()

    def test_serveur_injoignable(self):
        client = Subagent(CLE_AGENT, base_url="http://127.0.0.1:9", max_retries=0, timeout=2)
        with self.assertRaises(SubagentConnectionError):
            client.inbox_status()


class Asynchrone(AvecServeur):
    def test_le_client_asynchrone_a_les_memes_methodes(self):
        async def scenario():
            client = AsyncSubagent(CLE_AGENT, base_url=self.serveur.url)
            etat, fils = await asyncio.gather(client.inbox_status(), client.list_threads(status="replied"))
            envoi = await client.send_email(**ENVOI, idempotency_key="rdv-jeudi-nadia-morel")
            try:
                await client.approve_message(message_id=MESSAGE)
            except SubagentError as refus:
                return etat, fils, envoi, refus.code
            return etat, fils, envoi, None

        etat, fils, envoi, code = asyncio.run(scenario())
        self.assertIn("inboxes", etat)
        self.assertIn("items", fils)
        self.assertEqual(envoi["message"]["to"], ENVOI["to"])
        self.assertEqual(code, "forbidden")

    def test_les_deux_clients_couvrent_tout_le_registre(self):
        for nom in OPERATIONS:
            self.assertTrue(callable(getattr(Subagent, nom, None)), nom)
            self.assertTrue(asyncio.iscoroutinefunction(getattr(AsyncSubagent, nom, None)), nom)


if __name__ == "__main__":
    unittest.main()
