# PingOne Privilege

## Overview
PingOne Privilege is a cloud-based privileged access management (PAM) solution for developers and DevOps teams accessing cloud infrastructure and applications. It provides passwordless, just-in-time access so permissions are granted only when needed and can be centrally governed.

## Core Concepts
- **Just-in-time permissions:** Self-service, resource-specific requests provide temporary authorization instead of persistent credentials and secrets.
- **Passwordless identity:** TPM or Apple Secure Enclave-backed keys can bind authentication to supported devices.
- **Multi-cloud governance:** Risk analysis and dynamic permission management help govern access across cloud environments.
- **Session oversight:** Administrators can view sessions in real time and terminate them when necessary.
- **Deployment choices:** Agent-based access provides stronger device assurance; an agentless CLI supports environments where an agent cannot be installed.

## When to use
- Govern privileged access to cloud accounts, Kubernetes environments, network infrastructure, and applications.
- Replace static credentials with centrally managed, time-limited access and session visibility.

## When not to use
- This area is specifically for cloud-based privileged access management, not general-purpose identity capabilities.
- For broader PingOne or PingOne Advanced Identity Cloud functionality unrelated to privileged infrastructure access, use the relevant product documentation.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/privilege/index.html)
