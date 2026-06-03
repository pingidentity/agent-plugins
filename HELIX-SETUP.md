# Helix Setup Guide — AIC and DaVinci

> Compiled from internal Ping Identity documentation (Glean-indexed). Source URLs cited inline. Some sections (notably DaVinci validation/apply gates) had only partial documentation available; those are flagged explicitly.

---

## 1. Helix Overview

Helix is Ping's low-code AI Agent platform, originally released as the "Helix Playground" (formerly "Everest") in Q4 2024 and now being ported into PingOne. It exposes REST APIs for building, publishing, and invoking AI agents. Agents are graph-based (DAG of nodes) and consist of inputs (Text/File), AI Tasks, Functions, AI/Function Decisions, Vector Search, and Output nodes.

Key concepts ([Helix Playground Release](https://docs.google.com/document/d/1VSUvZO14KG5jUfx8ZLJsXWR7YTNmo3X5KDWNkBu1QPk), [Helix Security Guide](https://docs.google.com/document/d/1Ij0kkgnXIInDHdIJVS4Hnmau9aG-1RosxUkEwYAcfEU)):

- **Tenant / Environment** — multi-tenant unit; each PingOne or AIC environment can map 1:1 to a Helix environment.
- **IDP** — every Helix environment is bound to an IDP (AIC, PingOne, or external). The IDP governs agent identity lifecycle, inbound auth, and outbound auth.
- **Agent** — a published unit identified by `(env_id, name, version)`. Draft → Published lifecycle, multiple published versions allowed for A/B and rollout.
- **Conversation** — message container per session; channels carry messages between user ↔ agent (default channel is auto-created).
- **Channel** — communication path. Simple agents use a single auto-generated User↔Agent channel.
- **Message** — has `class` (`start`, `wait`, `complete`), `content` (input field map), `field_id`, `value`. Async by default; LLM calls are long-running.
- **Tools** — registered Python functions or HTTP/REST calls invocable from AI Task nodes. Tools declare credential aliases.
- **Credentials** — four types: `Service Account JWK`, `OAuth Client`, `API Key`, `CIBA`. Stored per-agent.
- **`get_security_headers()`** — Helix runtime helper that returns the `Authorization` (or custom) header for outbound calls.

Hierarchy: `Agent → Conversation → Channel → Messages` ([Agent Interaction Model](https://docs.google.com/document/d/1RTXcH4Mit_WCSBGotUMNA68Zm9W6gX0DDXJmdzfIwjA)).

Public landing: https://www.pingidentity.com/en/lp/ac/pinghelix.html
Helix Playground UI: https://openam-helix.forgeblocks.com/dpc

---

## 2. Prerequisites

- **Helix tenancy** — provisioned by the Helix team. Internally requested in `#helix-playground` Slack ([Helix Playground Release](https://docs.google.com/document/d/1VSUvZO14KG5jUfx8ZLJsXWR7YTNmo3X5KDWNkBu1QPk)).
- **Helix role** — one of `Data Admin`, `Data Author`, `Data Viewer`. Only Data Admins can create API keys and invite users.
- **An IDP**:
  - **AIC**: an AIC tenant (e.g. `*.forgeblocks.com`) with an OAuth 2.0 client. DCR (Dynamic Client Registration) recommended so agent identities are created automatically.
  - **PingOne**: a worker app in the target environment with roles `Client Application Developer` (for DCR-style agent identity creation) and `Configuration Read Only` at organization level.
- **Helix environment ID** — UUID assigned at tenant creation; required in every API path.
- **Authentication credential**: API Key (`x-api-key` header) OR a Bearer access token from the onboarded IDP.
- **For headless invocation**: a Published agent version (drafts can also be invoked, but tokens via API key only target published versions).

Two API base URLs referenced internally:
- `https://openam-helix.forgeblocks.com/dpc/jas/helix/v1` — playground / AIC-hosted Helix
- The same path mounted behind `helix-proxy` inside PingOne (see §4.1)

Sources: [Helix-AIC Integration](https://docs.google.com/document/d/1fwQ8ZjCVNzTr2BFtl2HHvuEFwjSxkbgx20igl97jlGQ), [Helix Security Guide](https://docs.google.com/document/d/1Ij0kkgnXIInDHdIJVS4Hnmau9aG-1RosxUkEwYAcfEU).

---

## 3. Setting up Helix with PingOne AIC

### 3.1 Configure AIC as IdP for Helix

(From [Helix Security Guide §IDP onboarding for AIC](https://docs.google.com/document/d/1Ij0kkgnXIInDHdIJVS4Hnmau9aG-1RosxUkEwYAcfEU) and [Helix-AIC Integration](https://docs.google.com/document/d/1fwQ8ZjCVNzTr2BFtl2HHvuEFwjSxkbgx20igl97jlGQ).)

1. In the AIC admin UI, create an OAuth 2.0 Client in the alpha realm with:
   - `client_id` and `client_secret` (the doc demo uses `helix-idp-demo` for both).
   - **Grant types**: at minimum `Client Credentials`. Add `Resource Owner Password Credentials` if you want user-token issuance against this client.
   - **Scopes**: `openid`, `profile` (plus product-specific scopes such as `fr:idm:*`, `fr:iga:*`).
   - DCR scope enabled if you want Helix to auto-create agent identities.
2. Switch to AIC **Native Consoles → Access Management**, select the alpha realm, then **Services → OAuth2 Provider → Advanced**, and set `OAuth2 Token Signing Algorithm = RS256` (so Helix can validate tokens via JWKS URI).
3. In Helix UI, go to **Admin → Identity Provider** and enter the AIC client details (issuer, JWKS URI, client_id, client_secret, token endpoint).
4. Save. The Helix environment now uses AIC for inbound auth and agent-identity creation.

**Verify**: Create a draft agent. If DCR was enabled, an OAuth client named `<env_id>_<agent_name>_agent` (e.g. `32ea2671_2337_4f50_bcfb_693c0072672a_DescribePlace_agent`) appears in AIC's OAuth Clients section.

### 3.2 Configure agent identity / OAuth client credentials

Two paths (Security Guide §Agent Identity, §Manually create OAuth Client):

**Auto (DCR)**: If the IDP onboarding client has DCR scope, every new Helix agent automatically receives an OAuth client in AIC. No manual work.

**Manual**:
1. In AIC, create a Custom Application → OIDC OpenId Connect → Service.
2. Set name/owner; assign client_id and client_secret.
3. On the **Sign On** tab: Grant Types = `Client Credentials`; Scopes = `openid profile` (+ any product scopes).
4. In Helix UI, click the three-dot menu next to the agent → **Agent Identity** → enter `client_id` and `client_secret`.

**Agent credentials (separate from agent identity)** — used by tools/functions for outbound calls. Four types via Helix UI (three-dot menu → **Credentials**) or REST API:

```
POST https://openam-helix.forgeblocks.com/dpc/jas/helix/v1/environments/<env_id>/agents/<agent_name>/credentials
Authorization: <bearer or x-api-key>
Content-Type: application/json
{
  "credential_name": "iga-oauth",
  "credential": {
    "type": "oauth",
    "client_id": "<id>",
    "client_secret": "<secret>",
    "token_endpoint": "<token_endpoint>",
    "scope": "fr:iga:*"
  }
}
```

Notes:
- For OAuth: `grant_type` is hard-coded to `client_credentials`.
- For Service Account: uses `urn:ietf:params:oauth:grant-type:jwt-bearer`.
- For OAuth-via-AIC, the example agent (`AICIGAAgentUsingOAuthCredentials`) requires creating an Auth Script and enabling **OAuth Provider Overrides → Access Token Modification Plugin Type = SCRIPTED** in AIC.

### 3.3 Author custom tools for AIC REST

Tools are Python functions registered in Helix. They use credential aliases that the consuming agent must satisfy at runtime.

**Pattern A — Function inside an agent (inline)**:

```python
def function0b138036f3d7(textInput9999aa5e0489: str):
    import requests
    from helix.security import get_security_headers
    url = f"https://{baseUrl}/openidm/managed/alpha_user?_queryFilter=mail eq '{textInput9999aa5e0489}'"
    headers = get_security_headers(
        credential_name='am_users',
        scope='fr:idm:*',
        grant_type='urn:ietf:params:oauth:grant-type:jwt-bearer'
    )
    headers['accept'] = 'application/json'
    return requests.get(url, headers=headers).json()
```

**Pattern B — Reusable custom tool (preferred)** — registered separately under **Tools** in Helix Studio, given an alias. The using agent satisfies the alias via Tool Credentials at agent config time.

```python
def get_aic_user_by_filter(email: str):
    import requests
    from helix.security import get_security_headers
    url = f"https://{baseUrl}/openidm/managed/alpha_user?_queryFilter=mail eq '{email}'&_fields=userName,givenName,sn,mail"
    headers = get_security_headers(
        credential_name=am_users,                 # NOTE: unquoted alias
        scope='fr:idm:*',
        grant_type='urn:ietf:params:oauth:grant-type:jwt-bearer'
    )
    headers['accept'] = 'application/json'
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()
```

**`get_security_headers()` reference** (Security Guide §Integration: Get Security Headers in Tools and Functions):

```python
def get_security_headers(
    credential_name=None,        # alias name, unquoted when used inside a tool
    scope=None,                  # required for OAuth/SA
    grant_type=None,             # client_credentials | urn:ietf:params:oauth:grant-type:jwt-bearer
    use_existing_token=False,    # token passthrough — no other params needed
    custom_header=None,          # default 'Authorization'; e.g. 'API_KEY'
    use_agent_token=False        # use agent identity instead of credential
): ...
```

Returns: `{'Authorization': 'Bearer ey…'}` or `{'<custom_header>': '...'}`.

**Tool registration UI flow**: Tools section → New Tool → declare parameters, add Python script. Define aliases inline; tools become visible in Agent's Tool Credentials tab where the agent author binds each alias to a real credential (created on the fly with the `+` button).

End-to-end examples: Security Guide sections **Agents → P1 User info using custom tools** (PingOne) and **AGENT → AIC User info using custom tools** (`GetAICUser`, `GetAICUserByFilter`).

### 3.4 Headless conversation invocation

Three forms of inbound auth ([Helix Security Guide §Inbound Access](https://docs.google.com/document/d/1Ij0kkgnXIInDHdIJVS4Hnmau9aG-1RosxUkEwYAcfEU)):

1. **Helix API key** (`x-api-key: <value>`) — created by Data Admin in **Admin → API Keys**. Scoped to tenancy + agent IDs. Recommended for service-to-service headless invocation.
2. **AIC end-user / client OAuth bearer** (`Authorization: Bearer ...`).
3. **Helix user token** copied from the Helix UI's network call (development only).

**Get an AIC bearer (client_credentials)**:

```bash
curl -X POST 'https://openam-qa-helix-testimg.forgeblocks.com/am/oauth2/alpha/access_token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Authorization: Basic <base64(client_id:client_secret)>' \
  -d 'scope=openid profile' \
  -d 'grant_type=client_credentials'
# → { "access_token": "ey...", "token_type": "Bearer", "expires_in": 3599 }
```

**Conversation lifecycle** (concrete URLs from [Helix-AIC Integration](https://docs.google.com/document/d/1fwQ8ZjCVNzTr2BFtl2HHvuEFwjSxkbgx20igl97jlGQ) and [Agent Interaction Model](https://docs.google.com/document/d/1RTXcH4Mit_WCSBGotUMNA68Zm9W6gX0DDXJmdzfIwjA)):

**Step 1 — Create a conversation**:

```bash
curl -X POST \
  'https://openam-helix.forgeblocks.com/dpc/jas/helix/v1/environments/<env_id>/agents/<agent_name>/conversations' \
  -H 'Authorization: Bearer ey...' \
  -H 'Content-Type: application/json' \
  --data '{
    "name": "conversation_2805957c-a6a1-40ee-bd00-fc238c6fba64",
    "agent": { "version": "0.08" }
  }'
```

Response:
```json
{
  "created_on": "2025-01-24T19:30:48Z",
  "home_channel": "500e0225-78fe-45c5-a5f7-f5664b5a2a5e",
  "id": "62cbdcaf-115e-4edd-a311-105ce6724fdb",
  "name": "conversation_e42f4da6-...",
  "owner": "e51fa13c-c536-4d60-b9cc-81a84c4214eb"
}
```

**Step 2 — Post a START message** (to `home_channel`). Sync vs async selected by Content-Type:

- Sync: `Content-Type: application/json`
- Async: `Content-Type: application/json; async=true`

```bash
curl -X POST \
  'https://openam-helix.forgeblocks.com/dpc/jas/helix/v1/environments/<env_id>/conversations/<conv_id>/channels/<channel_id>/messages' \
  -H 'Authorization: Bearer ey...' \
  -H 'Content-Type: application/json; async=true' \
  --data '{
    "class": "start",
    "content": {
      "textInputbc96883ff5d3": "Melbourne"
    }
  }'
```

Sync response:
```json
{
  "message_class": "complete",
  "conversation_id": "...",
  "message_id": "...",
  "channel_id": "...",
  "content": [{
    "class": "complete",
    "field_id": "task384d0d61d94e",
    "type": "text",
    "value": "Melbourne is a dynamic and cosmopolitan city..."
  }]
}
```

Async response:
```json
{ "message_class": "wait", "conversation_id": "...", "message_id": "078fba75-...", "channel_id": "..." }
```

**Step 3 — Poll the channel for completes** (async only):

```bash
curl 'https://openam-helix.forgeblocks.com/dpc/jas/helix/v1/environments/<env_id>/conversations/<conv_id>/channels/<channel_id>/messages' \
  -H 'Authorization: Bearer ey...'
```

Loop until you see a message with `sender_role: "agent"`, `class: "complete"`, and `initiator_message_id == <id from Step 2>`. Structured agent output is in `value` (typically JSON when the agent uses an output node).

**Step 4 — (Optional) Inspect run trace**:

```bash
GET https://openam-helix.forgeblocks.com/dpc/jas/helix/internal/v1/environments/<env_id>/conversations/<conv_id>/channels/<channel_id>/messages/<message_id>/runs
```

Returns full execution trace including each node's prompt stack, model metrics, and intermediate outputs.

**Step 5 — Close** — Helix manages cleanup; no explicit close API documented. Conversations are not currently expected to be re-opened by users; automatic cleanup policy is TBD ([Agent Interaction Model](https://docs.google.com/document/d/1RTXcH4Mit_WCSBGotUMNA68Zm9W6gX0DDXJmdzfIwjA)).

**Important quirk**: When Helix returns the polled message list, a START message with `n` inputs is *expanded into `n` individual messages* on the channel, all sharing the same `message_id` but different `field_id`. Documented as confusing; may change before GA.

### 3.5 Token passthrough setup

Use case: forward the inbound user's token into outbound calls so downstream APIs enforce that user's permissions ([Helix Security Guide §Token Passthrough](https://docs.google.com/document/d/1Ij0kkgnXIInDHdIJVS4Hnmau9aG-1RosxUkEwYAcfEU)).

When to use:
- Calling APIs that don't support standard OAuth client_credentials (notably DaVinci endpoints).
- Need user-scoped authorization in the agent's outbound calls.
- Cross-environment scenarios where agent identity wouldn't have the right perms.

Setup: no per-agent credential to create. The function opts into passthrough:

```python
def functionedfc6bf898a7(textInputf89a326d1a9c: str):
    import requests
    from helix import security
    headers = security.get_security_headers(use_existing_token=True)
    headers['Accept'] = 'application/json'
    return requests.get("https://openam-helix.forgeblocks.com/dpc/jas/tenants",
                        headers=headers).text
```

Sample agent: **TokenPassthrough** in `helix-security` (Env Id `a9c33d49-52a9-4596-b978-9dd165f719fc`).

Known gotchas (from `#helix-p1-auth-design` Slack):
- Inside PingOne, the access token `helix-proxy` receives is an *internal* token. It is re-signed before being passed downstream; the issuer is preserved so the API Gateway does not block it.
- Cross-environment passthrough requires both the user and agent identities to exist in the same environment (open issue at the time of writing).

---

## 4. Setting up Helix with PingOne DaVinci

Internal documentation is significantly thinner here than for AIC. The DaVinci-Helix integration is being delivered under JIRA **DV-22278** (`P1DAV-E-691`, Gartner-2026 release Q2 2026) and the metrics-Helix POC is closed under **P1ME-3460**. The following is what is documented.

### 4.1 Helix-backed flow generation pattern (architecture)

(From [What and Why PingOne AI Assistant Service](https://docs.google.com/document/d/1H_fLBCGNmDwBd7k2ls17JyfLv9sZIbg6rel5suJTz-M) and [Helix Proxy Claude TM](https://pingidentity.atlassian.net/wiki/spaces/SE/pages/2875555922).)

The DaVinci AI assistant calls Helix through `helix-proxy`, a Java 21 / Spring Boot 3.5 microservice that lives **inside** the PingOne trust boundary:

```
PingOne Console UI → API Gateway → helix-proxy → helix-platform (Helix) → LLM
```

`helix-proxy` is responsible for:
- Conversation / message proxying with OAuth2 JWT enforcement (permissions: `p1ai:create:conversations`, `p1ai:read:conversations`, `p1ai:create:messages`, `p1ai:read:messages`).
- Environment onboarding / offboarding via Kafka events (`ENVIRONMENT.CREATED`, `ENVIRONMENT.DELETED`) — automatically creates a Helix tenant, a PingOne worker app, an environment API key, and an IDP config per eligible PingOne environment.
- Audit event publishing to the `aidp-helix-audit-events` Kafka topic.
- Dynamic URL routing between standard and testing Helix endpoints via `HELIX_TESTING_FEATURE_FLAG` (`HelixUrlResolver`).

A DaVinci-specific proxy hop (`davinci-proxy → helix-proxy → helix-platform → LLM`) was discussed but as of June 2025 is debated; the team is questioning whether the additional hop is necessary (`#davinci-ai-poc` Slack thread, June 2025).

The DaVinci agent itself is small (<1 MB) compared to the PingOne Assistant agent (>5 MB), making Helix conversation creation faster against it (`#helix-bringing-to-p1`, April 2026).

### 4.2 Conversation lifecycle for DaVinci agents

API shape is identical to §3.4 — same paths, same body, same async semantics — but routed through `helix-proxy` instead of directly to `openam-helix.forgeblocks.com`. From a Slack-shared real call (jrawat, April 2026):

```bash
curl --location \
  '<helix-proxy-base>/v1/environments/<env_id>/agents/PingOneAgent/conversations' \
  -H 'Authorization: Bearer <user_admin_token>' \
  -H 'Content-Type: application/json' \
  --data '{ "name": "PingOneAgent Conversation", "agent": { "version": "draft" } }'
```

The PingOne Assistant currently sends the **signed-in user's access token** to `helix-proxy` (not a worker app), and Helix performs token-passthrough authorization. Cross-environment scenarios (admin in env A, agent in env B) are a known limitation; a worker-app-with-client-credentials approach was being brainstormed as of mid-2025.

### 4.3 Authoring DaVinci-facing custom tools

Same Tools/Function pattern as §3.3, but the credential type for DaVinci is **passthrough** (DaVinci does not support standard OAuth, per [Helix Playground Release](https://docs.google.com/document/d/1VSUvZO14KG5jUfx8ZLJsXWR7YTNmo3X5KDWNkBu1QPk) §Agent Credential):

```python
from helix import security
import requests

def list_dv_flows():
    headers = security.get_security_headers(use_existing_token=True)
    headers['Accept'] = 'application/json'
    return requests.get(
        f"https://api.pingone.com/v1/environments/{envId}/davinci/flows",
        headers=headers
    ).json()
```

For DaVinci Metrics specifically, the integration is via a new DV Metrics API designed to accept structured queries from a Helix agent (epic [P1ME-3460](https://pingidentity.atlassian.net/browse/P1ME-3460) — closed POC stage). The Metrics API uses internal IAM roles for write paths; Helix only reads.

### 4.4 Validation, versioning, and apply gates for generated flows

**No internal documentation found via Glean search that specifies the validation/versioning/apply gates for the Helix→DaVinci flow-generation use case** (request shape, returned flow JSON schema, validate-then-apply gate, version reconciliation). Internal threads ([DV-22278](https://pingidentity.atlassian.net/browse/DV-22278), `DaVinci-Helix` label) reference this work but the searchable artefacts are JIRA epics and threat models, not engineering specs. The threat model ([WIP - Helix Runtime in PingOne Threat Model](https://pingidentity.atlassian.net/wiki/spaces/SE/pages/2714697742)) confirms a "DV Assistant (running on Helix services deployed in PingOne)" was slated for May 8, 2026 (Gartner magic quadrant review release), but the request/response contract for `POST flow context → return flow JSON → validate → apply` is not in any indexed doc.

**This section needs to be authored from product team input** — recommended contacts (from Slack history): Sourav Chakraborty (DV-22278 assignee), Satish Varagani (DV-helix-proxy), Mayank Somani (helix-proxy), Raminder Kaler (Helix platform).

---

## 5. Authoring and Publishing Agent Versions

(From [Helix Playground Release §Developing Agents](https://docs.google.com/document/d/1VSUvZO14KG5jUfx8ZLJsXWR7YTNmo3X5KDWNkBu1QPk).)

Identifier: `(env_id, name, version)`. Within an environment you can have:
- At most **one DRAFT** version per name.
- At most **one PUBLISHED** version per name+version (multiple published versions allowed across different version strings).

Authoring options:
- **UI**: Agent Builder canvas — drag Text Input / File Input / AI Task / Function / Vector Search / AI Decision / Function Decision / Output nodes.
- **API**: `POST /environments/<env_id>/agents/` with the full agent JSON (Security Guide includes a complete example for the `describePlaceDemo` agent — `entities`, `ui_config`, `tools`, `tables`, `files`, `version`, `name`).

List endpoints:
```bash
GET .../environments/<env_id>/agents?offset=0&limit=10&state=draft
GET .../environments/<env_id>/agents?offset=0&limit=10&state=published&latest=true
GET .../environments/<env_id>/tools?offset=0&limit=10&type=custom
```

Publish flow:
- In Studio, mark draft as Published; assign a unique version string (no clash with existing published).
- The `version` is referenced in conversation create body (`"agent": { "version": "0.08" }`) when invoking.

Helix API Keys are scoped to `(tenancy, agentIDs)` and required for service-to-service invocation of published agents. Created by Data Admins via Admin → API Keys; **download/copy the key value at creation time** (it is never retrievable later).

CI/CD for agents (Q1 FRAaS epic, design TBD):
- **Agent Bundle** packages agent + tool + config + file + vector-store dependencies.
- **Security Bundle** captures credential provisioning required before the agent is functional.

---

## 6. Sample End-to-End Flows

### 6.1 AIC: Add MFA journey via Helix

End-to-end pattern combining §3:

1. Onboard AIC as IDP for the Helix env (§3.1).
2. Create an AIC service-account credential `am_users` with scope `fr:idm:*`, grant_type `urn:ietf:params:oauth:grant-type:jwt-bearer` (§3.2).
3. Author two custom tools backed by AIC IDM and AM REST:
   - `GetJourneyByName(realm, name) → Journey` (AM endpoint `/am/json/realms/root/realms/{realm}/realm-config/authentication/authenticationtrees/trees/{name}`).
   - `UpdateJourney(realm, name, body)` (PUT to same path with `Accept-API-Version: resource=2.0`).
4. Build an agent **MfaJourneyEditor** with inputs `realm`, `journeyName`, `instruction` and a single AI Task node that uses both tools.
5. Publish version `0.1`. Generate an API key.
6. Headlessly invoke:

```bash
TOKEN="$(./get-aic-token.sh)"

CONV=$(curl -s -X POST \
  "https://openam-helix.forgeblocks.com/dpc/jas/helix/v1/environments/$ENV_ID/agents/MfaJourneyEditor/conversations" \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"add-mfa","agent":{"version":"0.1"}}')

CID=$(jq -r .id <<<"$CONV"); CHAN=$(jq -r .home_channel <<<"$CONV")

curl -s -X POST \
  "https://openam-helix.forgeblocks.com/dpc/jas/helix/v1/environments/$ENV_ID/conversations/$CID/channels/$CHAN/messages" \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json; async=true' \
  -d '{"class":"start","content":{
        "textInputRealm":"alpha",
        "textInputJourneyName":"Login",
        "textInputInstruction":"Insert a Push MFA node after Identity Store Decision."
       }}'
# → poll GET .../channels/$CHAN/messages until class=complete & sender_role=agent
```

The agent calls AM via `get_security_headers(credential_name=am_users, scope='fr:idm:*', grant_type='urn:ietf:params:oauth:grant-type:jwt-bearer')` and writes back the modified Journey JSON.

### 6.2 DaVinci: Generate a flow via Helix

Conceptual pattern (note caveat in §4.4 — exact contract not in internal docs):

1. PingOne Console UI gathers user prompt + current flow context (env_id, flow_id, flow JSON) and sends signed-in admin's access token.
2. UI calls `helix-proxy` `/v1/environments/<env_id>/agents/DaVinciAssistant/conversations` (Bearer = admin token).
3. Posts `start` message: `content` includes `textInputUserPrompt`, `textInputFlowContext`, `textInputEnvironment`.
4. Helix agent uses passthrough credential to call DV admin APIs and an LLM to synthesize new flow JSON.
5. UI polls for `complete`, parses returned JSON, presents diff/preview to admin.
6. UI calls DaVinci's own Apply API (not Helix) to commit the flow — Helix is purely the generation/troubleshoot engine.

Sample shape of the create-conversation call (April 2026 Slack snippet):

```json
POST /v1/environments/<env_id>/agents/DaVinciAssistant/conversations
Authorization: Bearer <admin_pingone_token>
{
  "name": "DV Assistant Conversation",
  "agent": { "version": "draft" }
}
```

The DaVinci agent definition itself, the input schema, and the validation/apply gates are not in indexed docs.

---

## 7. Known Limitations and Gotchas

From Slack threads and threat models:

- **Inbound errors aren't propagated**: the current Helix MVP "does not capture and report internal errors that happen during an agent invocation"; clients must implement timeouts and surface generic error states ([Agent Interaction Model](https://docs.google.com/document/d/1RTXcH4Mit_WCSBGotUMNA68Zm9W6gX0DDXJmdzfIwjA)).
- **Start-message expansion**: a START with N inputs is reflected as N separate messages on the channel sharing one `message_id` — confusing to consumers, may change before GA.
- **Inputs are addressed by generated UUID** (e.g. `textInputbc96883ff5d3`), not by friendly name. Ties UI tightly to a specific agent version. New version → new UIDs → UI updates.
- **PingOne does not support DCR**: agent identity creation requires manual OAuth client provisioning unless `Client Application Developer` role is assigned. **Always assign at least one role** to the worker app or no access tokens will be issued.
- **AIC token-signing** must be RS256 (asymmetric) for JWKS-based validation to work.
- **DaVinci does not support standard OAuth**; outbound calls from a Helix agent into DV must use **token passthrough** (`use_existing_token=True`).
- **Internal access tokens** received by `helix-proxy` are not externally usable — re-signed by `helix-proxy` before forwarding so the API Gateway accepts them.
- **PingOne Assistant agent is >5 MB**, which slowed conversation creation (S3 fetch of agent definition). DaVinci agent is <1 MB and recommended for benchmarking.
- **Cross-environment** PingOne Assistant calls fail when admin is in env A and agent in env B; mitigation under design.
- **`credential_name` inside a tool must be UNQUOTED** (e.g. `worker_user`, not `'worker_user'`) — this is an alias reference, not a string.
- **Sync vs async**: sync requests can hit gateway timeouts on long LLM calls; the Helix team recommends async (`Content-Type: application/json; async=true`) and polling.
- **Admin API keys** can only delete environments and create env-API-keys for environments they themselves created — created by super admins via `#helix-playground` ([Security Guide §Admin API Keys](https://docs.google.com/document/d/1Ij0kkgnXIInDHdIJVS4Hnmau9aG-1RosxUkEwYAcfEU)).
- **Helix Roles**: only Data Admin can create API keys and invite users; Data Author and Data Viewer have reduced perms.
- **Agent token endpoint**: the token endpoint Helix uses for agent identity is whatever was supplied during IDP onboarding — not configurable per-agent.

---

## 8. Source Documents

Primary specs (internal, Glean-indexed):

- **Helix Security Guide 1.0** — owner Raminder Kaler — https://docs.google.com/document/d/1Ij0kkgnXIInDHdIJVS4Hnmau9aG-1RosxUkEwYAcfEU — **the authoritative setup doc**: IDP onboarding, agent identity, agent credentials, `get_security_headers`, sample agents, API keys, token passthrough.
- **Helix Playground Release Notes** — owner Sudhakar Peddibhotla — https://docs.google.com/document/d/1VSUvZO14KG5jUfx8ZLJsXWR7YTNmo3X5KDWNkBu1QPk — concept overview, node types, REST API & Postman pointers, FAQ.
- **Helix-AIC Integration** — owner Andersson Garcia — https://docs.google.com/document/d/1fwQ8ZjCVNzTr2BFtl2HHvuEFwjSxkbgx20igl97jlGQ — concrete curl walkthrough of IDP onboarding through to async conversation + run trace.
- **Journey AI Agent Interaction Model** — owner Dave Ernsting — https://docs.google.com/document/d/1RTXcH4Mit_WCSBGotUMNA68Zm9W6gX0DDXJmdzfIwjA — full Agent → Conversation → Channel → Message lifecycle, request/response shapes, JSON Schema.
- **What and Why PingOne AI Assistant Service** — owner Vasuki Dileep — https://docs.google.com/document/d/1H_fLBCGNmDwBd7k2ls17JyfLv9sZIbg6rel5suJTz-M — `helix-proxy` architecture, sequence diagrams.
- **Helix Proxy Claude TM** — Confluence — https://pingidentity.atlassian.net/wiki/spaces/SE/pages/2875555922 — service summary, tech stack, OAuth permission scheme.
- **Helix Playground Threat Model** — Confluence — https://pingidentity.atlassian.net/wiki/spaces/SE/pages/1167622145
- **PingOne AI Assistant Threat Model** — Confluence — https://pingidentity.atlassian.net/wiki/spaces/SE/pages/1937408023
- **WIP - Helix Runtime in PingOne Threat Model** — Confluence — https://pingidentity.atlassian.net/wiki/spaces/SE/pages/2714697742
- **P1ME-3460 DaVinci Metrics Helix API Threat Model** — Confluence — https://pingidentity.atlassian.net/wiki/spaces/SE/pages/2008121454

Helix MVP API artefacts (referenced from Journey AI doc):
- Helix MVP API Google Drive — https://drive.google.com/drive/folders/1HaXE0Omlm-g9d61KYA7-bMb_2zA5u_zz
- HTML Render of API Specification — https://drive.google.com/file/d/1Mst3JcLozk9WhJI-vIm_qMDEwv_HpH5s/view
- Helix REST APIs (transactional + security) — https://drive.google.com/file/d/1v2t-BgfmuuOKt6FsHfCYixopcbhZIIx3/view
- Helix Agent Evaluation APIs — https://drive.google.com/open?id=1x2sgSDmbRPd3UKHbhKLFAIRzqPPGyVoD
- Postman collection — https://drive.google.com/open?id=1GI8j1psHaALlaeuM-4BjZL50yuHedC7-

JIRA epics:
- DV-22278 (DaVinci-Helix flow generation, Q2 2026) — https://pingidentity.atlassian.net/browse/DV-22278
- P1ME-3460 (DaVinci Metrics API – Helix Integration MVP, closed) — https://pingidentity.atlassian.net/browse/P1ME-3460
- P1AX-3589 (PingOne Helix Integration Service Backend Proxy, closed) — https://pingidentity.atlassian.net/browse/P1AX-3589
- FRAAS-21880 (AIC feature for Running Helix Agents, closed) — https://pingidentity.atlassian.net/browse/FRAAS-21880
- AI-2530 (OOTB report for Helix Token Usage By Model) — https://pingidentity.atlassian.net/browse/AI-2530
- AI-2128 (Assisting PingOne assistant agent) — https://pingidentity.atlassian.net/browse/AI-2128

Slack channels for live questions:
- `#helix-playground` — main support channel; super-admin API key requests go here.
- `#helix-p1-auth-design` — token passthrough / cross-env auth design.
- `#helix-bringing-to-p1` — current PingOne integration coordination.
- `#davinci-ai-poc` — DV-Helix integration discussion.
