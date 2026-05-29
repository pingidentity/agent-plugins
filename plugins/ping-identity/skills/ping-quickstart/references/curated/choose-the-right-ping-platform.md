---
title: "Choose the Right Ping Platform"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate", "pingaccess", "pingdirectory"]
capabilities: ["quickstart"]
audience: ["admin", "architect"]
use_cases: ["workforce", "customer", "cross-platform"]
doc_type: guide
status: current
canonical: true
last_updated: ""
slug: ""
---

# Choose the Right Ping Platform

Decision guide for selecting between PingOne MT, PingOne ST, and the Ping Software Suite.

## Scope

Covers: platform selection decision criteria.
Does NOT cover: configuration steps — see `ping-foundation`.

## Decision matrix

| Need | Best platform |
|---|---|
| New deployment, SaaS-managed, low ops overhead | PingOne MT |
| Deep customization, journey/tree orchestration, ForgeRock migration | PingOne ST |
| Existing on-prem or hybrid, PingFederate/PingAccess/PingDirectory | Ping Software Suite |
| CIAM with DaVinci orchestration | PingOne MT + DaVinci |
| Complex authentication trees and self-service | PingOne ST |
| Federation hub for enterprise apps | PingFederate (Software Suite) |
| API and application protection | PingAccess (Software Suite) |

## Key differentiators

**PingOne MT vs PingOne ST:**
- PingOne: SaaS console, simpler admin model, DaVinci for orchestration
- PingOne ST: Fully managed but highly configurable, journey/tree-based orchestration, advanced self-service

**Cloud vs Software Suite:**
- Cloud: Ping-managed infrastructure, subscription model
- Software Suite: Customer-managed infrastructure, traditional enterprise deployment

## Common patterns

- Workforce SSO with existing AD → PingFederate or PingOne MT SSO
- CIAM registration and login flows → PingOne ST or PingOne + DaVinci
- API gateway protection → PingAccess
- Directory as authoritative store → PingDirectory

## Related references

- `getting-started-overview.md`
- `common-starting-patterns.md`

## Source

[Ping Identity Solution Guides](https://docs.pingidentity.com/solution-guides/)
