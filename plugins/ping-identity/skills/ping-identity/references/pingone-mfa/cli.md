# PingOne MFA CLI

The Ping CLI exposes the PingOne MFA administration command group. Use the current command reference rather than relying on version-specific subcommand assumptions.

## Intent routing

| Request signal | Use when | Continue with |
|---|---|---|
| MFA settings | Inspect or manage environment MFA settings | `pingcli mfa settings --help` and the [MFA command reference](https://developer.pingidentity.com/pingcli/latest/command_reference/pingcli_mfa.html) |
| Device policies | Manage MFA device policies | `pingcli mfa device-policies --help` and the [MFA command reference](https://developer.pingidentity.com/pingcli/latest/command_reference/pingcli_mfa.html) |
| FIDO2 policies | Manage FIDO2 policy configuration | `pingcli mfa fido2-policies --help` and the [MFA command reference](https://developer.pingidentity.com/pingcli/latest/command_reference/pingcli_mfa.html) |
| User devices | Manage user MFA devices | `pingcli mfa user-devices --help` and the [MFA command reference](https://developer.pingidentity.com/pingcli/latest/command_reference/pingcli_mfa.html) |

`pingcli pingone api` can be used to make direct API requests to manage PingOne MFA configuration that may be not available to manage through native commands.

## Boundary

This handoff covers administration command discovery. It does not provide tenant-specific policy values, device enrollment procedures, or Workforce PingID desktop commands. Verify the installed CLI version and current help output before generating a script.

## Source

- [Ping CLI MFA command reference](https://developer.pingidentity.com/pingcli/latest/command_reference/pingcli_mfa.html)
