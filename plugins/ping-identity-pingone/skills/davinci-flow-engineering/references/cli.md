# Ping CLI execution mode

Use this mode when Ping CLI is installed and an authorized PingOne profile is configured. Explore commands, subcommands, and flags with `-h` at every level — treat it as the source of truth over this doc, since it reflects the installed version and this doc does not.

## What pingcli can't tell you

`pingcli davinci` and `pingcli pingone` expose no subcommand for flow executions, interactions, or audit activities. For those two capabilities only, use `pingcli pingone api` against the raw PingOne management API described below. Everything else needed for this skill — environments, flows, flow versions, users, connectors, connector instances, forms, variables — has a native command; discover it and its flags with `-h` rather than trusting a hardcoded example here.

Treat CLI, HTTP, and authorization errors as evidence gaps, not flow failures. Never print auth tokens or secrets, and don't persist execution or audit output beyond the session unless requested.

## PingOne API structure for execution and audit endpoints

- **Base path** — `environments/<env-id>/...`, relative to the configured regional `/v1` management API; `pingcli pingone api` supplies the base and region.
- **Resource hierarchy** — `flows/<flow-id>/interactions` (execution list) → `interactions/<interaction-id>/events` (per-execution event trail); `activities` is a sibling collection directly under the environment, not nested under a flow.
- **Filter grammar** — SCIM-style: `transactionId eq "<id>"`, `timestamp ge "<iso>" and timestamp le "<iso>"`, joined with `and`. The execution API does not support username/email filters — resolve those first via `environments/<env-id>/users?filter=<encoded-filter>`.
- **Pagination** — up to 500 records/page on execution endpoints, 200 on users/audit; follow `_links.next` until absent before concluding an execution, event, or subflow is missing.
- **Response envelope** — `_links`, `_embedded.<collectionName>`, top-level `count`/`size`. Trust `_embedded`/`data` over `_links.self`, which has been observed to omit path segments on the `interactions` collection even on a successful request.

## References

- [PingOne API llms.txt index](https://developer.pingidentity.com/pingone-api/llms.txt) — machine-readable index of every PingOne API doc page.
