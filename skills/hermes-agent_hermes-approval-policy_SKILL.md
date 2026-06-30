---
name: ReYMeN-agent-ReYMeN-approval-policy
description: Configure how ReYMeN Agent handles command and tool approvals. Use this
  skill when the user wants fully autonomous operation (no approval prompts), selective
  auto-approval, or to restore interactive safeguards.
title: ReYMeN Agent ReYMeN Approval Policy
version: 1.0.0
---

## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | AI/ML mühendisi |
| **Nerede?** | AI_ML/ |
| **Ne Zaman?** | AI/ML görevi gerektiğinde |
| **Neden?** | standardize etmek için |
| **Nasıl?** | Skill adımlarını takip ederek |

operation. Use when user wants to eliminate interactive approval prompts, enable
  subagent auto-approval, or adjust destructive-command confirmation behavior.
# ReYMeN Approval Policy

Configure how ReYMeN Agent handles command and tool approvals. Use this skill when the user wants fully autonomous operation (no approval prompts), selective auto-approval, or to restore interactive safeguards.

## Trigger

- User says "tüm onayları otomatik yap", "onay sorma", "otonom mod", "approvals off", "no prompts", or equivalent.
- User asks to enable/disable auto-approval for subagents, cron jobs, MCP reloads, or slash commands.
- User wants to change `approvals.mode`, `delegation.subagent_auto_approve`, or related approval settings.

## Class-Level Settings

| Setting | Values | Meaning |
|---------|--------|---------|
| `approvals.mode` | `manual` / `smart` / `off` | `off` = no prompts |
| `approvals.timeout` | seconds | 0 = no timeout wait |
| `approvals.cron_mode` | `deny` / `auto` | `auto` = cron runs without prompting |
| `approvals.mcp_reload_confirm` | true / false | false = no MCP reload confirm |
| `approvals.destructive_slash_confirm` | true / false | false = no destructive slash confirm |
| `delegation.subagent_auto_approve` | true / false | true = subagents auto-approve |

## Fully Autonomous Preset

The following sequence puts ReYMeN into fully autonomous mode. Run each `ReYMeN config set` separately or as a chain; all edits are idempotent.

```bash
ReYMeN config set approvals.mode off
ReYMeN config set approvals.timeout 0
ReYMeN config set delegation.subagent_auto_approve true
ReYMeN config set approvals.cron_mode auto
ReYMeN config set approvals.mcp_reload_confirm false
ReYMeN config set approvals.destructive_slash_confirm false
```

## Windows Pitfall

On Windows bash (git-bash), backslash-quoted paths can be stripped or mis-parsed. Use the **full ReYMeN executable path** in that shell:

```bash
/c/Users/marko/AppData/Local/hermes/hermes-agent/venv/Scripts/hermes.exe config set approvals.mode off
```

Do not rely on `python -m hermes_cli`; `hermes_cli` is a package, not a module.

## Verify

After changing settings, confirm with:

```bash
ReYMeN config get approvals.mode
ReYMeN config get delegation.subagent_auto_approve
```

Changes require a fresh session (`/reset` or restart) to take effect.

## Restore Interactive Mode

To re-enable prompts:

```bash
ReYMeN config set approvals.mode manual
ReYMeN config set approvals.timeout 60
ReYMeN config set delegation.subagent_auto_approve false
ReYMeN config set approvals.cron_mode deny
ReYMeN config set approvals.mcp_reload_confirm true
ReYMeN config set approvals.destructive_slash_confirm true
```
