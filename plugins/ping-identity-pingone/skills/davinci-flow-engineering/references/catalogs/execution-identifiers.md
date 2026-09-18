# Execution identifiers

| Identifier | Use |
|---|---|
| Environment ID or name | Required scope for all live retrieval |
| Transaction ID | Correlates the main execution, subflows, and related audit events |
| Interaction or execution ID | Locates one flow execution; flow context may also be required |
| Flow ID | Stable scope for execution search and definition retrieval |
| Flow name | Resolve to a flow ID; disambiguate duplicate or similar names |
| Username | Common actor filter for DaVinci execution search |
| Email | May equal username; otherwise resolve to identity before retrying |
| Time window | Bounds searches and distinguishes repeated executions |

Prefer transaction ID, then interaction ID, actor, and finally time-only discovery. Never derive an environment from an opaque identifier unless verified against the resolved environment. Preserve exact IDs during correlation; do not normalize or truncate values used for retrieval.
