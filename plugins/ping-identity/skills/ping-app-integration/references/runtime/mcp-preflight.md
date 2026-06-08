# MCP config preflight

> **How these MCP servers work:** Both the AIC and DaVinci MCP servers run **locally on your machine** and communicate over **stdio**. When you invoke an MCP tool, Claude Code spawns the server process via `npx` and sends JSON-RPC messages over stdin/stdout. The server then makes authenticated HTTP calls to your AIC tenant or PingOne DaVinci environment on your behalf. No cloud relay is involved — the process runs in your local shell with your configured credentials.

Before calling any AIC or DaVinci MCP tool, verify the required values are present in `~/.claude/settings.json` under `pluginConfigs["ping-identity-agent-plugins@pingidentity"].options`:

1. Read `~/.claude/settings.json` and check for the relevant keys under `pluginConfigs["ping-identity-agent-plugins@pingidentity"].options`.
2. For any missing or empty value, use `AskUserQuestion` to prompt the user.
3. Write confirmed values into `~/.claude/settings.json` under `pluginConfigs["ping-identity-agent-plugins@pingidentity"].options` using the Edit tool. Example structure:
   ```json
   "pluginConfigs": {
     "ping-identity-agent-plugins@pingidentity": {
       "options": {
         "aic_base_url": "https://openam-yourcompany.forgeblocks.com"
       }
     }
   }
   ```
4. Tell the user to run `/reload-plugins` so the MCP server picks up the new values before proceeding.

**AIC MCP** (platform: PingOne Advanced Identity Cloud / PingAM):

| option key | Ask if missing |
|---|---|
| `aic_base_url` | "What is your AIC tenant base URL? (e.g. `https://openam-mycompany.forgeblocks.com`)" |

**DaVinci MCP** (platform: PingOne + DaVinci):

| option key | Ask if missing |
|---|---|
| `davinci_environment_id` | "What is your PingOne environment ID (UUID)?" |
| `davinci_client_id` | "What is your PingOne Worker Application Client ID?" |
| `davinci_root_domain` | "What is your PingOne root domain? (e.g. `pingone.com`, `pingone.eu`) — default: `pingone.com`" |
| `davinci_custom_domain` *(optional)* | "Do you have a custom PingOne domain? (e.g. `auth.example.com`) — leave blank if using a standard regional domain" |

Only prompt for the server matching the detected platform branch. Do not ask for DaVinci values when executing against AIC, and vice versa.

## Cursor MCP preflight

If running inside Cursor, `userConfig` is not available. MCP servers are configured via environment variables. **Always attempt the MCP tool call directly — do not pre-check or ask for credentials.** Only surface configuration guidance if the call actually fails:

1. Call the requested MCP tool directly.
2. If the call **fails or the tool is unavailable**, tell the user:

   > "The Ping Identity MCP server is not responding. This usually means required environment variables are not set. Please configure the following in your shell (`~/.zshrc` or `~/.bashrc`) or in Cursor's MCP settings (**Settings → MCP → [server name] → Environment**):"
   >
   > **AIC server** (`aic`):
   > | Variable | Value |
   > |---|---|
   > | `AIC_BASE_URL` | Your AIC tenant base URL (e.g. `https://openam-mycompany.forgeblocks.com`) |
   >
   > **DaVinci server** (`davinci`):
   > | Variable | Value |
   > |---|---|
   > | `DAVINCI_MCP_ENVIRONMENT_ID` | Your PingOne environment UUID |
   > | `AUTHORIZATION_CODE_CLIENT_ID` | Your PingOne Worker Application Client ID |
   > | `ROOT_DOMAIN` | Regional domain — `pingone.com`, `pingone.eu`, or `pingone.asia` (default: `pingone.com`) |
   > | `CUSTOM_DOMAIN` | *(optional)* Your custom PingOne domain (e.g. `auth.example.com`) |
   >
   > "After setting the variables, reload the window (**Cmd+Shift+P → Developer: Reload Window**) and try again."

3. If the probe **succeeds**, proceed with the task using MCP tools.
4. Only fall back to curated references if MCP tools remain unavailable after the user has confirmed configuration.
