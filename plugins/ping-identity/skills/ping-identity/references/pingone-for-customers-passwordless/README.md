# PingOne for Customers Passwordless

## Overview
PingOne for Customers Passwordless combines guided setup with preconfigured DaVinci flows for password-free customer journeys. It helps organizations configure and test common registration, authentication, profile-update, and account-recovery experiences before adapting them for production.

## Core Concepts
- **Passwordless customer journeys:** Covers registration, authentication, profile updates, and account recovery so customers can use supported password-free experiences across key lifecycle interactions.
- **Email and SMS passcodes:** One-time passcodes and email magic links provide alternative ways to authenticate without a password.
- **FIDO2:** Adds a supported passwordless authentication method for customer journeys.
- **Risk and bot defenses:** A configurable PingOne Protect implementation supports bot and high-risk-user defenses, with additional handling options for lower-risk users.
- **Guided templates:** Organizations can choose methods, test them in a sample application, tailor configuration, and duplicate resulting flows for production use.

## When to use
- Use for common passwordless customer registration, sign-in, profile, or recovery scenarios.
- Use when a guided, testable starting point and reusable DaVinci flows are appropriate.

## When not to use
- Do not treat the packaged components as coverage for every DaVinci capability; assess fit for specialized requirements.
- For voice, mobile-app methods, or time-based one-time passwords, use the licensed PingOne MFA extension and account for required flow and environment changes.
- Adapt templates when compliance or regulatory requirements call for additional controls.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/pingone-solutions/pingone-customers-passwordless/index.md)
