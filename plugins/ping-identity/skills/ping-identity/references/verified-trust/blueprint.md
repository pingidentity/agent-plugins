# Verified Trust Workforce Help-Desk Fulfillment Blueprint

## Overview

This blueprint describes a typical workforce help-desk outcome: verify that an employee is the person associated with an account before permitting an assisted recovery or another protected support action.

Verified Trust is a cross-product solution composition, not a standalone product. The documented implementations combine a host platform, an operator authentication and orchestration layer, and PingOne Verify for identity proofing. PingOne and PingOne Advanced Identity Cloud use different orchestration layers and must be designed as separate variants.

Use this page to decide **what** must be configured and **what** the agent, employee, and platform must accomplish. Use the owning product skill and current product documentation for **how** to create objects, change tenant settings, import assets, configure nodes, call APIs, or deploy a flow or journey.

## Scope

This blueprint covers:

- Help-desk operator authentication and authorization.
- Employee lookup or identity selection.
- Delivery of a verification request to the employee.
- Government-document, selfie, liveness, and face/document comparison checks through PingOne Verify.
- Operator-visible verification outcomes and controlled failure handling.
- Platform-specific continuation into recovery where the official implementation documents it.
- Critical configuration concepts, validation checkpoints, and implementation handoffs.

## Does not cover

This is not a product configuration runbook. It does not prescribe:

- API payloads, CLI commands, Terraform, SDK code, or exact tenant-mutation procedures.
- Product pricing, quotas, licensing, release state, or unsupported policy behavior.
- A universal account-reset implementation. The downstream action must be explicit for the selected platform and organization.
- Equivalent behavior between PingOne/DaVinci and AIC journeys.
- External-IdP support for AIC based on the PingOne example.
- PingOne Protect, PingOne Authorize, PingOne Credentials, PingOne Neo, or PingOne Recognize as required components unless a selected implementation documents them.

If the platform is not known, ask for it before selecting an orchestration layer. The cited solution guides do not establish an equivalent composition for Advanced Services, self-managed Advanced Identity Software, or Government Identity Cloud.

## Fulfillment contract

### Actors

| Actor | Responsibility |
|---|---|
| Platform administrator or implementer | Provides the host environment, policy, credentials, groups, flow/journey assets, and deployment context. |
| Help-desk operator | Authenticates, passes the authorization check, identifies the employee, starts the verification request, and reviews the result. |
| Employee | Receives the request and completes the identity-proofing transaction on a suitable device. |
| PingOne Verify | Evaluates the configured identity-proofing policy and returns transaction and verification outcomes. |
| Recovery or support system | Performs the approved downstream action only when it is explicitly configured for the selected platform. |

### Expected outcome

Success means that the employee is verified according to the selected Verify policy and that the configured downstream action is allowed. Sending a verification request, receiving a partial result, or recording a failed ticket is not by itself a successful recovery.

## Platform decision boundary

Select the variant before choosing product skills or execution surfaces.

| Environment signal | Variant and orchestration | Verification and outcome |
|---|---|---|
| PingOne environment with PingOne SSO, DaVinci, and the Verified Trust Marketplace flow | PingOne SSO authenticates the operator; DaVinci provides lookup, authorization, orchestration, and outcome handling. | PingOne Verify performs proofing. The documented flow returns a result; account reset is a separate action. |
| AIC tenant with journeys, backchannel processing, and a PingOne Worker Service | AIC journeys and backchannel journeys coordinate the operator, employee, verification, and recovery stages. | The Worker Service invokes PingOne Verify. The documented flow can continue to password or MFA-device recovery. |
| Platform not identified | Stop and request the platform. | Do not infer DaVinci, AIC journeys, or an equivalent composition. |
| Advanced Services, self-managed Advanced Identity Software, or Government Identity Cloud | Route to the selected platform reference first. | The cited Verified Trust guides do not establish a corresponding implementation. |

## Shared fulfillment lifecycle

Use this as the solution-level sequence, not as a node or screen prescription:

