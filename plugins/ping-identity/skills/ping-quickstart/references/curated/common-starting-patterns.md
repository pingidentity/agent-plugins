---
title: "Common Starting Patterns"
product_family: cross-platform
products: ["pingone", "pingone-st", "pingfederate"]
capabilities: ["quickstart"]
audience: ["admin", "developer", "architect"]
use_cases: ["workforce", "customer"]
doc_type: guide
status: current
canonical: true
last_updated: ""
slug: ""
---

# Common Starting Patterns

The most frequent starting scenarios and which skills and platforms to use for each.

## Scope

Covers: the top 6 starting patterns and their routing.
Does NOT cover: step-by-step configuration — see `ping-foundation` or the relevant capability skill.

## Pattern 1: Employee SSO to cloud apps

**Platform:** PingOne MT or PingFederate
**Skill:** `ping-foundation` → `pingone-mt` or `ping-software/pingfederate`
**First step:** Add app connection; configure SAML or OIDC

## Pattern 2: Customer registration and login (CIAM)

**Platform:** PingOne ST (journey-based) or PingOne + DaVinci
**Skill:** `ping-foundation` for setup; `ping-orchestration` for flow design
**First step:** Create environment; configure registration journey or DaVinci flow

## Pattern 3: Add MFA to an existing deployment

**Platform:** Any — PingOne, PingOne ST, or PingFederate + PingID
**Skill:** `ping-foundation` for MFA policy setup; `ping-universal-services` for PingOne Protect/risk-based step-up
**First step:** Configure authentication policy to require MFA

## Pattern 4: Protect an API or web app

**Platform:** PingAccess (Software Suite) or PingOne + app integration
**Skill:** `ping-foundation` → `ping-software/pingaccess`; or `ping-app-integration` for SDK patterns
**First step:** Define a protected resource and configure agent/gateway

## Pattern 5: Migrate from ForgeRock / legacy deployment

**Platform:** PingOne ST
**Skill:** `ping-foundation` → `pingone-st`
**First step:** Provision PingOne ST tenant; migrate realms and trees

## Pattern 6: Add identity verification (KYC)

**Platform:** PingOne + PingOne Verify
**Skill:** `ping-universal-services` → `verify` branch
**First step:** Enable PingOne Verify in environment; invoke from policy or DaVinci flow

## Related references

- `getting-started-overview.md`
- `choose-the-right-ping-platform.md`
