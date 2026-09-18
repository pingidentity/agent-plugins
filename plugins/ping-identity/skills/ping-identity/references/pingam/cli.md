# PingAM Administration CLI

Use the command-line administration tooling documented for the target PingAM deployment. Choose Amster for release-specific PingAM administration, or consider the community-supported Frodo CLI when its deployment and version support match the target. Do not substitute the Ping CLI for self-managed PingAM administration.

## Intent routing
| Request signal | Use when | Continue with |
|---|---|---|
| Amster administration | Inspect or change self-managed PingAM configuration with the release-specific PingAM CLI | [PingAM Amster documentation](https://docs.pingidentity.com/pingam/latest/amster/introduction.html); verify the installed release in the [PingAM documentation](https://docs.pingidentity.com/pingam/latest/index.md) |
| Frodo community automation | Use a community CLI for supported Ping identity environments, ForgeOps deployments, or classic PingAM/PingIDM/PingDS deployments | [Frodo CLI](https://github.com/rockcarver/frodo-cli); check its compatibility and current usage before scripting |

## Boundary
Amster is PingAM release tooling; its command set and packaging are release-specific. Frodo is a community project, not a Ping-supported replacement for Amster, and its CLI (`frodo-cli`) is distinct from its supporting library (`frodo-lib`). Neither path supplies a version-independent command contract here. Verify compatibility and the effect of export, import, or configuration changes before running automation.

## Security and variables
- Treat URLs, tenant IDs, realm names, credentials, tokens, client secrets, and local paths as variables; do not place real secrets in generated examples.
- Use least-privilege administrator roles and protect any CLI configuration, token cache, export, or backup files produced by the tooling.

## Source
- [PingAM official documentation](https://docs.pingidentity.com/pingam/latest/index.md)
- [PingAM Amster documentation](https://docs.pingidentity.com/pingam/latest/amster/introduction.html)
- [Frodo project](https://github.com/rockcarver/frodo)
- [Frodo CLI](https://github.com/rockcarver/frodo-cli)
- [Frodo library](https://github.com/rockcarver/frodo-lib)
