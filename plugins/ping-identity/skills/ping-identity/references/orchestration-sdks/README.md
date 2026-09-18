# Ping Orchestration SDKs

## Overview
Ping Orchestration SDKs embed authentication and registration in applications. They connect apps to DaVinci flows, Advanced Identity Cloud or PingAM journeys, and OIDC authorization servers.

## Core Concepts
- **DaVinci:** Runs server-driven flows while the app renders requested inputs, supporting flow changes without republishing where applicable.
- **Journeys:** Advances Advanced Identity Cloud or PingAM authentication journeys and callbacks while the app controls each step’s interface.
- **OIDC sign-on:** Uses browser-based OpenID Connect with PingOne, Advanced Identity Cloud, PingAM, PingFederate, or another conforming server.
- **Cross-platform modules:** Supports Android, iOS, JavaScript, and React Native, with availability varying by orchestration approach.
- **Sessions and tokens:** Coordinates protocol exchanges, OAuth 2.0 tokens, sessions, and secure handling.

## When to use
- Embed centrally managed authentication, registration, MFA, or risk decisions in mobile, web, or React Native applications.
- Keep supported server-side flow or journey changes independent of client republishing.

## When not to use
- For direct calls to individual PingOne services, use the relevant standalone PingOne SDK.
- For MFA, Verify, or Credentials outside orchestration, use the dedicated SDK or direct REST API.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://developer.pingidentity.com/orchsdks/index.md)
