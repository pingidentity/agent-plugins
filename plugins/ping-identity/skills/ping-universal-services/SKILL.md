---
name: ping-universal-services
description: >-
  Use this skill whenever the task involves configuring or invoking a Ping shared service at the policy or service level. Triggers: PingOne Protect (risk scoring, predictors, risk policies, Signals SDK); PingOne Verify (KYC, identity proofing, document + liveness, verification policies); PingOne MFA (device management, MFA policies, enrollment API, MFA-as-a-service); PingOne Credentials (verifiable credential issuance, presentation, revocation); PingOne IGA (access requests, access reviews, provisioning, entitlements); PingOne Authorize (fine-grained authorization, ABAC policies); cross-platform SSO; "which shared service do I need". Service-in-flow rule — when a Protect, Verify, IGA, or Authorize node or connector appears inside a DaVinci flow or AIC journey, configuring that node, connector, or service invocation belongs here, NOT in ping-orchestration. Orchestration owns the flow shape; this skill owns the service node configuration regardless of where the node lives. Do NOT trigger on vague "add security" requests — clarify which service first. Also invoke with /ping-universal-services.
compatibility: Designed for Ping Identity shared services work. References product docs and the Ping Marketplace.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-universal-services

Shared strategic services used across PingOne, PingOne Advanced Identity Cloud (AIC), and Ping Software Suite — invoked from flows rather than administered as standalone products. Covers PingOne Protect (risk), PingOne Verify (identity proofing / KYC), PingOne Credentials (verifiable credentials), PingOne IGA (governance), PingOne Authorize (fine-grained authorization), and cross-platform SSO.

## Invocation

Invoke explicitly with `/ping-universal-services` or by saying "use ping-universal-services to...".

## When to use this skill

- "Add PingOne Protect risk evaluation to my login flow"
- "Use PingOne Verify for KYC / identity proofing during registration"
- "Configure PingOne MFA — device management, MFA policies, or MFA-as-a-service enrollment API"
- "Issue or present a verifiable credential"
- "Add IGA governance to my PingOne environment"
- "Use PingOne Authorize for fine-grained authorization"
- "Score risk with PingOne Protect and adapt the journey based on the signal"
- "Cross-platform service selection — which shared service do I need?"

## When NOT to use this skill

- If the task is platform setup or admin: use `ping-foundation`.
- If the task is flow / journey design (without a specific service invocation): use `ping-orchestration`.
- If the user is just orienting or choosing a platform: use `ping-quickstart`.
- If the task is integrating a Protect / Verify / Credentials **SDK or library into app code**: use `ping-app-integration` — SDK wiring is app integration, not service configuration.
- If the user mentions "add security" or "prevent suspicious logins" without naming a specific service, ask a clarifying question — the task may be Protect (risk scoring) or just MFA (orchestration).
- If the task is **MFA node/connector wiring within a journey or flow** (not MFA policy or device management): use `ping-orchestration` — that is flow design, not service configuration.
- If the task is generic app / SDK integration without referencing a named Universal Service: use `ping-app-integration`.
- **PingOne Recognize** — not yet GA; this skill will cover it when available.

## Multi-skill use cases

A complete identity verification or risk-based flow typically spans:

| Layer | Skill |
|---|---|
| Platform setup | `ping-foundation` |
| Flow / journey design | `ping-orchestration` |
| Service invocation (Protect, Verify, etc.) | `ping-universal-services` (this skill) |
| App integration | `ping-app-integration` |

**End-to-end example — risk-gated identity proofing with Protect + Verify:**

1. Use `ping-foundation` to provision the PingOne environment and license both Protect and Verify.
2. Use `ping-orchestration` to design the DaVinci flow or AIC journey (login nodes, branching logic).
3. Use `ping-universal-services` (this skill) to configure the Protect connector/node, set the risk policy thresholds, wire the Verify connector/node, and handle VERIFIED / REQUIRES_REVIEW outcomes.
4. Use `ping-app-integration` to embed the Protect JavaScript SDK in the user-facing application.

When Protect and Verify are configured here, hand off to `ping-app-integration` for SDK wiring and to `ping-orchestration` for any remaining flow-level branching.

## Routing — Step 1: What are you trying to do?

| Task | Branch |
|---|---|
| Evaluate risk or adapt flows based on risk signals | Protect branch |
| Identity proofing / document + liveness check | Verify branch |
| PingOne MFA — device enrollment API, MFA policy config, MFA-as-a-service | MFA branch — see `references/curated/choosing-the-right-service.md` for MFA vs flow-level MFA routing |
| Issue or present verifiable credentials | Credentials branch |
| Governance, access reviews, provisioning | IGA branch |
| Fine-grained authorization policies | Authorize branch |
| Cross-application session management / token issuance | SSO branch |
| "Which service do I need?" | Cross-service selection (curated overview) |

## Step 2: Load the curated reference

| Task | Curated reference |
|---|---|
| Cross-service selection / orientation | `references/curated/universal-services-overview.md` |
| Service selection decision (which service do I need?) | `references/curated/choosing-the-right-service.md` |
| Invocation patterns (DaVinci, AIC, PingFederate) | `references/curated/service-invocation-patterns.md` |
| Cross-platform usage constraints and service chaining | `references/curated/cross-platform-service-usage.md` |
| Protect predictors, risk policies, Signals SDK setup | `references/curated/protect-configuration.md` |
| Verify policy fields, verification types, transaction lifecycle | `references/curated/verify-configuration.md` |
| PingOne MFA policy config, device management, pairing keys, enrollment API, AMR codes | `references/curated/mfa-configuration.md` |

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

## Retrieval escalation

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
2. Generated shortlists (`references/generated/<service>/`) — not yet populated; skip this tier until CI populates them.
3. Docs MCP fallback — see `references/runtime/docs-mcp-routing.md`. Only if curated anchors are insufficient.
