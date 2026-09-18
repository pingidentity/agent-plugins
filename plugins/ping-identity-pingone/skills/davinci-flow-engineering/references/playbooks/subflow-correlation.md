# Subflow correlation

Use these invariants whenever a flow may invoke another flow:

1. Resolve and retain the main execution's transaction ID.
2. Inspect the definition active at execution time, not only the latest flow definition.
3. Identify invoked subflows from both definition and execution evidence.
4. Search each referenced flow for execution records sharing the transaction ID.
5. Retrieve every page and every matching invocation.
6. Repeat for nested subflows while tracking visited execution IDs and flow IDs.
7. Stop a circular branch without discarding other branches.
8. Merge all events globally by timestamp and preserve source flow and interaction IDs.
9. Report referenced subflows whose execution evidence could not be retrieved.

A shared transaction ID establishes correlation, not ordering. Use event timestamps and flow-local sequence to construct the timeline.
