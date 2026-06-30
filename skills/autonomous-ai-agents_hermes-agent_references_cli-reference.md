---
name: autonomous-ai-agents_hermes-agent_references_cli-reference
description: CLI Reference
title: "Autonomous Ai Agents ReYMeN Agent References Cli Reference"
version: 1.0.0
---


| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI/ML mühendisi |
| **Ne** | CLI Reference |
| **Nerede** | AI_ML/ |
| **Ne Zaman** | AI/ML görevi gerektiğinde |
| **Neden** | standardize etmek için |
| **Nasıl** | Skill adımlarını takip ederek |

## CLI Reference

### Global Flags

```
ReYMeN [flags] [command]

  --version, -V             Show version
  --resume, -r SESSION      Resume session by ID or title
  --continue, -c [NAME]     Resume by name, or most recent session
  --worktree, -w            Isolated git worktree mode (parallel agents)
  --skills, -s SKILL        Preload skills (comma-separate or repeat)
  --profile, -p NAME        Use a named profile
  --yolo                    Skip dangerous command approval
  --pass-session-id         Include session ID in system prompt
```

No subcommand defaults to `chat`.

### Chat

```
ReYMeN chat [flags]
  -q, --query TEXT          Single query, non-interactive
  -m, --model MODEL         Model (e.g. anthropic/claude-sonnet-4)
  -t, --toolsets LIST       Comma-separated toolsets
  --provider PROVIDER       Force provider (openrouter, anthropic, nous, etc.)
  -v, --verbose             Verbose output
  -Q, --quiet               Suppress banner, spinner, tool previews
  --checkpoints             Enable filesystem checkpoints (/rollback)
  --source TAG              Session source tag (default: cli)
```

### Configuration

```
ReYMeN setup [section]      Interactive wizard (model|terminal|gateway|tools|agent)
ReYMeN model                Interactive model/provider picker
ReYMeN config               View current config
ReYMeN config edit          Open config.yaml in $EDITOR
ReYMeN config set KEY VAL   Set a config value
ReYMeN config path          Print config.yaml path
ReYMeN config env-path      Print .env path
ReYMeN config check         Check for missing/outdated config
ReYMeN config migrate       Update config with new options
ReYMeN auth                 Interactive credential manager
ReYMeN auth add PROVIDER    Add OAuth or API-key credential (e.g. nous, openai-codex, qwen-oauth)
ReYMeN auth list            List stored credentials
ReYMeN auth remove PROVIDER Remove a stored credential
ReYMeN doctor [--fix]       Check dependencies and config
ReYMeN status [--all]       Show component status
```

### Tools & Skills

```
ReYMeN tools                Interactive tool enable/disable (curses UI)
ReYMeN tools list           Show all tools and status
ReYMeN tools enable NAME    Enable a toolset
ReYMeN tools disable NAME   Disable a toolset

ReYMeN skills list          List installed skills
ReYMeN skills search QUERY  Search the skills hub
ReYMeN skills install ID    Install a skill (ID can be a hub identifier OR a direct https://…/SKILL.md URL; pass --name to override when frontmatter has no name)
ReYMeN skills inspect ID    Preview without installing
ReYMeN skills config        Enable/disable skills per platform
ReYMeN skills check         Check for updates
ReYMeN skills update        Update outdated skills
ReYMeN skills uninstall N   Remove a hub skill
ReYMeN skills publish PATH  Publish to registry
ReYMeN skills browse        Browse all available skills
ReYMeN skills tap add REPO  Add a GitHub repo as skill source
```

### MCP Servers

```
ReYMeN mcp serve            Run ReYMeN as an MCP server
ReYMeN mcp add NAME         Add an MCP server (--url or --command)
ReYMeN mcp remove NAME      Remove an MCP server
ReYMeN mcp list             List configured servers
ReYMeN mcp test NAME        Test connection
ReYMeN mcp configure NAME   Toggle tool selection
```

### Gateway (Messaging Platforms)

```
ReYMeN gateway run          Start gateway foreground
ReYMeN gateway install      Install as background service
ReYMeN gateway start/stop   Control the service
ReYMeN gateway restart      Restart the service
ReYMeN gateway status       Check status
ReYMeN gateway setup        Configure platforms
```

Supported platforms: Telegram, Discord, Slack, WhatsApp, Signal, Email, SMS, Matrix, Mattermost, Home Assistant, DingTalk, Feishu, WeCom, BlueBubbles (iMessage), Weixin (WeChat), API Server, Webhooks. Open WebUI connects via the API Server adapter.

Platform docs: https://ReYMeN-agent.nousresearch.com/docs/user-guide/messaging/

### Sessions

```
ReYMeN sessions list        List recent sessions
ReYMeN sessions browse      Interactive picker
ReYMeN sessions export OUT  Export to JSONL
ReYMeN sessions rename ID T Rename a session
ReYMeN sessions delete ID   Delete a session
ReYMeN sessions prune       Clean up old sessions (--older-than N days)
ReYMeN sessions stats       Session store statistics
```

### Cron Jobs

```
ReYMeN cron list            List jobs (--all for disabled)
ReYMeN cron create SCHED    Create: '30m', 'every 2h', '0 9 * * *'
ReYMeN cron edit ID         Edit schedule, prompt, delivery
ReYMeN cron pause/resume ID Control job state
ReYMeN cron run ID          Trigger on next tick
ReYMeN cron remove ID       Delete a job
ReYMeN cron status          Scheduler status
```

### Webhooks

```
ReYMeN webhook subscribe N  Create route at /webhooks/<name>
ReYMeN webhook list         List subscriptions
ReYMeN webhook remove NAME  Remove a subscription
ReYMeN webhook test NAME    Send a test POST
```

### Profiles

```
ReYMeN profile list         List all profiles
ReYMeN profile create NAME  Create (--clone, --clone-all, --clone-from)
ReYMeN profile use NAME     Set sticky default
ReYMeN profile delete NAME  Delete a profile
ReYMeN profile show NAME    Show details
ReYMeN profile alias NAME   Manage wrapper scripts
ReYMeN profile rename A B   Rename a profile
ReYMeN profile export NAME  Export to tar.gz
ReYMeN profile import FILE  Import from archive
```

### Credential Pools

```
ReYMeN auth add             Interactive credential wizard
ReYMeN auth list [PROVIDER] List pooled credentials
ReYMeN auth remove P INDEX  Remove by provider + index
ReYMeN auth reset PROVIDER  Clear exhaustion status
```

### Other

```
ReYMeN insights [--days N]  Usage analytics
ReYMeN update               Update to latest version
ReYMeN pairing list/approve/revoke  DM authorization
ReYMeN plugins list/install/remove  Plugin management
ReYMeN honcho setup/status  Honcho memory integration (requires honcho plugin)
ReYMeN memory setup/status/off  Memory provider config
ReYMeN completion bash|zsh  Shell completions
ReYMeN acp                  ACP server (IDE integration)
ReYMeN claw migrate         Migrate from OpenClaw
ReYMeN uninstall            Uninstall ReYMeN
```
