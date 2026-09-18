# Researching a PingFederate–PingOne Protect integration

## Scope

Use this as a focused research brief for **PingFederate** and **PingOne Protect**. The integration boundary is a federation and authentication transaction handled by PingFederate, with Protect providing risk information for an authentication-policy decision.

### Covers

- **Administrative/interface plane:** PingFederate and Protect licensing, Integration Kit and version compatibility, IdP Adapter and Provider/SDK roles, policy and adapter ownership, regional endpoint reachability, and deployment or promotion dependencies.
- **Runtime/client plane:** transaction and device-profile collection, Protect evaluation, risk information returned to PingFederate, authentication-policy routing, step-up or mitigation behavior, and transaction completion or feedback boundaries.

### Does NOT cover

- Tenant mutations, Integration Kit installation commands, adapter or policy field values, API/CLI/Terraform commands, SDK code, exact credentials or regional values, or executable authentication policies.
- PingOne platform-native/DaVinci, Advanced Identity Cloud, or self-managed PingAM implementation. Those paths have separate product boundaries.
- An assumption that a risk result automatically performs MFA, denies access, or changes a PingFederate policy. The host authentication policy owns the documented response.

Treat this as orientation, not an installation or administration guide. Confirm current product and kit documentation for the target release.

## Research brief

Research two connected planes:

- **Administrative/interface plane:** identify the PingFederate deployment and version, the applicable Protect or legacy Risk Integration Kit, the PingOne organization/environment and entitlement, the adapter/provider arrangement, authentication-policy owner, credential and secret boundary, and outbound HTTPS requirements. The current Protect Integration Kit documentation describes an IdP Adapter that communicates with Protect and a Protect Provider/SDK that can work with the HTML Form adapter; these surfaces may be used independently or together. The exact supported arrangement is release-sensitive.
- **Runtime/client plane:** determine where device profiling or client-side Signals are collected, when the transaction is sent to Protect, and how the returned risk assessment and transaction information are exposed to PingFederate. The authentication policy then maps the result to the required authentication treatment. Device profiling, authentication API versus widget behavior, and whether the Provider executes for a given policy path must be verified for the kit and release in scope.

The documented high-level lifecycle is: collect sign-on transaction context and optional device profile; submit it through the Integration Kit surface; receive a Protect risk assessment and related transaction information; branch the PingFederate authentication policy; complete, step up, or stop the transaction; and preserve the resulting operational evidence. The exact callback, failure, retry, and terminal-feedback behavior must be taken from the current kit and PingFederate references rather than inferred from a policy diagram.

## Resource index

### Protect and Integration Kit

- [PingOne Protect Integration Kit](https://docs.pingidentity.com/integrations/pingone/pingone_protect_integration_kit/pf_p1_protect_ik.html)
- [Protect Integration Kit device profiling](https://docs.pingidentity.com/integrations/pingone/pingone_protect_integration_kit/pf_p1_protect_ik_integrating_device_profiling.html)
- [PingOne Protect overview](https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_overview.html)
- [PingOne Protect API](https://developer.pingidentity.com/pingone-api/protect/introduction.html)
- [PingOne Signals SDK](https://developer.pingidentity.com/pingone-api/native-sdks/pingone-risk-sdks/risk_evaluation_sdk.html)
- [Legacy PingOne Risk Integration Kit](https://docs.pingidentity.com/integrations/pingone/pingone_risk_integration_kit/pf_p1_risk_ik_integrating_device_profiling.html) — release-sensitive comparison only.

### PingFederate administration and handoffs

- [PingFederate reference](README.md)
- [PingFederate IdP adapters](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_managing_idp_adapters.html)
- [PingFederate authentication policies](https://docs.pingidentity.com/pingfederate/latest/administrators_reference_guide/pf_authentication_policies.html)
- [PingFederate Protect reference](../pingone-protect/README.md)
- [Developer tools handoff](../developer-tools/README.md)

## Research matrix

| Area | Research questions / findings to extract | Qualify or verify |
|---|---|---|
| Product boundary | Which PingFederate deployment, population, protocol, and sign-on transaction are in scope? Which Protect or Risk kit matches the release? | Confirm supported versions and kit lifecycle; do not combine legacy and current guidance. |
| Administrative readiness | Is the Protect entitlement present? Are adapter/provider assets, policy ownership, credentials, and outbound regional endpoints ready? | Verify target environment, firewall, certificate, secret, and licensing requirements. |
| Component topology | Is the design IdP Adapter only, Provider/SDK with HTML Form adapter, or a documented combination? Where is device profiling performed? | Use current kit documentation; do not infer component ordering from names. |
| Runtime | What transaction, device, identity, and session data is available before evaluation? What risk assessment and prior-transaction information returns? | Check kit and PingFederate release; distinguish documented output from inferred policy input. |
| Decision handling | How does the authentication policy map risk to normal authentication, step-up, mitigation, retry, or stop? | Thresholds, action mappings, and failure behavior are policy- and tenant-specific. |
| Completion and operations | What counts as a completed transaction, and what evidence is retained for audit and tuning? | Verify callback/feedback semantics, logs, monitoring, and privacy requirements. |
| Promotion | Which adapter/provider assets, policies, credentials, templates, scripts, endpoints, and Protect-side settings move or must be recreated? | Revalidate release, secrets, bindings, regional endpoints, and drift in the target. |

## Guardrails and report

Keep these distinctions visible:

- PingFederate is the federation and authentication policy engine; PingOne Protect supplies risk information. Protect does not replace PingFederate’s authentication policy or credential validation.
- The IdP Adapter, Protect Provider/SDK, HTML Form adapter, and device-profile templates are distinct integration components. A design must state which are in scope and which release supports them.
- Device profiling and risk evaluation may involve client-side collection and server-side transaction context. Successful signal collection does not prove that policy, credentials, endpoint reachability, or risk interpretation is correct.
- Risk thresholds, recommended actions, failure routing, transaction status values, and kit field names are release-sensitive or tenant-specific. Preserve conflicts and verify the target release.
- Promotion must account for both PingFederate assets and PingOne Protect state; moving an authentication policy does not by itself reproduce credentials, endpoints, Protect policies, or operational evidence.

Report: (1) the PingFederate transaction and kit boundary; (2) verified administrative, version, credential, and network readiness; (3) documented adapter/provider and runtime behavior; (4) policy decision, step-up, failure, and completion handling; (5) promotion and unresolved checks; (6) facts versus inference, tenant-specific observations, and release-sensitive claims; and (7) the appropriate handoff to the [PingFederate reference](README.md), [PingOne Protect reference](../pingone-protect/README.md), current Integration Kit documentation, or [developer tools](../developer-tools/README.md). Do not turn the report into an installation or policy-authoring runbook.
