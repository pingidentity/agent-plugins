# Ping Configuration Promotion

## Overview
Ping Deployment Automation guides teams in moving Ping Identity configuration across environments with CI/CD, GitOps, and configuration-as-code practices. The approach makes promotion repeatable and reviewable while reducing manual configuration errors.

## Core Concepts
- **Configuration as code:** Version machine-readable configuration to support collaboration, reproducibility, change history, and rollback.
- **Validation:** Check syntax, formatting, dependencies, security, and compliance before promotion; these checks do not replace product testing.
- **Audit and review:** Compare current and desired state and review changes for intent, compliance, and unverified modifications.
- **Automated testing:** Run unit and integration tests in CI to check components, dependencies, data flow, and error handling.
- **Promotion and deployment:** Deliver approved changes to pre-production and production through Terraform, APIs or CLI, Postman collections, or Server Configuration Profiles.
- **Verification:** Use Terraform plans, assertions, or API checks to detect post-deployment drift, including external changes.
- **Journey and flow artifacts move as static configuration:** Authentication journeys, DaVinci flows and flow policies, scripts, and themes promote as configuration between environments; runtime data — live sessions, MFA device enrollments, user-created applications, and user profile data — never moves and must be handled by process, not promotion.

## When to use
- Organizations managing Ping Identity across multiple environments need controlled, repeatable promotion.
- Platform, application, or self-managed infrastructure teams are building a GitOps or CI/CD pipeline.

## When not to use
- Example pipelines and validation checks are not complete product-specific implementations or deployment guarantees.
- Use product documentation for configuration authoring and behavior details.

## Gotchas

Stage separation differs by platform — use the right model per platform:

- **PingOne (multi-tenant):** separate environments per stage within the same org; OAuth client IDs differ per stage — do not share them. PingOne allows GitOps based configuration promotion (most flexibility, advanced use cases), or an in-console promotion capability (simple use cases) enabled as a preview feature.
- **AIC:** separate tenant instances per stage; promote configuration initiated via the AIC REST API or Ping Platform Config Manager.
- **AIC promotion runs an integrity check:** Promotion is blocked when configuration references an environment-specific variable missing in the target, or when an encrypted secret is embedded directly in configuration instead of referenced.
- **DaVinci connector credentials are promotion-gated:** Sensitive connector attributes (secrets, API keys) block promotion until matching promotion variables exist, created in the source environment with the target-specific value.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://developer.pingidentity.com/config-automation-promotion/configuration_promotion_landing_page.md)
