# subagent-python

Le SDK Python de **Subagent Mail** : des boîtes mail pour agents IA. Votre agent crée sa boîte, écrit, lit ses fils et répond avec sa propre adresse. Le serveur applique les règles d'envoi : montée progressive, créneaux, validation humaine, désinscription.

- **Une méthode par opération du serveur** (64), mêmes noms et mêmes arguments que les outils du MCP.
- **Aucune dépendance** : bibliothèque standard seulement, Python 3.9 ou plus.
- **Typé** : arguments et résultats sont tirés des schémas du serveur.
- **Généré** depuis le registre d'opérations du serveur, jamais écrit à la main.

## Installer

```sh
pip install git+https://github.com/subagent-fr/subagent-python
```

## Démarrer

### 1. Une clé

Sans clé, une seule opération est ouverte : `sign_up`. Elle rend une clé, affichée une seule fois, et une boîte sur `subagentmail.fr`. Votre humain reçoit un code à 6 chiffres par e-mail ; `verify` ouvre l'envoi.

```python
from subagent_mail import Subagent

client = Subagent()  # lit SUBAGENT_KEY ; sans clé, seule sign_up est ouverte

inscription = client.sign_up(username="atelier-exemple", human_email="marie@exemple.fr")
print(inscription["api_key"])           # affichée une seule fois : rangez-la
print(inscription["inbox"]["address"])  # atelier-exemple@subagentmail.fr

client.verify(otp_code="482913")        # le code reçu par votre humain
```

Vous avez déjà une clé ? Rangez-la hors du code, le client la lit seul :

```sh
export SUBAGENT_KEY="sak_…"
```

### 2. Où en est la boîte

`inbox_status` est le point de départ de toute session : l'espace, les permissions de la clé, le créneau d'envoi, et pour chaque boîte son quota du jour.

```python
etat = client.inbox_status()
boite = etat["inboxes"][0]
print(boite["address"], boite["quota"]["remaining_today"])
```

### 3. Un premier envoi

Un envoi de test ne part qu'à l'humain de l'espace ou à une autre de ses boîtes : remplacez l'adresse par la vôtre.

```python
envoi = client.send_email(
    inbox_id=boite["id"],
    to="marie@exemple.fr",
    subject="Premier message",
    text="Bonjour Marie,\n\nCeci est mon premier message.\n",
    test=True,                            # à soi-même seulement
    requires_approval=True,               # reste en brouillon jusqu'à la validation d'un humain
    idempotency_key="premier-message-1",  # rejouer cet appel ne crée pas de doublon
)
print(envoi["message"]["status"])  # draft
```

Sans `requires_approval`, le message entre en file et part dans le créneau d'envoi, selon le quota du jour de la boîte. `estimated_send_at` donne l'heure de départ au plus tôt. Un message en file n'est pas une erreur : ne le renvoyez pas.

## Les opérations

| Famille | Opérations |
| --- | --- |
| Inscription | `sign_up`, `verify`, `attach_human` |
| Boîtes | `inbox_status`, `activity_report`, `list_inboxes`, `create_inbox`, `update_inbox`, `delete_inbox`, `request_inbox_review` |
| Domaines | `inspect_domain`, `add_domain`, `verify_domain`, `list_domains`, `domain_quality`, `remove_domain` |
| Envoi | `send_email`, `reply_to_thread` |
| Fils | `list_threads`, `get_thread`, `classify_thread`, `close_thread`, `get_message` |
| Brouillons | `list_drafts`, `update_draft`, `approve_message`, `cancel_message` |
| Pièces jointes | `attach_files`, `remove_attachment`, `get_attachment` |
| Liste de blocage | `add_suppression`, `remove_suppression`, `list_suppressions` |
| Contacts et audiences | `list_contacts`, `get_contact`, `save_contact`, `set_contact_audiences`, `list_audiences`, `get_audience`, `save_audience`, `import_contacts`, `remove_audience_contact` |
| Campagnes | `list_campaigns`, `get_campaign`, `save_campaign`, `preview_campaign`, `campaign_action`, `campaign_metrics`, `campaign_history`, `list_campaign_templates`, `save_campaign_template` |
| Main courante | `list_events`, `workspace_snapshot` |
| Forfait | `billing_status`, `subscribe`, `cancel_subscription` |
| Espace et accès | `get_settings`, `update_settings`, `list_keys`, `create_key`, `revoke_key`, `set_webhook`, `remove_webhook`, `close_space` |

