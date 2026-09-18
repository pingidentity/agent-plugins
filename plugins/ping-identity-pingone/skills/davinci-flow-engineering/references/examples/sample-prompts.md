# Sample prompts

Use these prompts to evaluate routing and playbook behavior. Identifiers are synthetic unless explicitly replaced with authorized test data.

| ID | Prompt | Primary behavior |
|---|---|---|
| T-01 | Why did user john.doe@example.com fail to log in? Trace the full execution and tell me at which step it failed. | Actor-first discovery, audit fallback, complete chain |
| T-02 | Find all failed login attempts for alice@acme.com between 2026-06-28T08:00:00Z and 2026-06-28T09:00:00Z and explain what went wrong. | Exact time window, multiple executions |
| T-03 | What is the point of failure for flow execution ID abc123def456? Include node ID and flow details. | Interaction-first discovery and correlation |
| T-04 | User bob@example.com says MFA failed. Trace the main flow and all subflows in execution order and identify exactly which node caused the failure. | Recursive subflow traversal |
| T-05 | I have transaction ID txn-9876xyz. Retrieve all related flow and subflow executions, sort them chronologically, and summarize what happened. | Transaction correlation and global ordering |
| T-06 | Show me all failures in the Corporate SSO Login flow in the last 2 hours, correlate with subflows, and identify the most common failure node. | Flow resolution and aggregate comparison |
| T-07 | A user reports they were stuck in an infinite loop during registration. Their email is carol@example.com. What happened and how do we fix it? | Loop classification and remediation |
| T-08 | There was an authorization error around 2026-06-28T14:30:00Z. Find the flow execution, trace all subflows, and recommend a fix. | Approximate-time bounded discovery |
| T-09 | Flow execution ID xyz789abc failed silently. Identify the failure node, summarize the execution chain across all subflows, and recommend a configuration fix. | Abnormal termination without explicit error |
| T-10 | Compare the last 3 failed executions for user dave@example.com. Are they failing at the same node? What is the root cause pattern and recommended remediation? | Multi-execution comparison |

Minimum expectations for every diagnosis: no fabricated evidence; bounded discovery; complete pagination; transaction-based subflow correlation when available; chronological timeline; explicit confidence and evidence gaps; actionable remediation only when supported.
