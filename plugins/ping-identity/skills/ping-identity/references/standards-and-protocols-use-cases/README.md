# Standards and Protocols Use Cases

## Overview
This area catalogs solution guides for standards- and protocol-related scenarios involving PingFederate and Office 365. It helps customers identify guidance for federation changes, Windows-integrated authentication, SAML identity naming, and SSL certificate diagnosis.

## Core Concepts
- **Office 365 federation:** Guidance for moving an Office 365 domain from WS-Federation to SAML2P, supporting a standards-aligned federation configuration.
- **Integrated Windows Authentication:** Coverage of browser Kerberos and NTLM configuration, including SPNEGO with PingFederate, to support Windows-integrated sign-on scenarios.
- **Group Policy browser settings:** Guidance for applying Integrated Windows Authentication browser settings through Group Policy, helping standardize enterprise client behavior.
- **Persistent SAML NameID:** Guidance for defining a persistent SAML NameID format in PingFederate, supporting stable subject identification across federated interactions.
- **SSL connectivity diagnosis:** OpenSSL-based checks for certificate validity, trust, and chain completeness, helping identify certificate-related connectivity issues.

## When to use
- You need to select guidance for an Office 365 federation or PingFederate standards/protocol scenario.
- You are evaluating Windows authentication, SAML NameID, or SSL certificate concerns.

## When not to use
- Do not treat this catalog as implementation procedures, prerequisites, or architecture guidance.
- Do not use it as a substitute for detailed troubleshooting or compatibility documentation; consult the corresponding product documentation.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://docs.pingidentity.com/solution-guides/standards_and_protocols_use_cases/htg_standards_and_protocols.md)
