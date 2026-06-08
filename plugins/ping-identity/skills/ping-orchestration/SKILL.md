---
name: ping-orchestration
description: >-
  Use this skill whenever the task involves designing, building, or advising on authentication flows, journeys, or orchestration logic in Ping Identity. Triggers: DaVinci flows, PingOne ST journeys, PingAM authentication trees, scripted decision nodes; login, registration, recovery, MFA, or step-up journey design; passwordless authentication (passkeys, FIDO2, magic links, biometric); authenticator app enrollment, TOTP, push MFA flows; transaction approvals via email or push notification (CIBA, out-of-band step-up); progressive profiling, social login, consent; flow troubleshooting; "what nodes do I need", "design a flow for", "build a journey that". When the user asks "journey vs DaVinci flow?", "AIC or DaVinci?", "which orchestration platform should we use?", or "where do I configure MFA in Ping?" without stating both a use case (workforce / CIAM / B2B) AND a platform — you MUST ask one clarifying question before recommending. Do not guess. Also invoke with /ping-orchestration.
compatibility: Designed for Ping Identity orchestration tasks. MCP tools for PingOne ST are used when available to create and update journeys directly.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-orchestration

Design and build authentication flows, orchestration logic, and journey-based experiences across Ping Identity platforms. MCP tools handle execution; this skill supplies design patterns, node sequencing, branching logic, and platform-specific constraints.

## Invocation

Invoke this skill explicitly with `/ping-orchestration` or by saying "use ping-orchestration to...".

## When to use this skill

Trigger on ANY question — including advisory, planning, and "what nodes do I need" requests, not just implementation — when the task involves:
- Building or designing a login, registration, recovery, MFA, or step-up journey in PingOne ST / AIC / PingAM
- Passwordless authentication flows (passkeys, FIDO2, magic links, biometric)
- Authenticator app login, push MFA, or TOTP enrollment flows
- Transaction approvals via email or push (CIBA / out-of-band step-up)
- Creating or designing a DaVinci flow for authentication, MFA, or orchestration
- Configuring a PingAM authentication tree or scripted decision node
- Planning or reviewing journey structure before implementation
- Deciding between inner journeys, scripted nodes, or DaVinci connectors
- Any question about designing, planning, or advising on authentication flows, journeys, or orchestration logic in PingOne ST, PingOne MT / DaVinci, or PingAM

## When NOT to use this skill

- If the platform is not yet set up (no tenant, no realm, no app registered): use `ping-foundation` first
- If the task is **configuring the platform layer** (apps, directories, policies, branding): use `ping-foundation`
- If the task is **invoking a Universal Service** (Protect, Verify, IGA, Credentials) without needing flow design: use `ping-universal-services`
- If the task is **integrating the flow into an app or SDK**: use `ping-app-integration`
- If unsure which platform: use `ping-quickstart` first

## Multi-skill use cases

| Sequence | Skill |
|---|---|
| Before: tenant, realm, identity store, app configured | `ping-foundation` |
| After: risk scoring, MFA step-up, identity verification | `ping-universal-services` |
| After: wire flow into web, mobile, or SDK app | `ping-app-integration` |

---

## MCP tool-first execution

Scan available tools for MCP tools that can perform the required operation. If matching tools are available, run the **MCP config preflight** below first, then use them. Otherwise, proceed with curated references.

## MCP config preflight

> **How these MCP servers work:** Both the AIC and DaVinci MCP servers run **locally on your machine** and communicate over **stdio**. When you invoke an MCP tool, Claude Code spawns the server process via `npx` and sends JSON-RPC messages over stdin/stdout. The server then makes authenticated HTTP calls to your AIC tenant or PingOne DaVinci environment on your behalf. No cloud relay is involved — the process runs in your local shell with your configured credentials.

Before calling any AIC or DaVinci MCP tool, verify the required values are present in `~/.claude/settings.json` under `pluginConfigs["ping-identity-agent-plugins@pingidentity"].options`:

1. Read `~/.claude/settings.json` and check for the relevant keys under `pluginConfigs["ping-identity-agent-plugins@pingidentity"].options`.
2. For any missing or empty value, use `AskUserQuestion` to prompt the user.
3. Write confirmed values into `~/.claude/settings.json` under `pluginConfigs["ping-identity-agent-plugins@pingidentity"].options` using the Edit tool. Example structure:
   ```json
   "pluginConfigs": {
     "ping-identity-agent-plugins@pingidentity": {
       "options": {
         "aic_base_url": "https://openam-yourcompany.forgeblocks.com"
       }
     }
   }
   ```
4. Tell the user to run `/reload-plugins` so the MCP server picks up the new values before proceeding.

**AIC MCP** (platform: PingOne Advanced Identity Cloud / PingAM):

| option key | Ask if missing |
|---|---|
| `aic_base_url` | "What is your AIC tenant base URL? (e.g. `https://openam-mycompany.forgeblocks.com`)" |

**DaVinci MCP** (platform: PingOne + DaVinci):