Arguments, résultats et un exemple par méthode : [`reference.md`](reference.md). Sur le site : [documentation](https://subagent.fr/docs) · [`openapi.json`](https://api.subagent.fr/openapi.json) · [`llms.txt`](https://api.subagent.fr/llms.txt).

Les résultats sont des dictionnaires typés (`TypedDict`) : `envoi["message"]["id"]`. Le serveur peut ajouter des champs : un champ inconnu ne casse rien.

## Quand le serveur refuse

Un refus n'est pas une panne. Il lève `SubagentError`, qui porte un `code` stable, un `message` en français et une piste (`hint`) qui dit quoi faire. La piste se suit, elle ne se contourne pas.

```python
from subagent_mail import SubagentError

try:
    client.approve_message(message_id=envoi["message"]["id"])
except SubagentError as refus:
    print(refus.code)     # forbidden : la clé d'un agent ne porte pas approve
    print(refus.message)  # la phrase du serveur, en français
    print(refus.hint)     # ce qu'il faut faire
    print(refus.status)   # 403
```

Un agent ne valide jamais son propre brouillon : `approve_message` demande la permission `approve`, que la clé rendue par `sign_up` ne porte pas.

Les refus les plus courants :

| `code` | HTTP | Ce qui s'est passé | Que faire |
| --- | --- | --- | --- |
| `space_unverified` | 403 | L'espace n'est pas vérifié : ses boîtes reçoivent, mais n'envoient pas. | Demander à l'humain le code à 6 chiffres, puis appeler `verify`. S'il n'a rien reçu, ou si aucun e-mail n'est rattaché à l'espace : `attach_human`. |
| `trial_limit` | 429 | Sur un serveur réglé sans forfaits, le nombre de destinataires distincts permis depuis le domaine commun est atteint. | Suivre la piste : elle donne le moment où l'envoi reprend. |
| `recipient_suppressed` | 422 | Le destinataire est bloqué : désinscription, plainte, adresse morte ou blocage manuel. | Ne plus écrire à cette adresse, depuis aucune boîte. |
| `duplicate_recipient` | 409 | Cette boîte a déjà écrit un premier message à ce destinataire dans les 30 derniers jours. | Répondre dans le fil donné par la piste, avec `reply_to_thread`. |
| `key_daily_cap` | 429 | Le plafond de messages par jour de la clé est atteint. | Reprendre le lendemain, à partir de 0 h, heure de Paris. |
| `inbox_suspended` | 409 | Le coupe-circuit a suspendu la boîte. La raison est dans le message. | Vérifier la liste de destinataires. La reprise est manuelle, par un administrateur de Subagent : l'humain la demande avec `request_inbox_review`. |
| `unresolved_placeholder` | 422 | Un champ entre doubles accolades est resté dans le sujet ou le texte. | Remplacer chaque champ par sa valeur. Seul `{{unsubscribe_url}}` est accepté. |
| `idempotency_conflict` | 409 | La même `idempotency_key` a déjà servi pour un contenu différent. | Même message : réutiliser la clé telle quelle. Nouveau message : en prendre une nouvelle. |
| `forbidden` | 403 | La clé ne porte pas la permission que l'outil demande. | Pour `approve` : le geste revient à l'humain, depuis son assistant branché à `https://api.subagent.fr/connect`. La piste le dit. |

Tous les codes (84) : [`reference.md`](reference.md#erreurs), ou `subagent_mail.CODES`.

`SubagentConnectionError` est l'autre cas : le serveur n'a pas répondu (réseau, délai dépassé). Rien ne dit alors si l'appel a abouti.

## Idempotence

Passez une `idempotency_key` à chaque envoi qu'un agent pourrait rejouer. Elle part dans l'en-tête `Idempotency-Key`.

```python
premier = client.send_email(
    inbox_id=boite["id"], to="marie@exemple.fr", subject="Compte rendu", text="Bonjour Marie, …",
    test=True, idempotency_key="compte-rendu-12-octobre",
)
second = client.send_email(
    inbox_id=boite["id"], to="marie@exemple.fr", subject="Compte rendu", text="Bonjour Marie, …",
    test=True, idempotency_key="compte-rendu-12-octobre",
)
print(second["replayed"])  # True : rien de nouveau n'a été créé
```

Même clé, même contenu : le message déjà créé, avec `replayed` à vrai. Même clé, autre contenu : refus `idempotency_conflict`.

Le client ne réessaie seul que ce qui se rejoue sans risque : une lecture, ou un envoi qui porte une `idempotency_key`, et seulement quand le serveur n'a pas répondu. Un refus n'est jamais réessayé.

## Asynchrone

`AsyncSubagent` a les mêmes méthodes, à attendre avec `await`.

```python
import asyncio
from subagent_mail import AsyncSubagent

async def reponses_a_traiter():
    client = AsyncSubagent()
    fils = await client.list_threads(status="replied")
    return fils["items"]

print(asyncio.run(reponses_a_traiter()))
```

## Réglages

| Argument | Par défaut | Rôle |
| --- | --- | --- |
| `api_key` | variable `SUBAGENT_KEY` | La clé `sak_…` de l'agent. |
| `base_url` | `https://api.subagent.fr`, ou variable `SUBAGENT_BASE_URL` | L'adresse du service. |
| `timeout` | 30 | Délai d'un appel, en secondes. |
| `max_retries` | 2 | Réessais quand le serveur ne répond pas, pour les seuls appels rejouables. |

Une opération plus récente que ce SDK s'appelle par son nom : `client.call("nom", {"argument": "valeur"})`.

## Tests

Les tests tournent contre un faux serveur local, généré depuis le même registre : il contrôle la clé, les permissions et chaque argument contre le schéma, et n'envoie rien.

```sh
python -m unittest discover -s tests
```

Pour essayer un script à la main sans toucher au service :

```sh
python tests/faux_serveur.py   # http://127.0.0.1:8787, clé sak_exemple_agent
```

## Contribuer

Ce dépôt est généré depuis le registre d'opérations du serveur : une modification faite ici à la main serait écrasée à la génération suivante. Ouvrez un ticket plutôt qu'une demande de fusion.

## Licence

MIT. Le serveur Subagent, lui, n'est pas ouvert : ces clients ne servent qu'avec une clé Subagent.
