# Helix for Headless Agentic Workflows in AIC and DaVinci

## Executive Summary

Helix is the right orchestration layer for a headless agentic workflow across both AIC and DaVinci. The most practical pattern is to run agent logic in Helix, invoke it remotely via Helix conversation and message APIs, and let the agent call product APIs through custom tools and functions. For AIC, this is the clearest production-shaped pattern today. For DaVinci, it aligns directly with the current Helix-backed assistant direction. <cite>citation_153:1,citation_247:0,citation_247:1,citation_247:3,citation_247:5,citation_247:6,citation_195:13,citation_195:19</cite>

## What Helix Provides

Helix supports outbound auth using agent identity or OAuth client credentials. It also supports tool and function integrations via `get_security_headers()`, which allows downstream API calls with the right security context. Helix also supports token passthrough so user context can propagate into agent execution when needed. <cite>citation_205:6,citation_205:55,citation_205:73,citation_198:37,citation_198:38</cite>

The practical execution model is:

1. Start a Helix conversation.
2. Post a start message.
3. Poll for completion.
4. Let the agent call AIC or DaVinci APIs through Helix tools.
5. Return results, recommended actions, or generated artifacts such as flow JSON. <cite>citation_247:0,citation_247:1,citation_247:3,citation_247:5,citation_247:6</cite>

## AIC: Recommended Headless Pattern

For AIC, the recommended pattern is Helix-native API orchestration.

### Suggested setup

- Make AIC the IDP for the Helix environment. <cite>citation_205:2</cite>
- Give the agent either agent identity or AIC service-account / OAuth credentials. <cite>citation_205:6,citation_206:34</cite>
- Implement Helix custom tools or functions that call AIC REST APIs using Helix security headers. <cite>citation_205:55,citation_205:73</cite>
- Invoke the agent headlessly from a backend service, CI job, scheduler, or another orchestration layer via Helix conversation APIs. <cite>citation_247:0,citation_247:1,citation_247:3</cite>

### Good use cases

- AIC config and admin automation
- Journey, application, and managed-object inspection
- Usage and audit-oriented analysis
- Guided write workflows with policy checks before commit <cite>citation_207:68,citation_207:69,citation_207:72</cite>

### Key limitation

The current AIC MCP server is not yet the strongest basis for unattended headless runtime. There is an explicit request for headless support, and current modes still depend on interactive auth flows. Internal guidance also says the AIC MCP server should not be used against production. <cite>citation_214:1,citation_214:7,citation_214:8,citation_215:52</cite>

### Recommendation

Use Helix directly for production-oriented headless AIC workflows. Treat the AIC MCP server as a developer-assistant or sandbox path for now. <cite>citation_214:8,citation_215:52</cite>

## DaVinci: Recommended Headless Pattern

For DaVinci, Helix is an even cleaner fit because the product direction already assumes a Helix-backed assistant pattern.

### Suggested setup

- DaVinci, or a thin backend facade, creates a Helix conversation against a published agent version. <cite>citation_164:8,citation_164:11</cite>
- It sends the prompt plus current flow and environment context. <cite>citation_195:13,citation_195:19</cite>
- Helix returns complete flow JSON updates. <cite>citation_195:19,citation_195:32,citation_195:46</cite>
- DaVinci validates dependencies, versions the result, and only applies changes after policy or human-in-the-loop gates. <cite>citation_195:38,citation_195:46</cite>

This matches the current build-use-case direction: Helix asks clarifying questions, DaVinci consumes generated flow JSON, and the canvas is locked while generation is in progress. <cite>citation_195:16,citation_195:19,citation_195:38</cite>

### Key limitation

DaVinci has evaluated Helix-hosted remote MCP, but the decision to use it is still open. A custom remote MCP path is also being explored. <cite>citation_196:5,citation_196:6</cite>

### Recommendation

Use Helix agent APIs first for DaVinci headless execution. Do not make Helix-hosted remote MCP the primary production path until that evaluation closes. <cite>citation_196:5,citation_196:6</cite>

## Shared Architecture Recommendation

Use the same core model for both AIC and DaVinci:

- Helix as the orchestration and runtime layer
- Product-specific custom Helix tools as the execution layer
- Helix conversation APIs as the async control plane
- Policy and approval gates before write or apply operations
- Published agent versions for stability and repeatability <cite>citation_153:1,citation_247:0,citation_247:1,citation_247:3,citation_247:5,citation_164:11</cite>

### AIC flow

Scheduler or backend service -> Helix agent -> AIC-facing custom tools -> AIC APIs -> result or proposed change set. <cite>citation_205:55,citation_205:73,citation_247:0</cite>

### DaVinci flow

DaVinci UI or backend service -> Helix build or troubleshoot agent -> DaVinci-facing tools -> flow generation, validation, or troubleshooting output -> review and apply. <cite>citation_195:13,citation_195:19,citation_195:32,citation_195:46</cite>

## Practical Implementation Guidance

If one implementation path is needed for both products, use this sequence:

1. Standardize on Helix as the headless runtime. <cite>citation_153:1,citation_247:0</cite>
2. Build product-specific tool surfaces:
   - `aic_*` tools for AIC REST and admin operations
   - `davinci_*` tools for flow build, inspect, and troubleshoot operations
3. Invoke all agents through the Helix conversation APIs.
4. Keep MCP as a secondary interoperability surface for developer tooling and external agent ecosystems.
5. Put write operations behind policy and approval gates, especially where token passthrough or user context is involved, because Helix threat modeling explicitly calls out excessive-agency risk. <cite>citation_198:37,citation_198:38,citation_231:31</cite>

## Final Recommendation

If the goal is a real headless agentic workflow across both AIC and DaVinci, the architecture should be centered on Helix agents, Helix APIs, and product-specific tools. MCP should be additive, not central. That gives the cleanest and most consistent operating model across both platforms today. <cite>citation_214:8,citation_196:6,citation_247:0,citation_205:55</cite>