1. Confirm the host platform and the intended protected support outcome.
2. Authenticate the help-desk operator through the host platform.
3. Confirm that the operator is authorized for recovery or the protected support action.
4. Locate and match the intended employee using the platform-supported identity data.
5. Start a verification transaction and deliver the request through a supported channel.
6. Have the employee submit the required government identity document and live facial capture.
7. Evaluate document validity, liveness, facial comparison, and overall policy results.
8. Handle success, failure, timeout, cancellation, abandonment, and retry outcomes according to policy.
9. Continue only to the explicitly configured platform-specific recovery or support action.
10. Preserve enough transaction and flow/journey context for audit and support reconstruction.

The solution must define what the employee and operator see at each important outcome. Avoid silent retries, ambiguous bypasses, and messages that reveal unnecessary account or policy details.

## PingOne variant: DaVinci workforce help desk

See [PingOne Variant reference](blueprint-pingone.md).

## AIC variant: journey and backchannel workforce help desk

See [AIC Variant reference](blueprint-aic.md).

## Failure, recovery, and audit boundaries

Design these states before implementation:

| State | Required architectural handling |
|---|---|
| Verification success | Permit only the configured downstream support or recovery action. |
| Verification failure or inconclusive result | Show a controlled outcome, allow only policy-approved retry/escalation, and do not treat it as proof of identity. |
| Timeout, expired link, or expired backchannel | Define retry/restart behavior and avoid leaving the operator or employee in an unusable state. |
| Cancellation or abandonment | End or invalidate the attempt as appropriate and provide a clear next step. |
| Missing camera, unsupported document, or delivery failure | Provide a safe supported alternative or escalation path; do not silently bypass proofing. |
| Authorized operator with no recovery action configured | Return a clear incomplete-configuration outcome; do not imply that Verify performs the reset. |
| Failed verification ticket | Use Jira/ServiceNow only for the documented recording purpose; ticketing is not recovery. |

Capture or retain the identifiers and version context needed to correlate the operator, employee, verification transaction, result, and flow/journey version, subject to the organization’s privacy and retention requirements. Separate operational observability from storage of unnecessary identity-document or biometric data.

## Implementation handoffs

After selecting the platform, continue with the owning references for the **how**:

- [PingOne platform](../pingone/README.md) — host environment and service boundaries.
- [PingOne SSO](../pingone-sso/README.md) — operator sign-on and federation context.
- [PingOne DaVinci](../pingone-davinci/README.md) — flow orchestration and application launch context.
- [PingOne Verify](../pingone-verify/README.md) — proofing policy, transaction, channel, and outcome details.
- [Advanced Identity Cloud](../pingone-advanced-identity-cloud/README.md) — AIC tenant and journey-hosting context.

Select API, CLI, Terraform, MCP, or SDK execution surfaces only after the platform, product owner, and intent are known. This skill is an orientation and routing layer; it does not mutate a tenant.

## Verification checklist

Before calling the solution ready for a test or production handoff, confirm:

- The host platform and orchestration variant are explicit.
- Operator authentication and help-desk authorization are tested.
- Employee lookup/matching and the delivery channel are defined.
- The Verify policy is appropriate for the environment.
- Document, liveness, facial-comparison, and overall outcome paths are exercised.
- Failure, timeout, cancellation, retry, and escalation behavior is intentional.
- A downstream recovery or support action is explicitly configured; it is not inferred from proofing success.
- Optional external-IdP or ticketing paths are tested only when enabled and documented for the selected platform.
- Audit/support correlation and privacy/retention expectations are defined.
- Production rollout, policy, and rollback decisions are reviewed in the owning platform skill.

## Related references

- [Verified Trust solution overview](README.md)

## Source

- [Verified Trust overview](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-overview.html)
- [Verified Trust help desk with PingOne](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-pingone.html)
- [Verified Trust help desk with Advanced Identity Cloud](https://docs.pingidentity.com/solution-guides/verified-trust/verified-trust-helpdesk-aic.html)
- [PingOne external identity providers](https://docs.pingidentity.com/pingone/integrations/p1_external_idps.html)
- [PingOne Verify documentation](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_start.html)
- [AIC environment secrets](https://docs.pingidentity.com/pingoneaic/tenants/esvs.html)
