# Identity Verification using PingOne Verify

## Overview
PingOne Verify supports identity proofing by comparing a government-issued document with live facial capture. Organizations can automate identity checks and retain outcomes for review and access decisions.

## Core Concepts
- **Document and biometric verification:** OCR and barcode scanning read document information, assess validity, and compare the face with a live selfie.
- **Verification policies:** Policies combine government-ID checks, facial comparison, liveness, and transaction requirements to define verification checks.
- **Orchestration and channels:** Transactions can start through AIC or PingAM journeys, PingFederate, DaVinci, REST APIs, or iOS and Android SDKs, with browser and mobile capture.
- **Transaction outcomes:** Transactions record status, timestamp, result metadata, and audit information; authorized administrators can manually approve an incomplete check.

## When to use
- Automating identity proofing for new-employee onboarding before access provisioning.
- Supporting checks during registration, sign-on, or higher-risk transactions.
- Connecting verification to an existing journey, flow, federation integration, API, or mobile application.

## When not to use
- Identity proofing is not employment-eligibility verification; the documented onboarding process still requires an I-9.
- For supported documents, jurisdictions, API schemas, or detailed policy behavior, use the relevant Verify documentation.

## Gotchas
- **End-user camera access requires a correct HTTPS origin** — a wrong origin makes the browser deny camera permission before any capture starts.
- **`REQUIRES_INSPECTION` results need a human review queue** for manual fallback; there is no automatic approval.
- The Verify connector in DaVinci needs a PingOne worker app client ID/secret — use a **dedicated worker**, not the main application credential.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingone/identity_verification_using_pingone_verify/p1_verify_start.md)
