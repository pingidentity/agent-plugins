# Promoting AIC Journeys, Scripts, and Themes Between Environments

AIC-specific concerns when promoting journeys, scripts, themes, and AM service configuration between tenant instances. This is the AIC half of the orchestration promotion model; DaVinci flow promotion is a separate platform-native mechanism with different rules.

## Scope

**Covers:** What AIC promotion moves and doesn't move; ESV and script gotchas; environment lock impact; sequential pair routing; per-node promotion considerations; journey rollback; native-promotion-vs-Terraform choice for AIC work.
**Does NOT cover:** Environment topology, Terraform/CaC pipeline design, and cross-product configuration promotion — use the platform-native configuration and promotion model for those. DaVinci flow promotion (PingOne multi-tenant).

---

## What AIC promotion moves

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

## Environment lock impact

AIC requires an **environment lock** on both source and target during a promotion.

| During lock | Effect |
|---|---|
| End-user authentication flows | **Unaffected** — runtime auth continues |
| AIC admin console | Read-only; most writes blocked in the source (dev) environment |
| ESV API | Blocked in both locked environments (source and target) during promotion |
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

## Rollback

If a promoted journey causes issues in the upper environment, AIC self-service rollback restores the prior static config set:

- **Trigger:** `POST /promotions/{promotionId}/rollback` (API only; admin console does not expose rollback)
- **Behaviour:** The upper environment's journey/script set is restored to its pre-promotion state. In-flight sessions on the promoted journey are not interrupted — they continue against the current version in memory until they time out.
- **After rollback:** Diagnose the issue in the source (dev) environment, fix, and re-promote.

---

## Choosing native promotion vs Terraform for AIC journey work

| Scenario | Typical fit | Why |
|---|---|---|
| AIC journey iteration within one tenant chain | AIC self-service promotions | Platform-provided self-service path; admin-console-driven; sequential pairs enforced by the platform (dev→staging→production only) |
| Multi-org, multi-cloud, or Git-backed audit trail needed | Ping CLI + Terraform | Terraform providers cover PingFederate, PingDirectory, and PingOne; Ping CLI CRUD for PingFederate is still rolling out — check the [compatibility matrix](https://developer.pingidentity.com/pingcli/latest/product-compatibility.html); state tracking and drift detection via Terraform |
| Mixed AIC journeys + DaVinci flows in the same pipeline | Can combine both | Each platform's native model handles its own config; Terraform manages cross-product baseline |

---

## Prerequisites

- AIC tenant admin access in both environments
- All ESVs referenced in journey config must be pre-created in the target environment
- All dependent inner journeys or scripts co-included in the promotion

---

## Common variants

| Variant | Notes |
|---|---|
| Standard dev/staging/prod chain | Sequential pairs; ESVs pre-configured in each upper env |
| With UAT tier | dev → UAT → staging → production; cannot skip UAT |
| Terraform-managed journey baseline | Manage with Ping Identity Terraform providers; promote via PR + apply |

---

## Related references

- `references/design-notes.md` — journey design review before promoting
- `references/nodes/utility-nodes.md` — ESV usage in Scripted Decision nodes

---

## Source

- [AIC self-service promotions](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions.html)
- [AIC promotion FAQ](https://docs.pingidentity.com/pingoneaic/tenants/self-service-promotions-faqs.html)
- [AIC configuration placeholders (ESVs)](https://docs.pingidentity.com/pingoneaic/tenants/configuration-placeholders.html)
