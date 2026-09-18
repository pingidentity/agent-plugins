# Verified Trust - AIC variant: journey and backchannel workforce help desk

## Composition

The documented AIC composition uses:

- **AIC main and backchannel journeys** for operator authentication, employee interaction, verification coordination, and recovery continuation.
- **PingOne Worker Service** for the AIC-to-PingOne service connection used by the verification flow.
- **PingOne Verify** for identity proofing.
- **AIC journey assets** such as custom nodes, scripts, email templates, and user attributes required by the documented solution.

This is an AIC journey implementation. Do not substitute a DaVinci flow for the AIC journey and backchannel layer.

## Critical configuration concepts

| Concern | Required concept |
|---|---|
| Tenant and service relationship | An AIC development tenant is mapped to a PingOne environment with Verify available. |
| Worker identity | A Worker application supplies the client ID, client secret, and PingOne environment ID needed by the Worker Service. |
| Secret handling | Worker credentials are held through AIC environment-specific secrets/ESVs and referenced by the Worker Service rather than embedded in journey content. |
| Service endpoints | The Worker Service uses the appropriate regional PingOne API and authentication endpoints. |
| Proofing policy | The verification journey references the intended Verify policy ID and Worker Service. |
| Journey dependencies | Main, verification backchannel, password-reset, and MFA-reset journeys are imported/configured with their required scripts, custom nodes, templates, and user attributes. |
| Operator authorization | A `HelpDesk` group or equivalent authorization condition gates the main journey. |
| Backchannel/session behavior | Main and verification journeys use the documented session and audience behavior; backchannel wait limits must cover the expected proofing interaction. |
| Downstream outcome | After successful proofing, the documented journey can continue to password or MFA-device recovery. Failure and expiration require an explicit retry or restart path. |

The exact node names, attribute schema, ESV names, endpoint values, import order, and timeout settings belong to the current AIC solution guide and the downstream AIC journey/platform skills. Treat them as environment- and release-sensitive configuration, not universal values.
