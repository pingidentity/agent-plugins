# PingOne Identity Governance

## Overview
PingOne Identity Governance is a framework for centrally administering identities and resource access in line with organizational, regulatory, and security policies. It helps organizations reduce security exposure and unauthorized access while making compliance activities more efficient.

## Core Concepts
- **Access requests and approvals:** Self-service application-access requests with approval workflows give people a governed way to obtain access.
- **Access reviews:** Periodic manager reviews support confirming or removing team-member access.
- **Lifecycle automation:** Automated onboarding, birthright access, and offboarding align access with identity lifecycle events.
- **Segregation of duties:** Controls help prevent risky combinations of permissions.
- **Audit, delegation, and recommendations:** Activity records, reporting, delegated administration of users and entitlements, and machine-learning recommendations based on peer access patterns support oversight and informed decisions.

## When to use
- Use it for workforce identity governance requiring governed access requests, reviews, lifecycle processes, or audit reporting.
- Use it when access decisions must reflect organizational, regulatory, or security policies.

## When not to use
- Do not configure it in the Bravo realm; it does not recognize realms and requires delegated administration, which Bravo does not support.
- For workforce governance, prefer a dedicated Alpha-only Advanced Identity Cloud tenant; plan CIAM separately according to the application.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingoneaic/identity-governance/administration/getting-started-what-is-iga.md)
