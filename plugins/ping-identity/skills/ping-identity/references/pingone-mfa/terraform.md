# PingOne MFA Terraform

The PingOne Terraform provider documents resources and a data source for supported PingOne MFA administration. Use the provider version's current schema for arguments, import behavior, and environment or service prerequisites.

## Intent routing

| Request signal | Use when | Continue with |
|---|---|---|
| MFA settings | Manage environment-level MFA settings as code | [ `pingone_mfa_settings` resource](https://registry.terraform.io/providers/pingidentity/pingone/latest/docs/resources/mfa_settings) |
| Device policy | Manage a method-specific MFA device policy | [ `pingone_mfa_device_policy` resource](https://registry.terraform.io/providers/pingidentity/pingone/latest/docs/resources/mfa_device_policy) |
| Default device policy | Manage the default MFA device policy | [ `pingone_mfa_device_policy_default` resource](https://registry.terraform.io/providers/pingidentity/pingone/latest/docs/resources/mfa_device_policy_default) |
| FIDO2 policy | Manage FIDO2 policy configuration | [ `pingone_mfa_fido2_policy` resource](https://registry.terraform.io/providers/pingidentity/pingone/latest/docs/resources/mfa_fido2_policy) |
| Application push credential | Manage native application push credentials used by MFA integrations | [ `pingone_mfa_application_push_credential` resource](https://registry.terraform.io/providers/pingidentity/pingone/latest/docs/resources/mfa_application_push_credential) |
| Policy discovery | Read MFA device policies for composition or validation | [ `pingone_mfa_device_policies` data source](https://registry.terraform.io/providers/pingidentity/pingone/latest/docs/data-sources/mfa_device_policies) |

## Source

- [PingOne provider on the Terraform Registry](https://registry.terraform.io/providers/pingidentity/pingone/latest/)
- [PingOne Terraform provider source](https://github.com/pingidentity/terraform-provider-pingone)
