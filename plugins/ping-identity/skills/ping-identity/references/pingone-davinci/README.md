# PingOne DaVinci

## Overview
PingOne DaVinci is an orchestration platform for identity and access management user journeys. It helps organizations build guided processes such as registration and authentication with reusable integrations and decision logic.

## Core Concepts
- **Flows** model journeys as connected paths of nodes, allowing progress to follow decisions and collected information.
- **Nodes and operators** perform actions and control branching based on predecessor outcomes.
- **Connectors** provide reusable processing logic and integrations with Ping Identity and external services; their capabilities become flow steps.
- **Applications and flow policies** expose permitted flows or versions through redirects, widgets, APIs, OIDC, or SAML 2.0, including traffic distribution for testing.
- **Variables** retain values at company, flow, flow-instance, or user scope.
- **Versioning is deploy-gated:** Flow editing is separate from deployment — changes are saved and testable in the studio, but end users see them only after the flow version is deployed; earlier deployed versions continue to serve traffic until replaced.
- **Subflows as shared components:** Common logic (MFA, risk evaluation, email verification) is factored into subflows reused across flows; a subflow must define both a success and a failure path that the parent flow handles explicitly.

## When to use
- Build registration, authentication, or other journeys combining user interaction and backend processing.
- Integrate journeys into web, native, or PingFederate applications using a suitable launch pattern.
- Reuse configured service integrations across flows.

## When not to use
- For connector-specific capabilities, consult the DaVinci connector documentation.
- If the application needs DaVinci-provided screens, prefer a widget or redirect rather than API integration.
- If the application must own the complete experience and returned-data handling, use API integration with that responsibility explicitly assigned to the application.

## Gotchas
- **Token exchange from a DaVinci flow to PingOne OIDC** requires the DaVinci connector to be configured with the correct environment ID and client credentials — mismatches fail obscurely at runtime.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/davinci/davinci_introduction.md)
