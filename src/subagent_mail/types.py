"""Les objets rendus par les opérations.

Ce sont des dictionnaires (`TypedDict`) : `boite["id"]`. Le serveur ne déclare aucun champ de
sortie comme obligatoire et peut en ajouter : chaque champ est donc facultatif pour un
vérificateur de types, et un champ inconnu ne casse rien.

Généré depuis le registre d'opérations du serveur (clients/generer.py) : ne le modifiez pas.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


# Rendu par create_inbox, update_inbox.
Inbox = TypedDict(
    "Inbox",
    {
        "address": str,  # Adresse e-mail.
        "aliases": List[str],  # Alias d’expédition autorisés ; quota et réception partagés avec la boîte.
        "display_name": str,  # Nom affiché des envois.
        "drafts": int,
        "id": str,  # Identifiant de la boîte (inb_…).
        "next_send_at": Optional[str],  # Prochain départ au plus tôt (ISO 8601).
        "queued": int,
        "quota": Dict[str, Any],  # daily_quota, daily_max, sent_today, remaining_today.
        "send_window": str,  # Créneau d’envoi en clair.
        "shared": bool,  # Boîte du domaine commun, et non d’un domaine de l’espace.
        "status": Literal["active", "suspended", "deleted"],
        "status_changed_at": Optional[str],  # Depuis quand la boîte est dans cet état (ISO 8601) : la date d’une suspension, ou d’une reprise.
        "status_reason": Optional[str],
        "suspension": Optional[Dict[str, Any]],  # Pour une boîte suspendue : review (none, ou requested quand la reprise a été demandée) et requested_at. null sinon.
        "warmup": Dict[str, Any],  # Réchauffage : semaine, palier du jour, paliers, terminé ou non.
    },
    total=False,
)

# Rendu par sign_up.
SignUpResult = TypedDict(
    "SignUpResult",
    {
        "api_key": str,  # Votre clé d’API (sak_…). Affichée une seule fois : Subagent n’en garde qu’une empreinte.
        "code_expires_at": Optional[str],  # Fin de validité du code (ISO 8601).
        "code_sent": bool,  # Un code de vérification est parti à l’humain.
        "human_email": Optional[str],  # E-mail de l’humain, masqué.
        "inbox": Inbox,
        "mcp_url": str,  # Adresse du MCP, à appeler avec l’en-tête Authorization: Bearer <clé>.
        "space_id": str,  # Identifiant de l’espace.
        "status": Literal["unverified", "verified"],  # unverified : la boîte reçoit, n’envoie pas.
        "trial_limits": Dict[str, Any],  # Limites d’essai une fois l’espace vérifié.
    },
    total=False,
)

# Rendu par verify.
VerifyResult = TypedDict(
    "VerifyResult",
    {
        "space_id": str,  # Identifiant de l’espace.
        "trial_limits": Dict[str, Any],  # Limites d’essai des boîtes du domaine commun.
        "verified": bool,  # L’espace est vérifié : l’envoi est ouvert.
        "verified_at": str,  # ISO 8601.
    },
    total=False,
)

# Rendu par attach_human.
AttachHumanResult = TypedDict(
    "AttachHumanResult",
    {
        "code_expires_at": str,  # Fin de validité du code (ISO 8601).
        "code_sent": bool,  # Un code est parti.
        "human_email": str,  # E-mail de l’humain, masqué.
        "replaced": bool,  # L’adresse remplace celle qui était rattachée.
    },
    total=False,
)

# Rendu par inbox_status.
InboxStatusResult = TypedDict(
    "InboxStatusResult",
    {
        "billing": Optional[Dict[str, Any]],  # Où en est le paiement de l’espace : standing (exempt, unpaid, paid), plan, paid_until, subscription_status (none, pending, active, past_due, canceled), last_payment (none, pending, paid, failed). null : rien à payer sur ce serveur.
        "human_email": Optional[str],  # L’adresse de l’humain de l’espace, masquée (m•••@societe.fr). null : aucun humain rattaché.
        "inboxes": List[Inbox],
        "key": Dict[str, Any],
        "now": str,  # Instant de cet état (ISO 8601, heure de Paris).
        "require_approval": bool,  # Tout envoi de l’espace attend une validation humaine.
        "send_window": str,  # Créneau d’envoi en clair.
        "tenant": Dict[str, Any],
        "trial": Optional[Dict[str, Any]],  # Limites d’essai des boîtes du domaine commun : limit, used, window, next_limit, next_at. null : aucune.
        "verified": bool,  # L’espace est vérifié : il envoie. Sinon ses boîtes reçoivent seulement (verify).
    },
    total=False,
)

# Rendu par workspace_snapshot.
WorkspaceSnapshotResult = TypedDict(
    "WorkspaceSnapshotResult",
    {
        "access_key": str,  # Empreinte opaque de l’accès.
        "refreshed_at": str,  # Dernière préparation.
        "revision": str,  # Révision opaque.
        "unavailable": Dict[str, Any],
        "unchanged": bool,
        "views": Dict[str, Any],
    },
    total=False,
)

# Rendu par activity_report.
ActivityReportResult = TypedDict(
    "ActivityReportResult",
    {
        "billing": Optional[Dict[str, Any]],  # Où en est le paiement de l’espace : standing (exempt, unpaid, paid), plan, paid_until, subscription_status, last_payment. null : rien à payer sur ce serveur.
        "by_day": List[Dict[str, Any]],  # Un objet par jour de la période, dans l’ordre : date, sent, quota (0 un jour sans envoi), replies, bounces, unsubscribes, complaints.
        "inboxes": List[Inbox],
        "key": Dict[str, Any],  # La clé qui lit : name, permissions.
        "now": str,  # Instant du relevé (ISO 8601, heure de Paris).
        "pending": Dict[str, Any],  # Ce qui attend une décision. drafts : count et items (les cinq brouillons les plus récents : id, inbox_id, to, to_name, subject, is_reply, created_at). replies : count et items (les cinq fils les plus récents dont le dernier message est un e-mail reçu sans réponse), ou null sans la permission read. domains : les domaines non vérifiés (id, domain, status, required_missing), ou null sans la permission read ou manage_inboxes. suspended_inboxes : id, address, status_reason, suspended_at.
        "period": Dict[str, Any],  # kind (today ou week), from et to : jours de Paris (AAAA-MM-JJ), compris.
        "require_approval": bool,  # Tout envoi de l’espace attend une validation humaine.
        "send_window": str,  # Créneau d’envoi en clair.
        "tenant": Dict[str, Any],  # L’espace : id, name.
        "totals": Dict[str, Any],  # Sur la période : sent (envois comptés au quota), quota (somme des quotas du jour), queued (en file à l’instant), replies (réponses reçues dans un fil, hors réponses automatiques), bounces, unsubscribes, complaints.
        "verified": bool,  # L’espace est vérifié : il envoie.
    },
    total=False,
)

# Rendu par list_events.
ListEventsResult = TypedDict(
    "ListEventsResult",
    {
        "day": Optional[str],  # Le jour lu (AAAA-MM-JJ), ou null pour l’historique d’un objet.
        "events": List[Dict[str, Any]],  # Du plus récent au plus ancien : id, at, kind, text (phrase nominale en français, sans sujet), actor (kind agent, human ou service ; name ; you), et les objets touchés (inbox_id, thread_id, message_id, campaign_id, audience_id, contact, domain) quand il y en a.
        "next_cursor": Optional[str],
    },
    total=False,
)

# Rendu par billing_status.
BillingStatusResult = TypedDict(
    "BillingStatusResult",
    {
        "invoices": List[Dict[str, Any]],  # Les factures, de la plus récente à la plus ancienne : number, issued_on, amount_cents, amount, url.
        "last_payment": Literal["none", "pending", "paid", "failed"],  # L’issue du dernier paiement ouvert par subscribe.
        "period": Optional[Dict[str, Any]],  # La période payée : start, until (ISO 8601).
        "plan": Optional[Dict[str, Any]],  # Le forfait en cours : code, price_cents, price, inboxes, monthly_emails.
        "plans": List[Dict[str, Any]],  # Les forfaits en vente.
        "standing": Literal["exempt", "unpaid", "paid"],  # exempt : aucun forfait ne s’applique à cet espace ; unpaid : aucun forfait en cours ; paid : forfait en cours.
        "subscription": Dict[str, Any],  # Le prélèvement mensuel : status (none, pending, active, past_due, canceled), renews, next_charge_on (date du prochain prélèvement, ou null), ends_at (fin du forfait quand rien ne le renouvelle, ou null).
        "usage": Dict[str, Any],  # inboxes et inboxes_max ; emails (partis depuis le début du mois en cours de la période, emails_since) et emails_max ; emails_reset_at : quand le volume repart.
    },
    total=False,
)

# Rendu par subscribe.
SubscribeResult = TypedDict(
    "SubscribeResult",
    {
        "expires_at": Optional[str],  # Fin de validité du lien (ISO 8601).
        "human": Optional[str],  # L’adresse masquée de l’humain de l’espace.
        "payment_url": Optional[str],  # Le lien à donner à votre humain.
        "plan": Optional[Dict[str, Any]],  # Le forfait proposé, ou le forfait en cours.
        "plans": List[Dict[str, Any]],  # Les forfaits en vente.
        "status": Literal["link_ready", "subscribed", "exempt"],  # link_ready : le lien est prêt ; subscribed : un forfait est déjà en cours et prélevé ; exempt : aucun forfait ne s’applique à cet espace.
    },
    total=False,
)

# Rendu par cancel_subscription.
CancelSubscriptionResult = TypedDict(
    "CancelSubscriptionResult",
    {
        "paid_until": Optional[str],  # Fin du mois payé (ISO 8601) : l’envoi continue jusque-là.
        "plan": Optional[Dict[str, Any]],  # Le forfait qui s’arrêtera.
        "status": Literal["canceled", "already_canceled"],
    },
    total=False,
)

# Rendu par list_inboxes.
ListInboxesResult = TypedDict(
    "ListInboxesResult",
    {
        "items": List[Inbox],
        "next_cursor": Optional[str],  # À repasser en cursor pour la page suivante ; null à la dernière page.
    },
    total=False,
)

# Rendu par delete_inbox.
DeleteInboxResult = TypedDict(
    "DeleteInboxResult",
    {
        "cancelled_messages": int,
        "deleted": str,  # Identifiant de la boîte supprimée.
        "remote_account_removed": bool,  # Compte de messagerie supprimé.
    },
    total=False,
)

# Rendu par request_inbox_review.
RequestInboxReviewResult = TypedDict(
    "RequestInboxReviewResult",
    {
        "already_requested": bool,  # true : elle l’était déjà, rien n’a été ajouté.
        "inbox": Inbox,
        "requested": bool,  # true : la reprise de cette boîte est demandée.
        "requested_at": str,  # Date de la demande (ISO 8601).
    },
    total=False,
)

DnsRecord = TypedDict(
    "DnsRecord",
    {
        "label": str,  # Le rôle en clair.
        "name": str,  # Nom complet de l’enregistrement.
        "note": Optional[str],
        "required": bool,  # Exigé pour que le domaine soit vérifié (DMARC est seulement conseillé).
        "role": Literal["ownership", "dkim", "spf", "mx", "dmarc"],  # Ce que l’enregistrement prouve ou autorise.
        "seen": Optional[str],  # La valeur vue dans le DNS quand elle diffère.
        "state": Optional[Literal["found", "missing", "different"]],  # État au dernier contrôle : trouvé, absent, ou valeur différente.
        "type": Literal["TXT", "MX"],
        "value": str,  # Valeur exacte à publier.
    },
    total=False,
)

# Rendu par add_domain, verify_domain.
Domain = TypedDict(
    "Domain",
    {
        "domain": str,  # Nom de domaine.
        "id": str,  # Identifiant du domaine (dom_…).
        "last_checked_at": Optional[str],
        "records": List[DnsRecord],
        "status": Literal["pending", "verified", "suspended"],  # pending : DNS à publier ; verified : on peut y créer des boîtes ; suspended : le DNS a disparu, ses boîtes n’envoient plus.
        "status_reason": Optional[str],
        "verified_at": Optional[str],
    },
    total=False,
)

# Rendu par list_domains.
ListDomainsResult = TypedDict(
    "ListDomainsResult",
    {
        "items": List[Domain],
    },
    total=False,
)

# Rendu par domain_quality.
DomainQualityResult = TypedDict(
    "DomainQualityResult",
    {
        "collected_at": str,  # Instant de consultation.
        "dns": Dict[str, Any],
        "domain": str,  # Domaine de cet espace.
        "history_excluded": bool,
        "inboxes": List[Dict[str, Any]],
        "inboxes_truncated": bool,
        "notice": str,  # Portée des indicateurs.
        "period": Dict[str, Any],
        "protections": Dict[str, Any],
        "quality": bool,
        "rates": Dict[str, Any],
        "scope_limited": bool,
        "state": Literal["blocked", "configuration_required", "attention", "no_data", "limited_data", "no_alert"],
        "tests_included": bool,
        "volume": Dict[str, Any],
    },
    total=False,
)

# Rendu par remove_domain.
RemoveDomainResult = TypedDict(
    "RemoveDomainResult",
    {
        "remote_domain_removed": bool,  # Le domaine a été retiré du serveur de messagerie.
        "removed": str,  # Le domaine retiré.
    },
    total=False,
)

# Rendu par update_draft, cancel_message.
Message = TypedDict(
    "Message",
    {
        "attachments": List[Dict[str, Any]],  # Pièces jointes (voir get_attachment).
        "auto_reply": bool,  # Réponse automatique (absence…).
        "cc": List[str],  # Copies (sortant) ; autres destinataires (reçu).
        "created_at": str,  # ISO 8601.
        "direction": Literal["outbound", "inbound"],
        "from": str,  # Expéditeur.
        "has_html": bool,  # Le message a une version HTML.
        "id": str,  # Identifiant du message (msg_…).
        "inbox_id": str,  # Boîte du message.
        "received_at": Optional[str],
        "reply_to": Optional[str],  # Adresse de réponse, si elle diffère de la boîte.
        "revision": str,  # Version du message : change à chaque modification (voir approve_message).
        "sent_at": Optional[str],
        "status": Literal["draft", "queued", "sending", "sent", "delivered", "bounced", "failed", "rejected", "cancelled", "received"],
        "status_code": Optional[str],  # Code stable d’un refus ou d’un échec.
        "subject": str,  # Sujet.
        "text": str,  # Texte (lecture d’un message ou d’un fil).
        "thread_id": str,  # Fil du message.
        "to": str,  # Destinataire.
    },
    total=False,
)

Thread = TypedDict(
    "Thread",
    {
        "archived": bool,  # Conversation archivée.
        "counterpart": str,  # Adresse du correspondant.
        "counterpart_name": Optional[str],
        "id": str,  # Identifiant du fil (thr_…).
        "inbox_id": str,  # Boîte du fil.
        "labels": List[str],
        "last_inbound_at": Optional[str],
        "last_message_at": str,  # ISO 8601.
        "last_outbound_at": Optional[str],
        "message_count": int,
        "origin": Literal["outbound", "inbound"],
        "status": Literal["open", "replied", "bounced", "unsubscribed", "closed"],
        "subject": str,  # Sujet.
        "unread": bool,  # Au moins un message reçu depuis la dernière lecture.
    },
    total=False,
)

# Rendu par send_email.
SendEmailResult = TypedDict(
    "SendEmailResult",
    {
        "estimated_send_at": Optional[str],  # Départ au plus tôt (estimation : créneau, étalement, quota).
        "inbox": Inbox,
        "message": Message,
        "replayed": bool,  # true : même clé d’idempotence et même contenu, rien de nouveau n’a été créé.
        "thread": Thread,
    },
    total=False,
)

# Rendu par list_threads.
ListThreadsResult = TypedDict(
    "ListThreadsResult",
    {
        "inboxes": List[Dict[str, Any]],  # Boîtes accessibles : id, address, aliases, status.
        "items": List[Thread],
        "next_cursor": Optional[str],  # À repasser en cursor pour la page suivante ; null à la dernière page.
    },
    total=False,
)

# Rendu par classify_thread.
ClassifyThreadResult = TypedDict(
    "ClassifyThreadResult",
    {
        "thread": Thread,
    },
    total=False,
)

# Rendu par inspect_domain.
InspectDomainResult = TypedDict(
    "InspectDomainResult",
    {
        "current_mx": List[Dict[str, Any]],
        "current_spf": List[str],
        "domain": str,  # Domaine contrôlé.
        "receives_elsewhere": bool,  # Des MX conduisent à un autre service.
        "suggested_domain": str,  # Domaine proposé pour Subagent.
    },
    total=False,
)

Audience = TypedDict(
    "Audience",
    {
        "id": str,  # Audience (aud_…).
        "name": str,  # Nom de l’audience.
    },
    total=False,
)

Contact = TypedDict(
    "Contact",
    {
        "audiences": List[Audience],
        "created_at": str,  # Création de la fiche.
        "email": str,  # Adresse unique dans l’espace.
        "fields": Dict[str, Any],
        "labels": List[str],
        "name": str,  # Nom du contact.
        "suppression": Optional[Dict[str, Any]],  # Blocage effectif : kind (adresse/domaine), value, reason, scope (global ou propre à l’espace), source et created_at. Null ne signifie pas consentement commercial.
        "updated_at": str,  # Dernière édition globale.
    },
    total=False,
)

# Rendu par list_contacts.
ListContactsResult = TypedDict(
    "ListContactsResult",
    {
        "items": List[Contact],
        "next_offset": Optional[int],
        "total": int,
    },
    total=False,
)

# Rendu par get_contact.
GetContactResult = TypedDict(
    "GetContactResult",
    {
        "contact": Contact,
    },
    total=False,
)

# Rendu par list_audiences.
ListAudiencesResult = TypedDict(
    "ListAudiencesResult",
    {
        "items": List[Dict[str, Any]],  # Les audiences de l’espace, 200 au plus.
    },
    total=False,
)

# Rendu par list_campaign_templates.
ListCampaignTemplatesResult = TypedDict(
    "ListCampaignTemplatesResult",
    {
        "templates": List[Dict[str, Any]],  # Les modèles : id, name, subject, text_body, html_body, source, previous (la version qu’une correction a remplacée), updated_at.
    },
    total=False,
)

# Rendu par save_campaign_template.
SaveCampaignTemplateResult = TypedDict(
    "SaveCampaignTemplateResult",
    {
        "template": Dict[str, Any],  # Le modèle enregistré : id, name, subject, text_body, html_body, previous, updated_at.
    },
    total=False,
)

# Rendu par save_audience.
SaveAudienceResult = TypedDict(
    "SaveAudienceResult",
    {
        "audience": Dict[str, Any],  # Une audience : id (aud_…), name, source (subagent, ou l’outil d’où elle est reprise), external_id, contacts (leur nombre, dans list_audiences), created_at, updated_at.
    },
    total=False,
)

# Rendu par get_audience.
GetAudienceResult = TypedDict(
    "GetAudienceResult",
    {
        "audience": Dict[str, Any],  # Une audience : id (aud_…), name, source (subagent, ou l’outil d’où elle est reprise), external_id, contacts (leur nombre, dans list_audiences), created_at, updated_at.
        "items": List[Dict[str, Any]],  # Les contacts de la page, 200 au plus : email, name, fields, labels, created_at.
        "next_offset": Optional[int],  # Le rang de la page suivante (offset), ou null.
    },
    total=False,
)

# Rendu par import_contacts.
ImportContactsResult = TypedDict(
    "ImportContactsResult",
    {
        "updated": int,  # Le nombre de contacts ajoutés ou actualisés.
    },
    total=False,
)

# Rendu par remove_audience_contact.
RemoveAudienceContactResult = TypedDict(
    "RemoveAudienceContactResult",
    {
        "removed": bool,  # Le contact est retiré de l’audience.
    },
    total=False,
)

# Rendu par list_campaigns.
ListCampaignsResult = TypedDict(
    "ListCampaignsResult",
    {
        "items": List[Dict[str, Any]],  # Les campagnes de la page, 100 au plus, les plus récentes d’abord.
        "next_offset": Optional[int],  # Le rang de la page suivante (offset), ou null.
    },
    total=False,
)

# Rendu par save_campaign.
SaveCampaignResult = TypedDict(
    "SaveCampaignResult",
    {
        "campaign": Dict[str, Any],  # Une campagne : id (cmp_…), name, status (draft, scheduled, running, paused, completed, stopped), archived, inbox_id, from_address, audience_id, reply_to, steps (de 1 à 4 étapes : delay_days et variants, chacune avec subject, text, html), starts_at, status_reason, source, previous (dans get_campaign : les étapes qu’une correction a remplacées, avec l’auteur et l’heure de la correction), created_at, updated_at.
    },
    total=False,
)

# Rendu par get_campaign.
GetCampaignResult = TypedDict(
    "GetCampaignResult",
    {
        "campaign": Dict[str, Any],  # Une campagne : id (cmp_…), name, status (draft, scheduled, running, paused, completed, stopped), archived, inbox_id, from_address, audience_id, reply_to, steps (de 1 à 4 étapes : delay_days et variants, chacune avec subject, text, html), starts_at, status_reason, source, previous (dans get_campaign : les étapes qu’une correction a remplacées, avec l’auteur et l’heure de la correction), created_at, updated_at.
        "history": Dict[str, Any],  # La première page de l’historique repris, comme campaign_history la rend.
        "metrics": Dict[str, Any],  # Les performances, comme campaign_metrics les rend.
    },
    total=False,
)

# Rendu par preview_campaign.
PreviewCampaignResult = TypedDict(
    "PreviewCampaignResult",
    {
        "blocked": List[Dict[str, Any]],  # Les destinataires bloquants et la raison de chacun (champ vide, blocage, doublon).
        "blocked_count": int,  # Le nombre de destinataires bloquants.
        "campaign": Dict[str, Any],  # Une campagne : id (cmp_…), name, status (draft, scheduled, running, paused, completed, stopped), archived, inbox_id, from_address, audience_id, reply_to, steps (de 1 à 4 étapes : delay_days et variants, chacune avec subject, text, html), starts_at, status_reason, source, previous (dans get_campaign : les étapes qu’une correction a remplacées, avec l’auteur et l’heure de la correction), created_at, updated_at.
        "deferred": List[Dict[str, Any]],  # Les départs différés et leur raison.
        "deferred_count": int,  # Le nombre de destinataires dont le départ sera différé.
        "notice": str,  # Ce qu’il faut relire avant de lancer.
        "previews": List[Dict[str, Any]],  # Un aperçu personnalisé de chaque étape et variante.
        "ready": bool,  # Rien ne bloque le lancement.
        "recipients": int,  # Le nombre de destinataires.
        "revision": str,  # L’empreinte de ce qui a été relu : à donner à campaign_action pour start.
    },
    total=False,
)

# Rendu par campaign_metrics.
CampaignMetricsResult = TypedDict(
    "CampaignMetricsResult",
    {
        "campaign": Dict[str, Any],  # Une campagne : id (cmp_…), name, status (draft, scheduled, running, paused, completed, stopped), archived, inbox_id, from_address, audience_id, reply_to, steps (de 1 à 4 étapes : delay_days et variants, chacune avec subject, text, html), starts_at, status_reason, source, previous (dans get_campaign : les étapes qu’une correction a remplacées, avec l’auteur et l’heure de la correction), created_at, updated_at.
        "metrics": Dict[str, Any],  # live (les envois de Subagent : envoyés, remis, rebonds, réponses, erreurs, en file), history (ouvertures et clics repris, à part), recipients, variants (par étape et variante), note.
    },
    total=False,
)

# Rendu par campaign_history.
CampaignHistoryResult = TypedDict(
    "CampaignHistoryResult",
    {
        "items": List[Dict[str, Any]],  # Les envois repris, 100 au plus : email, status, sent_at, delivery, opened, clicked.
        "next_offset": Optional[int],  # Le rang de la page suivante (offset), ou null.
    },
    total=False,
)

# Rendu par get_thread.
GetThreadResult = TypedDict(
    "GetThreadResult",
    {
        "messages": List[Message],
        "next_cursor": Optional[str],  # Curseur de la suite du fil, s’il reste des messages.
        "thread": Thread,
        "truncated": bool,  # true : des corps ont été tronqués (200 Ko au plus par appel).
    },
    total=False,
)

# Rendu par close_thread.
CloseThreadResult = TypedDict(
    "CloseThreadResult",
    {
        "closed": bool,  # true : le fil vient d’être clos ; false : il l’était déjà.
        "thread": Thread,
    },
    total=False,
)

# Rendu par get_message.
GetMessageResult = TypedDict(
    "GetMessageResult",
    {
        "events": List[Dict[str, Any]],
        "message": Message,
        "waiting": Optional[Dict[str, Any]],  # Pour un message en file : reason (pourquoi il n’est pas encore parti) et earliest_send_at (départ au plus tôt, ISO 8601, ou null). null : le message n’est pas en file.
    },
    total=False,
)

# Rendu par list_drafts.
ListDraftsResult = TypedDict(
    "ListDraftsResult",
    {
        "items": List[Message],
        "key": Dict[str, Any],  # La clé qui lit : name, permissions. approve ouvre la validation (approve_message) ; send ou approve, l’annulation (cancel_message).
        "next_cursor": Optional[str],  # À repasser en cursor pour la page suivante ; null à la dernière page.
    },
    total=False,
)

# Rendu par approve_message.
ApproveMessageResult = TypedDict(
    "ApproveMessageResult",
    {
        "attachments": List[Dict[str, Any]],  # Pièces jointes (voir get_attachment).
        "auto_reply": bool,  # Réponse automatique (absence…).
        "cc": List[str],  # Copies (sortant) ; autres destinataires (reçu).
        "created_at": str,  # ISO 8601.
        "direction": Literal["outbound", "inbound"],
        "estimated_send_at": Optional[str],  # Départ au plus tôt du message validé (estimation : créneau, étalement, quota).
        "from": str,  # Expéditeur.
        "has_html": bool,  # Le message a une version HTML.
        "id": str,  # Identifiant du message (msg_…).
        "inbox_id": str,  # Boîte du message.
        "received_at": Optional[str],
        "reply_to": Optional[str],  # Adresse de réponse, si elle diffère de la boîte.
        "revision": str,  # Version du message : change à chaque modification (voir approve_message).
        "sent_at": Optional[str],
        "status": Literal["draft", "queued", "sending", "sent", "delivered", "bounced", "failed", "rejected", "cancelled", "received"],
        "status_code": Optional[str],  # Code stable d’un refus ou d’un échec.
        "subject": str,  # Sujet.
        "text": str,  # Texte (lecture d’un message ou d’un fil).
        "thread_id": str,  # Fil du message.
        "to": str,  # Destinataire.
    },
    total=False,
)

# Rendu par attach_files.
AttachFilesResult = TypedDict(
    "AttachFilesResult",
    {
        "attachments": List[Dict[str, Any]],  # Pièces déjà jointes.
        "expires_at": str,  # Fin de validité (ISO 8601).
        "max_bytes": int,  # Octets permis en tout.
        "message_id": str,  # Le brouillon.
        "upload_url": str,  # Le lien de dépôt.
    },
    total=False,
)

# Rendu par remove_attachment.
RemoveAttachmentResult = TypedDict(
    "RemoveAttachmentResult",
    {
        "attachments": List[Dict[str, Any]],  # Pièces qui restent.
        "removed": Dict[str, Any],
    },
    total=False,
)

# Rendu par get_attachment.
GetAttachmentResult = TypedDict(
    "GetAttachmentResult",
    {
        "attachment": Dict[str, Any],
        "download_url": Optional[str],  # null : contenu non gardé (stored = false).
        "expires_at": Optional[str],
        "text": Optional[str],  # Texte d’une petite pièce textuelle.
        "untrusted": bool,  # Pièce reçue d’un tiers.
    },
    total=False,
)

# Rendu par add_suppression.
AddSuppressionResult = TypedDict(
    "AddSuppressionResult",
    {
        "cancelled_messages": int,
        "kind": Literal["address", "domain"],
        "new": bool,  # Entrée nouvelle.
        "value": str,  # Ce qui est bloqué.
    },
    total=False,
)

# Rendu par remove_suppression.
RemoveSuppressionResult = TypedDict(
    "RemoveSuppressionResult",
    {
        "removed": str,  # Ce qui n’est plus bloqué.
    },
    total=False,
)

Suppression = TypedDict(
    "Suppression",
    {
        "created_at": str,  # ISO 8601.
        "kind": str,  # address ou domain.
        "reason": Literal["unsubscribe", "hard_bounce", "complaint", "manual"],
        "scope": Literal["tenant", "global"],
        "source": Optional[str],  # D’où vient l’entrée : qui l’a ajoutée et sa note, ou la voie de la désinscription. null pour une adresse morte commune.
        "value": str,  # Adresse ou domaine.
    },
    total=False,
)

# Rendu par list_suppressions.
ListSuppressionsResult = TypedDict(
    "ListSuppressionsResult",
    {
        "items": List[Suppression],
        "next_cursor": Optional[str],  # À repasser en cursor pour la page suivante ; null à la dernière page.
    },
    total=False,
)

# Rendu par get_settings.
GetSettingsResult = TypedDict(
    "GetSettingsResult",
    {
        "changed": List[str],  # Après update_settings : les réglages modifiés.
        "dedup_days": int,  # Jours pendant lesquels une boîte n’écrit pas deux premiers messages au même destinataire.
        "limits": Dict[str, Any],  # Ce que le service fixe : daily_max (quota d’une boîte par jour) et warmup_steps (paliers de la montée progressive).
        "postal_address": str,  # Adresse postale écrite en pied des premiers messages.
        "require_approval": bool,  # Tout envoi de l’espace attend une validation humaine.
        "send_window": Dict[str, Any],  # Le créneau d’envoi : text (en clair), weekdays (plages du lundi au vendredi si elles sont les mêmes, sinon null), saturday, sunday, days (les sept jours, lundi d’abord), skip_holidays, no_send_days.
        "space": Dict[str, Any],  # id, name, verified.
        "spacing_minutes": int,  # Minutes au moins entre deux envois d’une boîte.
        "webhook": Optional[Dict[str, Any]],  # Le webhook de l’espace : url (entière pour l’humain, son hôte seul pour un agent) et set_at. null : aucun.
    },
    total=False,
)

Key = TypedDict(
    "Key",
    {
        "created_at": str,  # ISO 8601.
        "current": bool,  # true : c’est l’accès qui appelle.
        "daily_cap": Optional[int],  # Plafond de messages créés par jour, s’il y en a un.
        "human_email": Optional[str],  # Pour un assistant branché : l’adresse de son humain, masquée.
        "id": str,  # Identifiant de l’accès (key_…), à passer à revoke_key.
        "inboxes": Any,  # « all » : toutes les boîtes de l’espace ; sinon la liste des adresses ouvertes à cet accès.
        "kind": Literal["key", "connection"],  # key : la clé d’un agent ; connection : l’assistant branché d’un humain.
        "last_used_at": Optional[str],
        "name": str,  # Nom de l’accès.
        "permissions": List[str],
        "prefix": Optional[str],  # Début de la clé, pour la reconnaître. null pour un assistant branché.
    },
    total=False,
)

# Rendu par list_keys.
ListKeysResult = TypedDict(
    "ListKeysResult",
    {
        "items": List[Key],
    },
    total=False,
)

# Rendu par create_key.
CreateKeyResult = TypedDict(
    "CreateKeyResult",
    {
        "api_key": str,  # La clé (sak_…), affichée cette seule fois.
        "key": Key,
        "mcp_url": str,  # L’adresse MCP où l’agent présente sa clé.
    },
    total=False,
)

# Rendu par revoke_key.
RevokeKeyResult = TypedDict(
    "RevokeKeyResult",
    {
        "kind": Literal["key", "connection"],
        "name": str,  # Son nom.
        "revoked": str,  # Identifiant de l’accès retiré.
    },
    total=False,
)

# Rendu par set_webhook.
SetWebhookResult = TypedDict(
    "SetWebhookResult",
    {
        "events": List[str],  # Les événements signalés.
        "replaced": bool,  # true : une adresse était déjà déclarée, elle est remplacée.
        "secret": str,  # Le secret de signature (whsec_…), affiché cette seule fois.
        "url": str,  # L’adresse déclarée.
    },
    total=False,
)

# Rendu par remove_webhook.
RemoveWebhookResult = TypedDict(
    "RemoveWebhookResult",
    {
        "removed": Optional[str],  # L’adresse retirée ; null s’il n’y en avait pas.
    },
    total=False,
)

# Rendu par close_space.
CloseSpaceResult = TypedDict(
    "CloseSpaceResult",
    {
        "cancelled": bool,  # true : une clôture confirmée vient d’être annulée.
        "closes_at": Optional[str],  # Date de l’effacement (ISO 8601), une fois la clôture confirmée.
        "code_sent": bool,  # true : un code de clôture vient de partir à l’humain de l’espace.
        "expires_at": Optional[str],  # Fin de validité du code (ISO 8601).
        "human_email": Optional[str],  # L’adresse où le code est parti, masquée.
        "removes": Dict[str, Any],  # Ce que la clôture emporte : inboxes, domains, subscription (un prélèvement à arrêter), invoices_kept.
        "scheduled": bool,  # true : la clôture est confirmée, l’espace sera effacé à closes_at.
    },
    total=False,
)

# save_contact rend le même objet que get_contact.
SaveContactResult = GetContactResult

# set_contact_audiences rend le même objet que get_contact.
SetContactAudiencesResult = GetContactResult

# campaign_action rend le même objet que save_campaign.
CampaignActionResult = SaveCampaignResult

# reply_to_thread rend le même objet que send_email.
ReplyToThreadResult = SendEmailResult

# update_settings rend le même objet que get_settings.
UpdateSettingsResult = GetSettingsResult

__all__ = [
    "Inbox",
    "SignUpResult",
    "VerifyResult",
    "AttachHumanResult",
    "InboxStatusResult",
    "WorkspaceSnapshotResult",
    "ActivityReportResult",
    "ListEventsResult",
    "BillingStatusResult",
    "SubscribeResult",
    "CancelSubscriptionResult",
    "ListInboxesResult",
    "DeleteInboxResult",
    "RequestInboxReviewResult",
    "DnsRecord",
    "Domain",
    "ListDomainsResult",
    "DomainQualityResult",
    "RemoveDomainResult",
    "Message",
    "Thread",
    "SendEmailResult",
    "ListThreadsResult",
    "ClassifyThreadResult",
    "InspectDomainResult",
    "Audience",
    "Contact",
    "ListContactsResult",
    "GetContactResult",
    "ListAudiencesResult",
    "ListCampaignTemplatesResult",
    "SaveCampaignTemplateResult",
    "SaveAudienceResult",
    "GetAudienceResult",
    "ImportContactsResult",
    "RemoveAudienceContactResult",
    "ListCampaignsResult",
    "SaveCampaignResult",
    "GetCampaignResult",
    "PreviewCampaignResult",
    "CampaignMetricsResult",
    "CampaignHistoryResult",
    "GetThreadResult",
    "CloseThreadResult",
    "GetMessageResult",
    "ListDraftsResult",
    "ApproveMessageResult",
    "AttachFilesResult",
    "RemoveAttachmentResult",
    "GetAttachmentResult",
    "AddSuppressionResult",
    "RemoveSuppressionResult",
    "Suppression",
    "ListSuppressionsResult",
    "GetSettingsResult",
    "Key",
    "ListKeysResult",
    "CreateKeyResult",
    "RevokeKeyResult",
    "SetWebhookResult",
    "RemoveWebhookResult",
    "CloseSpaceResult",
    "SaveContactResult",
    "SetContactAudiencesResult",
    "CampaignActionResult",
    "ReplyToThreadResult",
    "UpdateSettingsResult",
]
