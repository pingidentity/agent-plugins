---
title: "PingOne Verify — Policy Configuration and Transaction Flow"
product_family: cross-platform
products:
  - pingone-verify
  - pingone-davinci
  - pingone-aic
capabilities:
  - universal-services
services:
  - verify
audience:
  - architect
  - admin
  - developer
use_cases:
  - customer
  - workforce
doc_type: guide
status: current
canonical: true
last_updated: "2026-06-03"
slug: "https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_start.html"
---

# PingOne Verify — Policy Configuration and Transaction Flow

How to configure PingOne Verify policies and understand the verification transaction lifecycle — the setup required before flows can invoke Verify.

## Scope

**Covers:** Verify policy fields (document, liveness, facial comparison, voice, data-based), verification types, transaction lifecycle and statuses, IDA (Identity Assurance) claims storage, and the AAMVA integration.

**Does NOT cover:** How flows invoke Verify at runtime — see `references/curated/service-invocation-patterns.md`. Platform-specific node/connector configuration — see `references/curated/cross-platform-service-usage.md`.

---

## Verification types

PingOne Verify supports multiple verification modalities. A verify policy specifies which types are required, optional, or disabled.

| Type | What it does | Notes |
|---|---|---|
| **Government ID / Document Authentication** | Captures a photo of a government-issued ID; OCR + barcode scanning extracts PII; machine learning validates document authenticity | Default. Supports passport, driver's license, national ID |
| **Facial Comparison** | Compares a live selfie against the photo on the government ID | Default. Providers: Amazon (facial comparison), IDRND (liveness/injection detection) |
| **Liveness** | Detects that the selfie is from a live person, not a photo or mask | Default. Required when Facial Comparison is enabled |
| **Voice Verification** | Enrollment + verification using voice samples | Two separate policies required: one for enrollment, one for verification |
| **Data-Based Verification** | Verifies user identity attributes against trusted third-party data without requiring a physical document | US only. Returns a match score (Low/Medium/High) + risk evaluation; document-based verification can be triggered as a step-up for high-risk or no-match results |
| **DigiLocker (India)** | Verifies identity via India's government-backed electronic wallet; no document photo required | India only. Eliminates manual reviews for Indian residents |

**Balance:** An overly lenient policy allows identity spoofing; an overly strict policy causes user drop-off. Tune thresholds (Low/Medium/High) based on the use case and regulatory requirements.

---

## Verify policy fields

| Field | Options | Notes |
|---|---|---|
| **Name** | Free text | Required; identifies the policy in DaVinci and AIC node config |
| **Store Verified Claims** | On / Off | Stores extracted PII as Identity Assurance (IDA) attributes on the PingOne user object; view in admin console under user's Services > ID Verification tab |
| **Transaction Timeout** | 1–30 minutes | Time after transaction creation during which the full verification can complete |
| **Data Collection Timeout** | 1–30 minutes (default 15) | Time after verification is initiated in the UI during which the user can submit document/selfie data |
| **Data Collection Only** | On / Off | Collect documents and photos without running automated verification; for manual review workflows |
| **Inspection Type** | Automated / Manual / Step-Up to Manual | Manual and Step-Up to Manual require an additional license |
| **Enable AAMVA** | On / Off | Validates extracted driver's license data against the AAMVA DLDV (Driver's License Data Verification) database; US driver's licenses only |
| **Document type required** | ANY / specific type | Restrict verification to a specific document type (e.g., passport only) |
| **Facial Comparison** | Required / Optional / Disabled | |
| **Facial Comparison Threshold** | Low / Medium / High | Probability that selfie matches ID photo; higher threshold = stricter |
| **Liveness** | Required / Optional / Disabled | Required when Facial Comparison is Required |
| **Liveness Threshold** | Low / Medium / High | Probability that selfie passes liveness check |
| **Voice Verification** | Enrollment or Verification policy | Configure separately; voice verification requires two policies |

**Default policy:** Every environment with Verify enabled includes a default verify policy. Suitable for testing; configure a custom policy for production.

---

## Transaction lifecycle

A Verify transaction represents a single identity verification attempt by one user.

