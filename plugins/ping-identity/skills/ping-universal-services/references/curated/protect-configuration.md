---
title: "PingOne Protect — Risk Predictors and Policy Configuration"
product_family: cross-platform
products:
  - pingone-protect
  - pingone-davinci
  - pingone-aic
capabilities:
  - universal-services
services:
  - protect
audience:
  - architect
  - admin
use_cases:
  - customer
  - workforce
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_overview.html"
---

# PingOne Protect — Risk Predictors and Policy Configuration

How to configure PingOne Protect risk predictors, build risk policies, and integrate the Signals SDK — the configuration layer that precedes flow invocation.

## Scope

**Covers:** Risk predictor types, license tier differences (PingOne Risk vs PingOne Protect), risk policy types (Standard/Targeted), predictor score configuration, Signals SDK requirements, and the PingID Device Trust predictor for workforce deployments.

**Does NOT cover:** How flows invoke Protect at runtime — see `references/curated/service-invocation-patterns.md`. Cross-platform usage constraints — see `references/curated/cross-platform-service-usage.md`.

---

## License tiers

| License | Predictors available |
|---|---|
| **PingOne Risk** (subset — included with MFA license) | Anonymous network detection, Geovelocity anomaly, IP reputation, IP velocity, New device, User-based risk behavior, User location anomaly, User velocity |
| **PingOne Protect** (full) | All PingOne Risk predictors + Bot detection, Suspicious device, AitM, Email reputation, Traffic anomaly, PingID device trust |

To access the full predictor set, a PingOne Protect license is required. Contact your account team to upgrade from PingOne Risk.

---

## Risk predictors

Every PingOne Protect environment includes one default instance of each supported predictor type. Additional instances can be added (e.g., two User Location Anomaly predictors with different radius settings for different user populations).

| Predictor | Description | License |
|---|---|---|
| Adversary-in-the-Middle (AitM) | Detects reverse-proxy attacks where a malicious actor intercepts credentials mid-flow | Protect |
| Anonymous network detection | Detects requests from VPNs, Tor, and unknown proxies; configurable allow-list for legitimate VPN users | Risk + Protect |
| Bot detection | Detects non-human activity including AI automation, CUAs (computer-using agents), automated frameworks, and recorders; identifies specific agent types in the response | Protect |
| Email reputation | Assesses the risk level of the email address used in the authentication | Protect |
| Geovelocity anomaly | Detects physically impossible travel between two sign-on locations | Risk + Protect |
| IP reputation | Assesses the reputation of the client IP address | Risk + Protect |
| IP velocity | Detects an unusual number of authentication attempts from a single IP | Risk + Protect |
| New device | Detects a device not previously seen for the user | Risk + Protect |
| PingID device trust | Requires PingID Device Trust agent on managed workstations; adds device compliance state (TRUST_VERIFIED / TRUST_VERIFICATION_FAILED) | Protect (Workforce only) |
| Suspicious device | Detects device characteristics associated with suspicious activity | Protect |
| Traffic anomaly | Detects unusual authentication volume patterns | Protect |
| User-based risk behavior | Machine-learning model trained on the user's own historical sign-on patterns | Risk + Protect |
| User location anomaly | Detects sign-on from an unusual location for the user; configurable radius | Risk + Protect |
| User velocity | Detects an unusual number of sign-on attempts by a single user | Risk + Protect |

**Fallback value:** Most predictors can be configured with a fallback risk level (LOW / MEDIUM / HIGH) used when there is insufficient data to calculate the actual risk level. Set the fallback based on the risk tolerance for your use case.

**Custom predictors:** Add risk-related data not covered by built-in predictors. Two types: (1) data Protect already has but is not in a standard predictor (e.g., country of origin), or (2) external risk data you supply as input.

**Composite predictors:** Combine multiple predictors into a single predictor evaluated as a unit (e.g., flag as high risk only when anonymous network AND geovelocity anomaly both fire together).

---

## Risk policy types

A risk policy combines multiple predictors and maps the combined score to an overall risk level (LOW / MEDIUM / HIGH).

