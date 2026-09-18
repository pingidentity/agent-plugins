# PingFederate Terraform

Use Terraform only for PingFederate settings explicitly covered by an approved provider or deployment workflow. The existence of PingFederate APIs does not establish Terraform resource coverage.

## Intent routing
| Request signal | Use when | Continue with |
|---|---|---|
| Provider-managed configuration | Manage settings covered by a verified provider resource | [PingFederate provider](https://registry.terraform.io/providers/pingidentity/pingfederate/latest/docs) |
| Terraform orientation | Find provider guidance and supported product coverage | [Terraform at Ping Identity](../terraform/README.md) |

## Source
- [PingFederate provider](https://registry.terraform.io/providers/pingidentity/pingfederate/latest/docs)
- [PingFederate official documentation](https://docs.pingidentity.com/pingfederate/latest/index.md)
- [Terraform at Ping Identity](https://developer.pingidentity.com/terraform/terraform_landing_page.md)
