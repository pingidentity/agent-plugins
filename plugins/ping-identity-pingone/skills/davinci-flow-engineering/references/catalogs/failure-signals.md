# Failure signals

| Signal | Interpretation |
|---|---|
| Error response followed by retry or success | Recovered condition; retain as a warning, not terminal failure |
| Error response is the final unresolved event | Terminal failure when no later branch or subflow resolves it |
| Timeout, abort, or cancellation at chain end | Abnormal termination; usually medium confidence without explicit cause |
| Same node ID appears 3 or more times | Loop candidate; confirm that no exit or later success exists |
| Events stop at an interactive node | Possible stalled interaction; verify node configuration and expected client behavior |
| Start/end events only | Minimal logging; outcome is partial unless another source establishes it |
| DaVinci success followed by user failure | Check later policy/audit events and application response handling |
| Missing subflow execution | Incomplete evidence, not proof that the subflow succeeded or failed |

Classify only after merging the complete flow and subflow chain. Node titles and event labels are evidence, but node configuration and later events determine whether a signal is expected, recovered, or terminal.
