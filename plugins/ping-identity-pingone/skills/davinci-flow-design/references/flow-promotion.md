# Promoting DaVinci Flows and Flow Policies Between Environments

DaVinci-specific concerns when promoting flows, flow policies, and connector configuration between PingOne environments. This is the DaVinci half of the orchestration promotion model; AIC journey promotion is a separate platform-native mechanism with different rules.

## Scope

**Covers:** What DaVinci flow promotion moves; flow versioning rules; flow-policy dependencies; sensitive promotion variables for connector credentials.
**Does NOT cover:** General promotion model choice, environment topology, Terraform/CaC pipeline, and cross-product config promotion — see the platform-native configuration and promotion model for those. AIC journey promotion (PingOne Advanced Identity Cloud).

---

## What moves via native PingOne promotion

**Moves:**
- Flow definitions — **most recently deployed version only** (not all versions; if you have 4 versions and version 3 is the most recently deployed, only version 3 promotes)
- Flow policies (with their referenced flow versions auto-included as dependencies)
- Connector configuration structure (connection IDs and non-secret settings) — **exception: LDAP gateway credentials cannot be promoted or managed using promotion variables** and must be manually configured in each environment

**Does not move:**
- Live user sessions
- User-created or self-registered applications
- MFA device enrollments
- User profile data

**Connector credentials do not move directly.** PingOne gates promotion of any attribute marked sensitive (client secrets, API keys, passwords embedded in connector config) — the promotion cannot proceed until a **sensitive promotion variable** exists for each blocked attribute. Variables are created in the *source* environment with the target-specific value specified at that point; the connector structure is then promoted and resolves to those target values at promotion time, not the source's.

---

## Flow versioning rule

Each DaVinci flow has multiple versions; only the **most recently deployed version** is promoted to the target environment. Ensure the correct version is deployed before triggering a promotion.

---

## Flow-policy dependency

Flow policies reference specific flows and specific versions of those flows. **Promote the flow policy** — the promotion service then auto-includes the referenced flow versions as dependencies. If you promote a flow independently without also promoting its flow policy, the policy in the target environment may reference a different version than the one you promoted.

---

## Sensitive promotion variables for connector credentials

In DaVinci, connector credentials (client secrets, webhook URLs, API keys) are environment-specific. PingOne auto-detects sensitive attributes and requires **sensitive promotion variables** before the promotion can proceed:

1. When you select a connector config resource for promotion, PingOne identifies sensitive attributes and auto-selects them as requiring variables — you cannot clear this.
2. In the **source environment**, create a sensitive promotion variable for each blocked attribute and specify the target environment's value at that point.
3. The promotion proceeds; the connector resolves to those target values after promotion, not the source's.

---

## Prerequisites

- Promotion Admin role (PingOne) or environment admin in both environments
- DaVinci flow promotion variables assigned in the target before promotion

---

## Common variants

| Variant | Notes |
|---|---|
| Flow to a sandbox (test) environment | Supported in PingOne native promotion; sandbox counts as a valid target env |
| Terraform-managed flow baseline | Manage with the PingOne Terraform provider; promote via PR + apply |

---

## Related references

- `flow-model.md` — DaVinci versioning concepts (Save/Deploy/Try/Revert)

---

## Source

- [PingOne configuration management](https://docs.pingidentity.com/pingone/early-access-features/ea-p1_promote.html)
- [PingOne DaVinci API](https://developer.pingidentity.com/pingone-api/davinci/introduction.html)
