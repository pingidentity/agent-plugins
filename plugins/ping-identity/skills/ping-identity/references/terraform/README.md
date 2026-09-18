# Terraform at Ping Identity

## Overview
Terraform at Ping Identity connects Ping administration APIs to the Terraform ecosystem and community through product providers, available on the Terraform registry. Teams define Ping infrastructure and configuration as code, then promote reviewed changes across environments using GitOps, config-as-code methodology.

## When to use
- Promote consistent PingOne platform or PingFederate/PingOne Advanced Services configuration across environments using industry standard GitOps methodology.
- Adopt existing production configuration without recreating it.
- Use GitOps pipelines and drift detection for controlled configuration delivery.

## When not to use
- Do not treat Terraform state as a secrets store; use dedicated secret-management services for credentials.
- For runtime behavior or unsupported product settings, consult the relevant product documentation.

## Source
- [Product Index](https://docs.pingidentity.com/product-index.html)
- [Official documentation](https://developer.pingidentity.com/terraform/terraform_landing_page.md)
