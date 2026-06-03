# Service Map

Maps Ping Universal Services and strategic shared services to platform context and owning skill.

## Universal Services

These services are consumed across PingOne MT and PingOne ST. They are not configuration destinations; they are capabilities invoked from within a platform.

| Service | Platform Context | Primary Skill | Notes |
|---|---|---|---|
| PingOne Protect | PingOne MT, PingOne ST via connector | ping-universal-services | Risk signals, adaptive auth, bot detection |
| PingOne Verify | PingOne MT, PingOne ST via connector | ping-universal-services | Identity verification, document check, liveness |
| PingOne Credentials | PingOne MT | ping-universal-services | Verifiable credentials, digital wallet |
| PingOne SSO | PingOne MT | ping-universal-services | Workforce SSO, app federation, SAML/OIDC |
| PingOne IGA | PingOne MT | ping-universal-services | Identity governance, access requests, certifications |
| PingOne Neo | PingOne MT | ping-universal-services | Decentralized identity |
| PingOne Authorize | PingOne MT | ping-universal-services | Fine-grained authorization, policy enforcement |

## Orchestration-Adjacent Services

These services are tightly coupled to orchestration. Route to ping-orchestration when the primary task is designing a flow that uses them.

| Service | Primary Skill | Notes |
|---|---|---|
| PingOne DaVinci | ping-orchestration | Flow builder, connector library, CIAM orchestration |
| PingOne ST Journeys / Trees | ping-orchestration | PingAM authentication trees, journey nodes |

## On-Premises Strategic Services

| Service | Primary Skill | Notes |
|---|---|---|
| PingAuthorize | ping-universal-services / ping-foundation | Policy engine; route based on whether task is setup or runtime invocation |
| PingDirectory | ping-foundation | Directory setup and admin; ping-app-integration for integration patterns |
| PingDataSync | ping-foundation | Data synchronization and provisioning config |
