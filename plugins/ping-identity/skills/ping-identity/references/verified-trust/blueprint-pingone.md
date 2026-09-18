# Verified Trust - PingOne variant: DaVinci workforce help desk

## Composition

The documented PingOne composition uses:

- **PingOne SSO** for help-desk operator sign-on.
- **PingOne DaVinci** for the parent flow, user lookup, group authorization, verification orchestration, and result handling.
- **PingOne Verify** for government-document and live-face identity proofing.
- **PingOne application integration** to provide the supported flow launch path.

The Marketplace package supplies the documented parent flow and verification evaluation subflow. The flow can return a verification result, but it does not automatically reset the employee account.

## Critical configuration concepts

| Concern | Required concept |
|---|---|
| Flow assets | The Verified Trust for Workforce Help Desk solution package and its parent/evaluation flow structure. |
| DaVinci-to-PingOne access | The PingOne DaVinci Connection Environment ID, Client ID, and Client Secret must be available to the Verify connector configuration. |
| Proofing policy | A Verify policy ID is supplied to the flow. The default policy is suitable for testing; production requires an organization-appropriate policy. |
| Operator authorization | A PingOne group identifies help-desk operators allowed to perform the protected action. |
| Deployment and launch | The flow is deployed and launched through the configured PingOne DaVinci Connection application sign-on path, not an ad-hoc flow test path. |
| Downstream outcome | Account reset or another support action is configured separately from the proofing result and application response. |

## Optional PingOne variants

- An external identity provider can replace the normal end-user lookup path in the documented PingOne flow. The operator still authenticates through PingOne, and the external result must provide the user data required by the verification flow.
- Jira or ServiceNow can record verification failures when their connectors and failure-path settings are configured. Ticket creation does not perform account recovery.

Do not generalize these optional variants to AIC without separate supporting documentation.
