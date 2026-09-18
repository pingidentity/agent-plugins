# Researching a PingFederate–PingOne Credentials integration

## Scope

Use this as a focused research brief for a **PingFederate-hosted or adjacent application** that uses **PingOne Credentials**. PingOne Credentials manages issuer-side digital-credential resources and documented issuance, wallet, and verification capabilities; PingFederate remains a federation and authentication-policy platform. This brief does not assume a native PingFederate Credentials adapter or Integration Kit.

### Covers

- **Administrative/interface plane:** PingFederate transaction and application ownership, PingOne Credentials organization and environment, issuer and credential-profile ownership, wallet or verifier responsibility, protocol and launch surface, credentials, trust material, and promotion dependencies.
- **Runtime/credential plane:** issuance, wallet pairing or presentation, verification evidence, and the handoff from a credential transaction to a PingFederate authentication policy or host application when the selected architecture documents that relationship.

### Does NOT cover

- Tenant mutations, credential authoring procedures, API payloads or schemas, wallet SDK code, executable DaVinci flows, connector configuration, exact credentials, or installation commands.
- A claim that PingFederate is a PingOne Credentials issuer, wallet, verifier, native adapter, or Integration Kit host. Current product documentation must establish any such contract; otherwise treat the relationship as an external application or protocol handoff.
- A claim that a credential, presentation, or verification result automatically authenticates a user, performs MFA, authorizes an application, issues a PingFederate token, or provisions an account.
- PingOne Neo, AIC journeys, PingOne DaVinci implementation, or generic PingFederate federation configuration except as boundary handoffs.

Treat this as orientation, not configuration authority. Confirm current PingOne Credentials, wallet, verifier, protocol, PingFederate, and any selected application or connector documentation for the target release.

## Research brief

Research two connected planes:

- **Administrative/interface plane:** identify the PingFederate deployment and transaction, the PingOne Credentials organization and environment, issuer and credential-profile ownership, wallet or verifier application, DID and trust responsibilities, selected issuance or presentation protocol, service identities, signing keys, redirect or callback endpoints, and promotion or monitoring ownership. The current product references describe APIs, wallet SDKs, Credentials Connector, and Marketplace surfaces; do not infer a PingFederate-native adapter from those resources.
- **Runtime/credential plane:** determine whether the transaction issues a credential, pairs a wallet, requests a presentation, verifies evidence, or manages credential lifecycle; where the wallet or verifier runs; how evidence or a result reaches the PingFederate-hosted application; and which authentication-policy or application branch interprets success, failure, retry, expiry, or revocation. A credential result is evidence for a host decision, not automatically a federation or authorization result.

A common documented lifecycle is: establish the issuer, credential profile, wallet or verifier, and trust/protocol boundary; initiate the selected issuance or presentation interaction through the documented application, API, connector, or wallet surface; receive and validate the documented result; and let the host application or PingFederate transaction continue, retry, review, or stop. Exact protocol messages, wallet behavior, proof requirements, callbacks, status values, and trust semantics are surface- and release-sensitive.

## Resource index

### PingOne Credentials and wallet surfaces

- [PingOne Credentials overview](https://docs.pingidentity.com/pingone/digital_credentials_using_pingone_credentials/p1_credentials_start.html)
- [PingOne Credentials introduction](https://docs.pingidentity.com/pingone/digital_credentials_using_pingone_credentials/p1_credentials_introduction.html)
- [Credentials API](https://developer.pingidentity.com/pingone-api/credentials/introduction.html)
- [PingOne wallet native SDKs](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-neo-native-sdks/pingone-wallet-native-sdks.html)
- [PingOne Credentials Connector](https://docs.pingidentity.com/connectors/p1_credentials_connector.html)
- [PingOne Credentials reference](../pingone-credentials/README.md)
- [PingOne Credentials integration research](../pingone/blueprint-integrating-pingone-credentials.md)

### PingFederate host and handoffs

- [PingFederate reference](README.md)
- [PingFederate authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_authentication_policies.html)
- [PingFederate IdP adapters](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_managing_idp_adapters.html)
- [PingOne Neo reference](../pingone-neo/README.md)
- [PingOne DaVinci reference](../pingone-davinci/README.md)
- [Orchestration SDKs reference](../orchestration-sdks/README.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product and role boundary | Is the request for credential issuance, wallet pairing, credential presentation, verification, or lifecycle management? Which PingFederate transaction and application are in scope? | Do not treat PingFederate, PingOne Credentials, PingOne Neo, a wallet, and a verifier as interchangeable roles. |
| Issuer and credential readiness | Which organization, environment, issuer, credential profile, signing key, notification, and population are required? | Verify issuer state, credential rules, key ownership, entitlement, environment, and promotion requirements. |
| Wallet, verifier, and trust | Which wallet or verifier receives or requests the credential? Which DID, trust registry, presentation protocol, proof, and user-consent rules apply? | Check current wallet, verifier, OID4VCI/OID4VP, DIF, and trust documentation; distinguish documented behavior from inference. |
| PingFederate host surface | Is PingFederate directly invoking a documented Credentials integration, or is a separate web, mobile, API, DaVinci, or connector application involved? | Current product references do not by themselves establish a native PF adapter or Integration Kit. Fail closed when the host contract is unclear. |
| Runtime and result handoff | What issuance, presentation, verification, expiry, revocation, or error result reaches the host? Which PingFederate policy or application branch handles it? | A credential result does not automatically authenticate, authorize, issue tokens, or provision an account. |
| Credentials and network | Which application, API client, connector, wallet, callback, key, endpoint, and secret owners participate? | Verify scopes, roles, rotation, redirect values, certificate trust, regional endpoints, and least privilege. |
| Promotion and operations | What issuer resources, profiles, keys, wallet bindings, verifier configuration, endpoints, templates, policies, and audit evidence move or must be recreated? | Recheck target environment, trust material, privacy, monitoring, expiry/revocation behavior, and drift. |

## Guardrails and report

Keep these distinctions visible:

- PingOne Credentials is an issuer-side and credential-lifecycle service with wallet and verifier surfaces; PingFederate is the federation and authentication-policy host. The current documented product surfaces do not establish a native PF Credentials adapter or Integration Kit.
- Issuer resources, credential profiles, signing keys, wallet applications, verifier policies, DIDs, trust material, connector bindings, and PingFederate policies are distinct dependencies. A created credential or successful proof does not prove host readiness.
- Direct API, Credentials Connector, wallet SDK, DaVinci, and a PingFederate-hosted application can have different credentials, protocol messages, consent, callbacks, and lifecycle behavior.
- Do not infer storage, presentation, verification, revocation, supported protocols, trust semantics, token claims, or PingFederate policy mappings from an issuer or SDK resource.
- Do not treat an active issuer, paired wallet, successful presentation, configured policy, or installed client as proof that credentials, trust, redirect, privacy, monitoring, and operational ownership are production-ready.

Report: (1) the PingFederate, issuer, wallet, verifier, and protocol boundary; (2) verified issuer, credential, trust, key, credential, and network readiness; (3) documented issuance or presentation behavior and selected surface; (4) wallet/verifier result handling and PingFederate or application policy mapping; (5) promotion, operations, privacy, and unresolved checks; (6) documented facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingFederate reference](README.md), [PingOne Credentials reference](../pingone-credentials/README.md), [PingOne Neo reference](../pingone-neo/README.md), [DaVinci reference](../pingone-davinci/README.md), or current official documentation. Do not turn the report into a configuration runbook.
