---
name: ping-universal-services
description: Use this skill whenever the task involves configuring or invoking a Ping shared service at the policy or service level — not flow design. Triggers: PingOne Protect (risk scoring, predictors, risk policies, Signals SDK); PingOne Verify (KYC, identity proofing, document + liveness, verification policies); PingOne MFA (device management, MFA policies, enrollment API, MFA-as-a-service); PingOne Credentials (verifiable credential issuance, presentation, revocation); PingOne IGA (access requests, access reviews, provisioning, entitlements); PingOne Authorize (fine-grained authorization, ABAC policies); cross-platform SSO; "which shared service do I need". Do NOT trigger on vague "add security" requests — clarify which service first. Also invoke with /ping-universal-services.
compatibility: Designed for Ping Identity shared services work. References product docs and the Ping Marketplace.
metadata:
  publisher: Ping Identity
  version: "1.0.0"
---

# ping-universal-services

Shared strategic services used across PingOne MT, PingOne ST (AIC), and Ping Software Suite — invoked from flows rather than administered as standalone products. Covers PingOne Protect (risk), PingOne Verify (identity proofing / KYC), PingOne Credentials (verifiable credentials), PingOne IGA (governance), PingOne Authorize (fine-grained authorization), and cross-platform SSO.

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

## Retrieval escalation

1. Curated anchors (`references/curated/`) — load 1–3 max. Stop if sufficient.
2. Generated shortlists (`references/generated/<service>/`) — not yet populated; skip this tier until CI populates them.
3. Docs MCP fallback — see `references/runtime/docs-mcp-routing.md`. Only if curated anchors are insufficient.