| option key | Ask if missing |
|---|---|
| `davinci_environment_id` | "What is your PingOne environment ID (UUID)?" |
| `davinci_client_id` | "What is your PingOne Worker Application Client ID?" |
| `davinci_root_domain` | "What is your PingOne root domain? (e.g. `pingone.com`, `pingone.eu`) — default: `pingone.com`" |
| `davinci_custom_domain` *(optional)* | "Do you have a custom PingOne domain? (e.g. `auth.example.com`) — leave blank if using a standard regional domain" |

Only prompt for the server matching the detected platform branch. Do not ask for DaVinci values when executing against AIC, and vice versa.

### Cursor MCP preflight

If running inside Cursor, `userConfig` is not available. MCP servers are configured via environment variables. **Always attempt the MCP tool call directly — do not pre-check or ask for credentials.** Only surface configuration guidance if the call actually fails:

1. Call the requested MCP tool directly.
2. If the call **fails or the tool is unavailable**, tell the user:

   > "The Ping Identity MCP server is not responding. This usually means required environment variables are not set. Please configure the following in your shell (`~/.zshrc` or `~/.bashrc`) or in Cursor's MCP settings (**Settings → MCP → [server name] → Environment**):"
   >
   > **AIC server** (`aic`):
   > | Variable | Value |
   > |---|---|
   > | `AIC_BASE_URL` | Your AIC tenant base URL (e.g. `https://openam-mycompany.forgeblocks.com`) |
   >
   > **DaVinci server** (`davinci`):
   > | Variable | Value |
   > |---|---|
   > | `DAVINCI_MCP_ENVIRONMENT_ID` | Your PingOne environment UUID |
   > | `AUTHORIZATION_CODE_CLIENT_ID` | Your PingOne Worker Application Client ID |
   > | `ROOT_DOMAIN` | Regional domain — `pingone.com`, `pingone.eu`, or `pingone.asia` (default: `pingone.com`) |
   > | `CUSTOM_DOMAIN` | *(optional)* Your custom PingOne domain (e.g. `auth.example.com`) |
   >
   > "After setting the variables, reload the window (**Cmd+Shift+P → Developer: Reload Window**) and try again."

3. If the probe **succeeds**, proceed with the task using MCP tools.
4. Only fall back to curated references if MCP tools remain unavailable after the user has confirmed configuration.

---

## Routing — Step 1: Which platform?

| Platform signal | Branch |
|---|---|
| PingOne Advanced Identity Cloud (AIC), PingAM, identity cloud, ForgeRock lineage | [PingOne Advanced Identity Cloud](#pingone-advanced-identity-cloud) |
| PingOne + DaVinci | [PingOne / DaVinci](#pingone--davinci) |

---

## PingOne Advanced Identity Cloud

Sub-routing by task and journey use case: see `references/curated/pingone-st/routing-index.md`.

**Quick reference — node families:**

| Task | Reference |
|---|---|
| Journey design principles, patterns, resilience, security | `references/curated/pingone-st/journey-design-patterns.md` |
| Node composition rules, PageNode usage, child node gotchas | `references/curated/pingone-st/nodes/node-fundamentals.md` |
| Username/password, passthrough auth, session entry, lifecycle outcomes | `references/curated/pingone-st/nodes/basic-auth-nodes.md` |
| MFA: WebAuthn, OATH, push, OTP, recovery codes | `references/curated/pingone-st/nodes/mfa-nodes.md` |
| Risk scoring, lockout, CAPTCHA, auth level, PingOne Authorize | `references/curated/pingone-st/nodes/risk-management-nodes.md` |
| Registration, attributes, consent, KBA, T&C, social login, SelectIdP | `references/curated/pingone-st/nodes/identity-management-nodes.md` |
| Scripting, page composition, session, state, async, polling, LoginCount | `references/curated/pingone-st/nodes/utility-nodes.md` |
| SAML/OIDC federation, Twilio Verify, device/cookie/cert | `references/curated/pingone-st/nodes/federation-contextual-nodes.md` |

**Generated shortlist** (fallback):
- `references/generated/pingone-st/top-25.json`

---

## PingOne / DaVinci

**Sub-routing by task:**

| Task | Reference |
|---|---|
| DaVinci flow concepts, connectors, variables, versioning | `references/curated/pingone-mt/davinci-overview.md` |
| DaVinci flow design patterns (login, registration, step-up, error) | `references/curated/pingone-mt/davinci-flow-patterns.md` |
| DaVinci registration + email verification + MFA enrollment/step-up | `references/curated/pingone-mt/davinci-registration-and-mfa.md` |

---

## Cross-platform orchestration patterns

| Task | Reference |
|---|---|
| Passkeys / passwordless / FIDO2 design across PingOne MT, PingOne ST, Ping Software | `references/curated/cross-platform/passkeys-and-passwordless.md` |

**Generated shortlist** (fallback): `references/generated/pingone-mt/top-25.json`

---

## Retrieval escalation

Load 1–3 curated anchors for the detected platform/task; stop if sufficient. If not, scan the generated shortlist; pull summaries only.

## Cross-skill escalation

| If the task also involves... | Reference skill |
|---|---|
| Platform setup not yet complete | `ping-foundation` |
| Shared services (Protect, Verify, IGA, Credentials) within the flow | `ping-universal-services` |
| App/SDK code integration | `ping-app-integration` |
| Platform selection or orientation | `ping-quickstart` |
