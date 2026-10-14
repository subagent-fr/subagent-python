"""Chaque opération du registre, appelée par sa méthode, contre le faux serveur.

Généré depuis le registre d'opérations du serveur (clients/generer.py) : ne le modifiez pas.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from faux_serveur import CLE_HUMAIN, OPERATIONS, FauxServeur  # noqa: E402

from subagent_mail import Subagent  # noqa: E402


class ChaqueOperation(unittest.TestCase):
    """Une méthode par opération du registre : 64 opérations, 64 tests."""

    @classmethod
    def setUpClass(cls):
        cls.serveur = FauxServeur().demarrer()
        cls.addClassCleanup(cls.serveur.arreter)
        cls.client = Subagent(CLE_HUMAIN, base_url=cls.serveur.url)

    def controler(self, nom, minimal, complet):
        """`minimal` : l'appel avec les seuls arguments obligatoires ; `complet` : avec tous."""
        operation = OPERATIONS[nom]
        # Arguments obligatoires seuls : le résultat est l'exemple de l'opération, tel quel.
        self.serveur.verifie = operation["espace"] != "non vérifié"
        resultat = minimal()
        self.assertEqual(self.serveur.derniere["operation"], nom)
        self.assertEqual(self.serveur.derniere["arguments"], operation["obligatoires"])
        self.assertEqual(resultat, operation["exemple"])
        # Tous les arguments : chacun arrive au serveur sous son nom, avec sa valeur.
        self.serveur.verifie = operation["espace"] != "non vérifié"
        resultat = complet()
        self.assertEqual(self.serveur.derniere["arguments"], operation["arguments"])
        self.assertEqual(sorted(resultat), sorted(operation["exemple"]))
        self.assertEqual(self.serveur.derniere["entetes"].get("Idempotency-Key"),
                         operation["arguments"].get("idempotency_key"))

    def test_sign_up(self):
        self.controler(
            "sign_up",
            lambda: self.client.sign_up(
                username='atelier-exemple',
            ),
            lambda: self.client.sign_up(
                username='atelier-exemple',
                human_email='marie@exemple.fr',
                agent_name='Atelier Exemple',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.sign_up()

    def test_verify(self):
        self.controler(
            "verify",
            lambda: self.client.verify(
                otp_code='482913',
            ),
            lambda: self.client.verify(
                otp_code='482913',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.verify()

    def test_attach_human(self):
        self.controler(
            "attach_human",
            lambda: self.client.attach_human(
                human_email='marie@exemple.fr',
            ),
            lambda: self.client.attach_human(
                human_email='marie@exemple.fr',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.attach_human()

    def test_inbox_status(self):
        self.controler(
            "inbox_status",
            lambda: self.client.inbox_status(),
            lambda: self.client.inbox_status(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
            ),
        )

    def test_workspace_snapshot(self):
        self.controler(
            "workspace_snapshot",
            lambda: self.client.workspace_snapshot(),
            lambda: self.client.workspace_snapshot(
                known_revision='r-2026-10-14-1',
            ),
        )

    def test_activity_report(self):
        self.controler(
            "activity_report",
            lambda: self.client.activity_report(),
            lambda: self.client.activity_report(
                period='week',
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
            ),
        )

    def test_list_events(self):
        self.controler(
            "list_events",
            lambda: self.client.list_events(),
            lambda: self.client.list_events(
                day='2026-10-14',
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                contact='nadia.morel@exemple.com',
                domain='agents.exemple.fr',
                cursor='eyJhIjoiMjAyNi0xMC0xMyJ9',
                limit=20,
            ),
        )

    def test_billing_status(self):
        self.controler(
            "billing_status",
            lambda: self.client.billing_status(),
            lambda: self.client.billing_status(),
        )

    def test_subscribe(self):
        self.controler(
            "subscribe",
            lambda: self.client.subscribe(),
            lambda: self.client.subscribe(
                plan='mail-19',
            ),
        )

    def test_cancel_subscription(self):
        self.controler(
            "cancel_subscription",
            lambda: self.client.cancel_subscription(),
            lambda: self.client.cancel_subscription(),
        )

    def test_list_inboxes(self):
        self.controler(
            "list_inboxes",
            lambda: self.client.list_inboxes(),
            lambda: self.client.list_inboxes(
                cursor='eyJhIjoiMjAyNi0xMC0xMyJ9',
                limit=20,
            ),
        )

    def test_create_inbox(self):
        self.controler(
            "create_inbox",
            lambda: self.client.create_inbox(
                username='atelier-exemple',
                display_name='Marie d’Atelier Exemple',
            ),
            lambda: self.client.create_inbox(
                username='atelier-exemple',
                display_name='Marie d’Atelier Exemple',
                domain='agents.exemple.fr',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.create_inbox()

    def test_update_inbox(self):
        self.controler(
            "update_inbox",
            lambda: self.client.update_inbox(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                display_name='Marie d’Atelier Exemple',
            ),
            lambda: self.client.update_inbox(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                display_name='Marie d’Atelier Exemple',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.update_inbox()

    def test_delete_inbox(self):
        self.controler(
            "delete_inbox",
            lambda: self.client.delete_inbox(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                confirm=True,
            ),
            lambda: self.client.delete_inbox(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                confirm=True,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.delete_inbox()

    def test_request_inbox_review(self):
        self.controler(
            "request_inbox_review",
            lambda: self.client.request_inbox_review(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
            ),
            lambda: self.client.request_inbox_review(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                note='A demandé à ne plus être contactée.',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.request_inbox_review()

    def test_add_domain(self):
        self.controler(
            "add_domain",
            lambda: self.client.add_domain(
                domain='agents.exemple.fr',
            ),
            lambda: self.client.add_domain(
                domain='agents.exemple.fr',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.add_domain()

    def test_verify_domain(self):
        self.controler(
            "verify_domain",
            lambda: self.client.verify_domain(
                domain='agents.exemple.fr',
            ),
            lambda: self.client.verify_domain(
                domain='agents.exemple.fr',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.verify_domain()

    def test_list_domains(self):
        self.controler(
            "list_domains",
            lambda: self.client.list_domains(),
            lambda: self.client.list_domains(),
        )

    def test_domain_quality(self):
        self.controler(
            "domain_quality",
            lambda: self.client.domain_quality(
                domain='agents.exemple.fr',
            ),
            lambda: self.client.domain_quality(
                domain='agents.exemple.fr',
                days=30,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.domain_quality()

    def test_remove_domain(self):
        self.controler(
            "remove_domain",
            lambda: self.client.remove_domain(
                domain='agents.exemple.fr',
                confirm=True,
            ),
            lambda: self.client.remove_domain(
                domain='agents.exemple.fr',
                confirm=True,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.remove_domain()

    def test_send_email(self):
        self.controler(
            "send_email",
            lambda: self.client.send_email(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                to='nadia.morel@exemple.com',
                subject='Rendez-vous de jeudi',
                text='Bonjour Madame Morel,\n\nPouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?\n\nBien à vous,\nMarie',
            ),
            lambda: self.client.send_email(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                to='nadia.morel@exemple.com',
                subject='Rendez-vous de jeudi',
                text='Bonjour Madame Morel,\n\nPouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?\n\nBien à vous,\nMarie',
                to_name='Nadia Morel',
                test=False,
                from_address='marie@exemple.fr',
                html='<p>Bonjour Madame Morel,</p><p>Pouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?</p><p>Bien à vous,<br>Marie</p>',
                reply_to='marie@exemple.fr',
                metadata={'dossier': 'rdv-jeudi'},
                requires_approval=True,
                send_after='2026-10-13T09:00:00+02:00',
                idempotency_key='rdv-jeudi-nadia-morel',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.send_email()

    def test_list_threads(self):
        self.controler(
            "list_threads",
            lambda: self.client.list_threads(),
            lambda: self.client.list_threads(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                status='replied',
                unanswered=True,
                archived=False,
                unread=True,
                label='devis',
                folder='received',
                since='2026-10-12T00:00:00+02:00',
                query='exemple.com',
                cursor='eyJhIjoiMjAyNi0xMC0xMyJ9',
                limit=20,
            ),
        )

    def test_classify_thread(self):
        self.controler(
            "classify_thread",
            lambda: self.client.classify_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
            ),
            lambda: self.client.classify_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
                labels=['devis'],
                archived=False,
                read=True,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.classify_thread()

    def test_inspect_domain(self):
        self.controler(
            "inspect_domain",
            lambda: self.client.inspect_domain(
                domain='agents.exemple.fr',
            ),
            lambda: self.client.inspect_domain(
                domain='agents.exemple.fr',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.inspect_domain()

    def test_list_contacts(self):
        self.controler(
            "list_contacts",
            lambda: self.client.list_contacts(),
            lambda: self.client.list_contacts(
                query='exemple.com',
                label='devis',
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                subscription='subscribed',
                offset=0,
                limit=20,
            ),
        )

    def test_get_contact(self):
        self.controler(
            "get_contact",
            lambda: self.client.get_contact(
                email='nadia.morel@exemple.com',
            ),
            lambda: self.client.get_contact(
                email='nadia.morel@exemple.com',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.get_contact()

    def test_save_contact(self):
        self.controler(
            "save_contact",
            lambda: self.client.save_contact(
                email='nadia.morel@exemple.com',
            ),
            lambda: self.client.save_contact(
                email='nadia.morel@exemple.com',
                name='Atelier Exemple',
                fields={'prenom': 'Nadia', 'societe': 'Atelier Morel'},
                labels=['devis'],
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.save_contact()

    def test_set_contact_audiences(self):
        self.controler(
            "set_contact_audiences",
            lambda: self.client.set_contact_audiences(
                email='nadia.morel@exemple.com',
                audience_ids=['aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26'],
            ),
            lambda: self.client.set_contact_audiences(
                email='nadia.morel@exemple.com',
                audience_ids=['aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26'],
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.set_contact_audiences()

    def test_list_audiences(self):
        self.controler(
            "list_audiences",
            lambda: self.client.list_audiences(),
            lambda: self.client.list_audiences(),
        )

    def test_list_campaign_templates(self):
        self.controler(
            "list_campaign_templates",
            lambda: self.client.list_campaign_templates(),
            lambda: self.client.list_campaign_templates(),
        )

    def test_save_campaign_template(self):
        self.controler(
            "save_campaign_template",
            lambda: self.client.save_campaign_template(
                name='Atelier Exemple',
                subject='Rendez-vous de jeudi',
                text='Bonjour Madame Morel,\n\nPouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?\n\nBien à vous,\nMarie',
            ),
            lambda: self.client.save_campaign_template(
                name='Atelier Exemple',
                subject='Rendez-vous de jeudi',
                text='Bonjour Madame Morel,\n\nPouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?\n\nBien à vous,\nMarie',
                template_id='5d1c8e2a-7b3f-4e9a-b0c6-2f4d8a1e9c37',
                html='<p>Bonjour Madame Morel,</p><p>Pouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?</p><p>Bien à vous,<br>Marie</p>',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.save_campaign_template()

    def test_save_audience(self):
        self.controler(
            "save_audience",
            lambda: self.client.save_audience(
                name='Atelier Exemple',
            ),
            lambda: self.client.save_audience(
                name='Atelier Exemple',
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.save_audience()

    def test_get_audience(self):
        self.controler(
            "get_audience",
            lambda: self.client.get_audience(
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
            ),
            lambda: self.client.get_audience(
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                offset=0,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.get_audience()

    def test_import_contacts(self):
        self.controler(
            "import_contacts",
            lambda: self.client.import_contacts(
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                contacts=[{'email': 'marc.lefevre@exemple.com', 'name': 'Marc Lefèvre', 'fields': {'prenom': 'Marc'}}],
            ),
            lambda: self.client.import_contacts(
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                contacts=[{'email': 'marc.lefevre@exemple.com', 'name': 'Marc Lefèvre', 'fields': {'prenom': 'Marc'}}],
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.import_contacts()

    def test_remove_audience_contact(self):
        self.controler(
            "remove_audience_contact",
            lambda: self.client.remove_audience_contact(
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                email='nadia.morel@exemple.com',
            ),
            lambda: self.client.remove_audience_contact(
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                email='nadia.morel@exemple.com',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.remove_audience_contact()

    def test_list_campaigns(self):
        self.controler(
            "list_campaigns",
            lambda: self.client.list_campaigns(),
            lambda: self.client.list_campaigns(
                offset=0,
                archived=False,
            ),
        )

    def test_save_campaign(self):
        self.controler(
            "save_campaign",
            lambda: self.client.save_campaign(
                name='Atelier Exemple',
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                steps=[{'variants': [{'subject': 'Vos chantiers de la rentrée', 'text': 'Bonjour {{prenom}},\n\nUn mot sur vos chantiers.\n\n{{unsubscribe_url}}'}]}],
            ),
            lambda: self.client.save_campaign(
                name='Atelier Exemple',
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                steps=[{'variants': [{'subject': 'Vos chantiers de la rentrée', 'text': 'Bonjour {{prenom}},\n\nUn mot sur vos chantiers.\n\n{{unsubscribe_url}}'}]}],
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                from_address='marie@exemple.fr',
                audience_id='aud_3c8f1a5e9d2b47c6a0e4f81b7d5c9e26',
                reply_to='marie@exemple.fr',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.save_campaign()

    def test_get_campaign(self):
        self.controler(
            "get_campaign",
            lambda: self.client.get_campaign(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
            ),
            lambda: self.client.get_campaign(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                offset=0,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.get_campaign()

    def test_preview_campaign(self):
        self.controler(
            "preview_campaign",
            lambda: self.client.preview_campaign(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
            ),
            lambda: self.client.preview_campaign(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                offset=0,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.preview_campaign()

    def test_campaign_action(self):
        self.controler(
            "campaign_action",
            lambda: self.client.campaign_action(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                action='pause',
            ),
            lambda: self.client.campaign_action(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                action='pause',
                starts_at='2026-10-20T09:00:00+02:00',
                confirm=True,
                revision='5d41402abc4b2a76',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.campaign_action()

    def test_campaign_metrics(self):
        self.controler(
            "campaign_metrics",
            lambda: self.client.campaign_metrics(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
            ),
            lambda: self.client.campaign_metrics(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                offset=0,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.campaign_metrics()

    def test_campaign_history(self):
        self.controler(
            "campaign_history",
            lambda: self.client.campaign_history(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
            ),
            lambda: self.client.campaign_history(
                campaign_id='cmp_6b2d9e41c7a84f03b5e1d28a90c4f7e3',
                offset=0,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.campaign_history()

    def test_get_thread(self):
        self.controler(
            "get_thread",
            lambda: self.client.get_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
            ),
            lambda: self.client.get_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
                cursor='eyJhIjoiMjAyNi0xMC0xMyJ9',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.get_thread()

    def test_reply_to_thread(self):
        self.controler(
            "reply_to_thread",
            lambda: self.client.reply_to_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
                text='Bonjour Madame Morel,\n\nPouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?\n\nBien à vous,\nMarie',
            ),
            lambda: self.client.reply_to_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
                text='Bonjour Madame Morel,\n\nPouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?\n\nBien à vous,\nMarie',
                subject='Rendez-vous de jeudi',
                cc=['bureau.etudes@exemple.com'],
                from_address='marie@exemple.fr',
                html='<p>Bonjour Madame Morel,</p><p>Pouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?</p><p>Bien à vous,<br>Marie</p>',
                reply_to='marie@exemple.fr',
                metadata={'dossier': 'rdv-jeudi'},
                requires_approval=True,
                send_after='2026-10-13T09:00:00+02:00',
                idempotency_key='rdv-jeudi-nadia-morel',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.reply_to_thread()

    def test_close_thread(self):
        self.controler(
            "close_thread",
            lambda: self.client.close_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
            ),
            lambda: self.client.close_thread(
                thread_id='thr_0e5a7c2b9f1d48e6a3c7b5d0e2f9a814',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.close_thread()

    def test_get_message(self):
        self.controler(
            "get_message",
            lambda: self.client.get_message(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
            ),
            lambda: self.client.get_message(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.get_message()

    def test_list_drafts(self):
        self.controler(
            "list_drafts",
            lambda: self.client.list_drafts(),
            lambda: self.client.list_drafts(
                inbox_id='inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95',
                cursor='eyJhIjoiMjAyNi0xMC0xMyJ9',
                limit=20,
            ),
        )

    def test_update_draft(self):
        self.controler(
            "update_draft",
            lambda: self.client.update_draft(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
            ),
            lambda: self.client.update_draft(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
                subject='Rendez-vous de jeudi',
                text='Bonjour Madame Morel,\n\nPouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?\n\nBien à vous,\nMarie',
                html='<p>Bonjour Madame Morel,</p><p>Pouvons-nous déplacer notre rendez-vous de jeudi à vendredi, 10 h ?</p><p>Bien à vous,<br>Marie</p>',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.update_draft()

    def test_approve_message(self):
        self.controler(
            "approve_message",
            lambda: self.client.approve_message(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
            ),
            lambda: self.client.approve_message(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
                revision='5d41402abc4b2a76',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.approve_message()

    def test_cancel_message(self):
        self.controler(
            "cancel_message",
            lambda: self.client.cancel_message(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
            ),
            lambda: self.client.cancel_message(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
                reason='Rendez-vous annulé.',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.cancel_message()

    def test_attach_files(self):
        self.controler(
            "attach_files",
            lambda: self.client.attach_files(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
            ),
            lambda: self.client.attach_files(
                message_id='msg_7f2a91c4e8b34d0fa6c25e1b9d3f7a48',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.attach_files()

    def test_remove_attachment(self):
        self.controler(
            "remove_attachment",
            lambda: self.client.remove_attachment(
                attachment_id='att_5e1c9a7b3d2f40618c4e6a0b9d7f2c35',
            ),
            lambda: self.client.remove_attachment(
                attachment_id='att_5e1c9a7b3d2f40618c4e6a0b9d7f2c35',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.remove_attachment()

    def test_get_attachment(self):
        self.controler(
            "get_attachment",
            lambda: self.client.get_attachment(
                attachment_id='att_5e1c9a7b3d2f40618c4e6a0b9d7f2c35',
            ),
            lambda: self.client.get_attachment(
                attachment_id='att_5e1c9a7b3d2f40618c4e6a0b9d7f2c35',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.get_attachment()

    def test_add_suppression(self):
        self.controler(
            "add_suppression",
            lambda: self.client.add_suppression(
                address='nadia.morel@exemple.com',
            ),
            lambda: self.client.add_suppression(
                address='nadia.morel@exemple.com',
                note='A demandé à ne plus être contactée.',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.add_suppression()

    def test_remove_suppression(self):
        self.controler(
            "remove_suppression",
            lambda: self.client.remove_suppression(
                address='nadia.morel@exemple.com',
            ),
            lambda: self.client.remove_suppression(
                address='nadia.morel@exemple.com',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.remove_suppression()

    def test_list_suppressions(self):
        self.controler(
            "list_suppressions",
            lambda: self.client.list_suppressions(),
            lambda: self.client.list_suppressions(
                query='exemple.com',
                cursor='eyJhIjoiMjAyNi0xMC0xMyJ9',
                limit=20,
            ),
        )

    def test_get_settings(self):
        self.controler(
            "get_settings",
            lambda: self.client.get_settings(),
            lambda: self.client.get_settings(),
        )

    def test_update_settings(self):
        self.controler(
            "update_settings",
            lambda: self.client.update_settings(),
            lambda: self.client.update_settings(
                name='Atelier Exemple',
                postal_address='12 rue des Lilas, 69007 Lyon',
                weekdays='8-12,14-18',
                saturday='9-12',
                sunday='closed',
                skip_holidays=True,
                no_send_days=['2026-12-24'],
                require_approval=True,
                spacing_minutes=20,
                dedup_days=60,
            ),
        )

    def test_list_keys(self):
        self.controler(
            "list_keys",
            lambda: self.client.list_keys(),
            lambda: self.client.list_keys(),
        )

    def test_create_key(self):
        self.controler(
            "create_key",
            lambda: self.client.create_key(
                name='Atelier Exemple',
            ),
            lambda: self.client.create_key(
                name='Atelier Exemple',
                permissions=['send', 'read'],
                inbox_ids=['inb_3f9c2a7e5b1d4c8e9a0f6b2d7c4e1a95'],
                daily_cap=50,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.create_key()

    def test_revoke_key(self):
        self.controler(
            "revoke_key",
            lambda: self.client.revoke_key(
                key_id='key_5a0d8e3c9b714f26a1e47c08b3d95f62',
                confirm=True,
            ),
            lambda: self.client.revoke_key(
                key_id='key_5a0d8e3c9b714f26a1e47c08b3d95f62',
                confirm=True,
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.revoke_key()

    def test_set_webhook(self):
        self.controler(
            "set_webhook",
            lambda: self.client.set_webhook(
                url='https://exemple.fr/hooks/subagent',
            ),
            lambda: self.client.set_webhook(
                url='https://exemple.fr/hooks/subagent',
            ),
        )
        with self.assertRaises(TypeError):  # un argument obligatoire manque
            self.client.set_webhook()

    def test_remove_webhook(self):
        self.controler(
            "remove_webhook",
            lambda: self.client.remove_webhook(),
            lambda: self.client.remove_webhook(),
        )

    def test_close_space(self):
        self.controler(
            "close_space",
            lambda: self.client.close_space(),
            lambda: self.client.close_space(
                confirmation_code='482913',
                cancel=False,
            ),
        )

    def test_le_sdk_couvre_tout_le_registre(self):
        testees = {nom[len("test_"):] for nom in dir(self) if nom.startswith("test_")} & set(OPERATIONS)
        self.assertEqual(testees, set(OPERATIONS))


if __name__ == "__main__":
    unittest.main()
