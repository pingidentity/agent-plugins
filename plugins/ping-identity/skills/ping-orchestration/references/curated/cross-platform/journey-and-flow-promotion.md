---
title: "Promoting Journeys, Scripts, and DaVinci Flows Between Environments"
product_family: cross-platform
products: ["pingone", "pingone-st"]
capabilities: ["orchestration"]
services: []
audience: ["developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-22"
slug: "https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions.html"
---

# Promoting Journeys, Scripts, and DaVinci Flows Between Environments

Journey-, script-, and DaVinci-flow-specific concerns when promoting between AIC and PingOne environments.

## Scope

**Covers:** What journey and flow config moves; AIC ESV and script gotchas; DaVinci flow versioning and promotion variables; environment lock impact on running journeys; per-node promotion considerations; rollback.

**Does NOT cover:** General promotion model choice, tool selection, environment topology, and Terraform/CaC pipeline — see `ping-foundation` → `references/curated/cross-platform/config-promotion.md`. That anchor is the entry point; load this one only when the task involves journey- or flow-specific concerns.

---

## What journey and flow config moves

### AIC self-service promotions

**Moves (static config):**
- Journeys (authentication trees) and all node configurations
- Scripted Decision node scripts
- Themes and hosted pages customisations
- AM service config (OAuth2 Provider, OIDC, Session, CORS, Social IdPs, WebAuthn, etc.)
- IDM managed-object schema and scripts
- ESV references (the reference moves; the ESV value itself must exist in the target)

**Does not move (dynamic / runtime data):**
- Live user sessions
- User-created or self-registered applications
- MFA device enrollments
- User profile data and custom attributes

### PingOne DaVinci flows

**Moves via native PingOne promotion:**
- Flow definitions (all versions)
- Flow policies (with their dependent flow versions auto-included)
- Connector configuration structure (connection IDs and non-secret settings)

**Connector credentials do not move directly.** PingOne gates promotion of any attribute marked sensitive (client secrets, API keys, passwords embedded in connector config) — the promotion cannot proceed until a **sensitive promotion variable** exists for each blocked attribute. Variables are created in the *source* environment with the target-specific value specified at that point; the connector structure is then promoted and resolves to those target values at promotion time, not the source's.

---

## AIC: ESV and script gotchas

### ESV integrity check

AIC runs an integrity check before starting any promotion. Promotion is **blocked** if:
- A static config item references an ESV that does not exist in the target environment
- An encrypted secret is embedded directly in config rather than referenced via an ESV

**Fix before promoting:** Create the missing ESVs in the upper environment. Replace any inline secrets with ESV references using the AIC admin console (Environments → Environment Secrets & Variables).

### Orphaned or missing scripts

If a Scripted Decision node references a script that is not included in the static config export (e.g. it was created outside the normal journey-editing workflow), the promotion may succeed but the journey fails at runtime when that node executes.

**Fix:** Verify all scripts referenced by Scripted Decision nodes appear in the pre-promotion config snapshot. AIC's self-service promotion UI shows the full list of static resources included.

### PII / sensitive data in script logs

Review Scripted Decision node scripts for `logger.error(...)` or `logger.message(...)` calls that log user attributes before promoting to production. Production log retention is longer and may be subject to compliance requirements.

---

## DaVinci flow promotion: versioning and variables

### Flow versioning

Each DaVinci flow has a **saved version** (draft) and a **published version** (live). Native PingOne promotion moves the published version. Ensure the correct version is published before triggering a promotion.

### Flow-policy dependency

Flow policies reference a specific flow and version. When promoting a flow, also promote its associated flow policy — an unpromoted policy pointing at a flow that no longer matches will fail at authentication time.

### Promotion variables for connector credentials

In DaVinci, connector credentials (client IDs, client secrets, webhook URLs, API keys) are environment-specific. Use **DaVinci promotion variables** to bind these to environment-specific values:

1. In the source flow, replace the literal credential with a promotion variable token.
2. In the target environment, assign the variable to the target-side credential value before applying the promotion.
3. DaVinci flow promotion validates that all referenced variables have assigned values in the target.

---

## Environment lock impact during AIC promotion

AIC requires an **environment lock** on both source and target during a promotion.

| During lock | Effect |
|---|---|
| End-user authentication flows | **Unaffected** — runtime auth continues |
| AIC admin console | Read-only; most writes blocked in the source (dev) environment |
| ESV API | Blocked in the development environment during lock |
| Journey editing (AIC MCP Server, admin console) | Blocked in source during lock |
| Promotion duration | 10–45 minutes depending on config size |

**Implication for iterative development:** If you are actively editing journeys, schedule promotions during off-hours or low-activity windows to avoid blocking your development workflow.

---

## Sequential pair routing

AIC self-service promotions enforce a sequential chain:

```
dev → staging → production
(with UAT, if present: dev → UAT → staging → production)
```

Non-sequential promotion (dev → production directly) is not supported. To validate changes quickly in production-like conditions, promote to staging first, verify, then promote from staging to production.

Sandbox environments sit outside all promotion chains — you cannot promote to or from a sandbox.

---

## Per-node promotion considerations

| Node type | Promotion concern |
|---|---|
| Scripted Decision | Script reference must exist in the target; verify script is included in the static config snapshot before promoting |
| SAML/OIDC federation nodes | Entity IDs and redirect URIs are often environment-specific; use ESVs for issuer URLs and endpoints |
| PageNode / themes | Theme customisations move with the journey; ensure themes are included in the static config snapshot |
| Inner journeys | The inner journey must exist (or be co-promoted) in the target before the outer journey is promoted |
| WebAuthn / FIDO2 nodes | `origins` and `relyingPartyDomain` are environment-specific — use ESVs |
| Push MFA nodes | FCM/APNS credentials are environment-specific; store via ESVs |

---

## Rollback for journeys

If a promoted journey causes issues in the upper environment, AIC self-service rollback restores the prior static config set:

- **Trigger:** `POST /promotions/{promotionId}/rollback` (API only; admin console does not expose rollback)
- **Behaviour:** The upper environment's journey/script set is restored to its pre-promotion state. In-flight sessions on the promoted journey are not interrupted — they continue against the current version in memory until they time out.
- **After rollback:** Diagnose the issue in the source (dev) environment, fix, and re-promote.

---

## Choosing native promotion vs Terraform for journey/flow work

| Scenario | Typical fit | Why |
|---|---|---|
| AIC journey iteration within one tenant chain | AIC self-service promotions | Platform-provided self-service path for AIC; admin-console-driven; sequential pairs enforced by the platform (dev→staging→production only) |
| DaVinci flow changes within one PingOne org | PingOne native promotion | In-console; automatic dependency management; same-org constraint applies |
| Multi-org, multi-cloud, or Git-backed audit trail needed | Ping CLI + Terraform | Terraform providers span PingFederate, PingAccess, PingDirectory, and PingOne; Ping CLI CRUD for PingFederate is still rolling out — check the [compatibility matrix](https://developer.pingidentity.com/pingcli/1.0/product-compatibility.html); state tracking and drift detection via Terraform |
| Mixed AIC journeys + DaVinci flows in the same pipeline | Can combine both | Each platform's native model handles its own config; Terraform manages cross-product baseline |

---

## Prerequisites

- Promotion Admin role (PingOne) or AIC tenant admin access in both environments
- All ESVs referenced in journey/flow config must be pre-created in the target environment
- DaVinci flow promotion variables assigned in the target before promotion
- All dependent inner journeys or scripts co-included in the promotion

---

## Common variants

| Variant | Notes |
|---|---|
| AIC standard dev/staging/prod chain | Sequential pairs; ESVs pre-configured in each upper env |
| AIC with UAT tier | dev → UAT → staging → production; cannot skip UAT |
| DaVinci flow to a sandbox (test) | Supported in PingOne native promotion; sandbox counts as a valid target env |
| Terraform-managed journey baseline | Export with `pingcli platform export`; manage with Terraform; promote via PR + apply |

---

## Related references

- `ping-foundation` → `references/curated/cross-platform/config-promotion.md` — model selection, topology, general constraints, and rollback
- `references/curated/pingone-st/journey-design-patterns.md` — journey design best practices before promoting
- `references/curated/pingone-mt/davinci-overview.md` — DaVinci flow concepts and versioning

---

## Source

- [AIC self-service promotions](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions.html)
- [AIC promotion FAQ](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions-faqs.html)
- [AIC configuration placeholders (ESVs)](https://docs.pingidentity.com/pingoneaic/tenants/configuration-placeholders.html)
- [PingOne configuration management](https://docs.pingidentity.com/pingone/early-access-features/ea-p1_promote.html)
