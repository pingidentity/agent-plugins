# Ping Enterprise Connect

## Overview
Ping Enterprise Connect is a paid add-on for PingOne Advanced Identity Cloud and self-managed PingAM. It extends enterprise authentication with MFA for Windows and Mac workstations, virtual Windows environments, and RADIUS-connected tools.

## Core Concepts
- **Workstation MFA:** Enforces MFA on Windows and Mac endpoints to protect managed-device access.
- **Remote desktop MFA:** Adds MFA to virtual Windows machines.
- **Windows desktop SSO:** Signs users into the Ping Identity environment after Windows login.
- **Windows RADIUS proxy:** Extends MFA to tools such as organizational VPNs.
- **Journey-based deployment:** Uses feature-specific installation files with journeys connected to PingOne Advanced Identity Cloud or PingAM.

## When to use
- Protecting Windows or Mac workstations with MFA.
- Securing virtual Windows desktops, VPNs, or similar RADIUS-integrated tools.
- Providing Ping Identity sign-in after Windows login.

## When not to use
- For complete passwordless deployment: Enterprise Connect adds a factor but does not remove the password experience; consider Enterprise Connect Passwordless instead.
- Without the paid add-on or a supported PingOne Advanced Identity Cloud or self-managed PingAM 7.x.x/8.x.x environment.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/enterprise-connect/latest/index.md)