```
1. Flow creates a transaction (POST /v1/environments/{envId}/users/{userId}/verifyTransactions)
   → Returns: transactionId, webVerificationUrl (QR or web link for user), qrUrl

2. User completes verification on their device (mobile app or web browser)
   → Captures ID document photo + selfie
   → Data sent to Verify providers (Mitek for document, IDRND for liveness/injection, Amazon for facial comparison)

3. Flow polls transaction status
   GET /v1/environments/{envId}/users/{userId}/verifyTransactions/{transactionId}
   → Returns: status + verificationData (extracted fields) + metadata (per-provider results)

4. Transaction reaches terminal status
```

### Transaction statuses

| Status | Meaning | Flow action |
|---|---|---|
| `REQUESTED` | Transaction created; user has not yet started | Present QR/link to user; begin polling |
| `IN_PROGRESS` | User has started verification | Continue polling |
| `VERIFICATION_SUBMITTED` | User submitted data; processing | Continue polling |
| `APPROVED` | Verification passed | Proceed to application; optionally issue credential |
| `DECLINED` | Verification failed (document invalid, face mismatch, liveness failure) | Route to decline/fallback path |
| `REQUIRES_REVIEW` | Automated check inconclusive; manual review required | Route to manual review queue; inform user |
| `EXPIRED` | Transaction timeout elapsed before completion | Offer retry |
| `ERROR` | Service error | Log; route to error fallback |

**The `REQUIRES_REVIEW` state must be wired explicitly.** Flows that omit the `REQUIRES_REVIEW` path will drop users into an error state or loop indefinitely. Provision a manual review workflow or a "we'll contact you" holding page.

---

## Identity Assurance (IDA) claims

When **Store Verified Claims** is enabled in the Verify policy, successfully extracted PII is stored as IDA attributes on the PingOne user object:

- IDA attributes are stored per verify policy — each policy maintains its own IDA record
- View in the admin console: Directory > Users > [user] > Services > ID Verification
- IDA extends the OIDC protocol — verified user attributes and the verification metadata can be included in access tokens for downstream authorization decisions
- IDA attributes are verified at transaction time; they remain on the user object until the next verification supersedes them

**Downstream use:** Authorize policies can evaluate IDA attributes (e.g., `idaAssuranceLevel >= IAL2`) for resource access control.

---

## Transaction timeout planning

| Timeout | Default | Max | Notes |
|---|---|---|---|
| Transaction Timeout | Policy-defined | 30 min | Full transaction window from creation to terminal status |
| Data Collection Timeout | 15 min | 30 min | Window from initiating the UI to submitting data |

**DaVinci polling consideration:** DaVinci flows poll for transaction status using the Loop connector. The poll interval should be short (5–10 seconds) with a total poll window shorter than the Transaction Timeout. Stop polling and route to `EXPIRED` if the timeout elapses.

**AIC polling consideration:** The Verify Evaluation node has a `Waiting` outcome. Wire it to a `Polling Wait` node (5-second interval) that loops back to the Verify node. The journey exits `Waiting` when the status reaches a terminal state.

---

## Prerequisites

- PingOne environment with PingOne Verify service provisioned (separate licensing step)
- At least one Verify policy configured (or modify the default)
- For DaVinci: PingOne Verify connector instance configured with worker app credentials
- For AIC: PingOne Verify Evaluation node configured with the policy ID
- For AAMVA: additional license required; US driver's license data only
- For manual inspection: additional license required

## Common variants

| Variant | Pattern |
|---|---|
| KYC at registration | Invoke Verify after account creation; store IDA claims; issue credential on APPROVED |
| Step-up re-verification | Trigger Verify from a DaVinci or AIC step-up flow when Protect returns HIGH risk |
| Selfie-only liveness check | Disable Document Authentication; require Liveness only; lower friction for existing users |
| Data-based verification (US) | Enable Data-Based Verification; use document-based as step-up for high-risk outcomes only |
| Manual review queue | Enable Data Collection Only or set Inspection Type = Manual; route REQUIRES_REVIEW to a workflow that notifies a review team |

## Related references

- `references/curated/service-invocation-patterns.md` — how flows invoke Verify at runtime
- `references/curated/cross-platform-service-usage.md` — platform constraints, Waiting outcome handling, chaining with Credentials

## Source

- https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_introduction.html
- https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_policies.html
- https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_creating_verify_policy.html
- https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_types_of_verification.html
- https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_data_based_verification.html
- https://docs.pingidentity.com/auth-node-ref/latest/pingone/pingone-verify-evaluation.html
- https://docs.pingidentity.com/connectors/p1_verify_connector.html
