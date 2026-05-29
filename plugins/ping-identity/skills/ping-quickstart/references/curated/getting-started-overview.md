---
title: "Getting Started with Ping Identity"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate"]
capabilities: ["quickstart"]
audience: ["admin", "developer"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: ""
slug: ""
---

# Getting Started with Ping Identity

Orientation anchor for new users and inherited deployments. Covers the three primary platform families and the right entry point for each.

## Scope

Covers: which platform to use, what to set up first, and how to get your bearings.
Does NOT cover: detailed configuration steps — see `ping-foundation` for those.

---

## The three platform families

| Platform | When to use it | Admin entry point |
|---|---|---|
| PingOne MT | SaaS-hosted identity for new cloud-first deployments | apps.pingone.com |
| PingOne ST | Fully managed, highly customizable identity cloud (ForgeRock lineage) | Your PingOne ST tenant URL |
| Ping Software Suite | On-premises or self-managed: PingFederate, PingAccess, PingDirectory | Deployed server admin consoles |

---

## Setup sequence by platform

**PingOne MT:**
- Create or access a PingOne environment
- Add an application and connect a directory or identity provider
- Configure a sign-on policy and assign it to the app

**PingOne ST:**
- Access the PingOne ST tenant; verify `alpha` and `bravo` realms
- Configure the realm identity store
- Register an OAuth 2.0 / OIDC or SAML application
- Create or activate an authentication journey

**Ping Software Suite:**
- Identify which products are deployed (PingFederate, PingAccess, PingDirectory)
- Configure data stores, adapters, and connections for each product
- Test federation or access control before opening to users

---

## Related references

- `choose-the-right-ping-platform.md`
- `common-starting-patterns.md`

## Source

[Ping Identity Documentation](https://docs.pingidentity.com)