| Policy type | Description | When to use |
|---|---|---|
| **Standard** | Configure predictor scores and risk-level thresholds; applies to all authentication events | Simple deployments with a single risk posture |
| **Targeted** | Add flow-type, application, and user-group targeting criteria in addition to predictor scores and thresholds; multiple targeted policies evaluated in listed order; stops at first match | Different risk postures per app, user segment, or flow type (e.g., stricter for admin logins) |

**Risk level output:** Every evaluation returns LOW, MEDIUM, or HIGH plus a `recommendation.value` of ALLOW, CHALLENGE, or BLOCK. Flows should branch on the `recommendation.value` rather than the raw score — this keeps the threshold logic inside Protect's policy engine, not hardcoded in the flow.

**Default risk policy:** Every environment with Protect enabled includes a default risk policy. Custom policies can be added for different scenarios.

**Policy training:** New risk policies require a training period before machine-learning predictors (New Device, User-based risk behavior, etc.) produce meaningful results. During training, set conservative fallback values to avoid over-blocking.

---

## Signals SDK requirement

The **PingOne Signals SDK** (also called the Protect SDK) collects device fingerprint and behavioral signals from the user's browser or mobile app. These signals are required for predictors that depend on device data (New Device, Suspicious Device, Bot Detection, AitM).

**Without the SDK:** Protect can only evaluate IP and network signals. Bot detection, device-based predictors, and AitM operate with significantly reduced accuracy.

| Platform | SDK integration point |
|---|---|
| DaVinci flows | Add the `skrisk` component to the HTTP connector in the flow; enable "SDK payload provided as signed JWT" in the component configuration for maximum signal fidelity |
| AIC journeys | A client-side Script node collects the `_pingProtect` context object before the Protect Evaluation node runs |
| PingFederate | The Protect JavaScript SDK must be embedded in the user-facing application independently; PingFederate does not embed the SDK server-side |

**Bot detection and AI agents:** As of 2025, Protect's bot detection predictor identifies agentic AI automation and computer-using agents (CUAs) as bot activity. Flows handling non-human actors (AI agents, automation) should explicitly account for this — either allow-listing known automation clients or designing separate non-human flows that do not trigger Protect.

---

## Configuration checklist (before flow invocation)

| Step | Location |
|---|---|
| 1. Enable PingOne Protect service in the environment | Settings > Services > PingOne Protect |
| 2. Review and configure predictor instances | Threat Protection > Predictors |
| 3. Set fallback values on each predictor | Each predictor's edit panel |
| 4. Create or modify the risk policy; assign predictors and thresholds | Threat Protection > Risk Policies |
| 5. Embed Signals SDK in the user-facing application | App code (browser or mobile) |
| 6. Configure the Protect connector (DaVinci) or Protect node (AIC) to reference the risk policy ID | DaVinci connector config or AIC node config |

---

## Prerequisites

- PingOne environment with PingOne Protect (or PingOne Risk) service enabled
- Admin role: Environment Admin or Organization Admin
- For Bot detection, AitM, Suspicious device: PingOne Protect license (not just PingOne Risk)
- For PingID Device Trust: PingID Device Trust agent installed on managed workstations

## Common variants

| Variant | Note |
|---|---|
| Multi-population risk policies | Use Targeted policies; each policy targets a different user population or application |
| CIAM risk scoring | Anonymous network + Geovelocity + New device are the primary CIAM predictors; User-based risk behavior improves over time |
| Workforce risk scoring | Add PingID Device Trust for managed device compliance; Targeted policy for admin flows with stricter thresholds |
| Testing predictors | Use the sample app in PingOne to simulate risk events (geovelocity, anonymous network, new device) before production deployment |

## Related references

- `references/curated/service-invocation-patterns.md` — how flows invoke Protect at runtime
- `references/curated/cross-platform-service-usage.md` — platform constraints and chaining patterns

## Source

- https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_introduction.html
- https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_risk_predictors.html
- https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_risk_policies.html
- https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_getting_started.html
- https://docs.pingidentity.com/pingone/threat_protection_using_pingone_protect/p1_protect_signals_sdk.html
