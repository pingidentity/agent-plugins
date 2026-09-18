# PingAuthorize

## Overview
PingAuthorize provides centralized, fine-grained authorization through dynamic, runtime decisions. It helps organizations control access to data and actions using transaction context, attributes, consent, entitlements, resources, and environmental information.

## Core Concepts
- **Attribute-based authorization:** Policies combine runtime attributes and processed values for context-aware decisions.
- **Policy Editor:** Teams create and validate fine-grained data-access policies that can permit, reject, filter, or transform resource data.
- **PingAuthorize Server:** The server enforces policies for application resources, APIs, microservices, LDAP directories, and relational databases.
- **Enforcement patterns:** PDP APIs, reverse-proxy or sideband gateways, and the built-in SCIM service support different access arrangements.
- **Decision placement:** External PDP decisions support development and testing; embedded PDP policies support pre-production and production deployments.

## When to use
- Apply attribute-driven authorization to APIs, applications, or structured data.
- Protect REST traffic through a gateway or expose governed external-store data through SCIM.
- Let applications request authorization decisions through PDP APIs.

## When not to use
- Redirect identity-lifecycle or authentication requirements to the applicable Ping Identity capability.
- Confirm licensing and architecture requirements before selecting a deployment pattern.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingauthorize/11.1/paz_introduction.md)
