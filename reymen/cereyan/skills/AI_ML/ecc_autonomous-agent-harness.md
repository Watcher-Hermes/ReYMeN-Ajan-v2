---
name: ecc_autonomous-agent-harness
title: Ecc Autonomous Agent Harness
description: ''
tags:
- ai_ml
category: AI_ML
audience: agent
---
| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI muhendisi |
| **Ne** | Transform Claude Code into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing. Replaces standalone agent frameworks (ReYMeN, AutoGPT) by lever |
| **Nerede** | `ai\ecc\ecc_autonomous-agent-harness.md` |
| **Ne Zaman** | AI modeli secimi veya degerlendirmesi gerektiginde |
| **Neden** | Ecc Autonomous Agent Harness islemini standartlastirmak icin |
| **Nasıl** | Skill dosyasindaki adimlari takip ederek |


## 📋 5N1K

| Soru | Cevap |
|:-----|:------|
| **Kim?** | Tüm ajanlar |
| **Ne?** | Transform Claude Code into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing. Replaces standalone agent frameworks (ReYMeN, AutoGPT) by leveraging Claude Code's native crons, dispatch, MCP tools, and memory. Use when the user wants continuous autonomous operation, scheduled tasks, or a self-directing agent loop. |
| **Nerede?** | ecc/ |
| **Ne Zaman?** | İhtiyaç duyulduğunda |
| **Neden?** | Otomatik kategorilendirme |
| **Nasıl?** | Skill referansı ile |

Kim: AI muhendisi
Ne: Transform Claude Code into a fully autonomous agent system with persistent memory, scheduled operations, computer use, and task queuing. Replaces standalone agent frameworks (ReYMeN, AutoGPT) by lever
Nerede: `ai\ecc\ecc_autonomous-agent-harness.md`
Ne Zaman: AI modeli secimi veya degerlendirmesi gerektiginde
Neden: Ecc Autonomous Agent Harness islemini standartlastirmak ve tekrarlanabilir kilmak icin
Nasil: Skill dosyasindaki adimlari takip ederek

name: task-queue
type: project
description: Persistent task queue for autonomous operation
## Active Tasks
- [ ] PR #123: Review and approve if CI green
- [ ] Monitor deploy: check /health every 30 min for 2 hours
- [ ] Research: Find 5 leads in AI tooling space

## Completed
- [x] Daily standup: reviewed 3 PRs, 2 issues
```

## Replacing ReYMeN

| ReYMeN Component | ECC Equivalent | How |
|------------------|---------------|-----|
| Gateway/Router | Claude Code dispatch + crons | Scheduled tasks trigger agent sessions |
| Memory System | Claude memory + MCP memory server | Built-in persistence + knowledge graph |
| Tool Registry | MCP servers | Dynamically loaded tool providers |
| Orchestration | ECC skills + agents | Skill definitions direct agent behavior |
| Computer Use | computer-use MCP | Native browser and desktop control |
| Context Manager | Session management + memory | ECC 2.0 session lifecycle |
| Task Queue | Memory-persisted task list | TodoWrite + memory files |

## Setup Guide

### Step 1: Configure MCP Servers

Ensure these are in `~/.claude.json`:

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/memory-mcp-server"]
    },
    "scheduled-tasks": {
      "command": "npx",
      "args": ["-y", "@anthropic/scheduled-tasks-mcp-server"]
    },
    "computer-use": {
      "command": "npx",
      "args": ["-y", "@anthropic/computer-use-mcp-server"]
    }
  }
}
```

### Step 2: Create Base Crons

```bash
# Daily morning briefing
claude -p "Create a scheduled task: every weekday at 9am, review my GitHub notifications, open PRs, and calendar. Write a morning briefing to memory."

# Continuous learning
claude -p "Create a scheduled task: every Sunday at 8pm, extract patterns from this week's sessions and update the learned skills."
```

### Step 3: Initialize Memory Graph

```bash
# Bootstrap your identity and context
claude -p "Create memory entities for: me (user profile), my projects, my key contacts. Add observations about current priorities."
```

### Step 4: Enable Computer Use (Optional)

Grant computer-use MCP the necessary permissions for browser and desktop control.

## Example Workflows

### Autonomous PR Reviewer
```
Cron: every 30 min during work hours
1. Check for new PRs on watched repos
2. For each new PR:
   - Pull branch locally
   - Run tests
   - Review changes with code-reviewer agent
   - Post review comments via GitHub MCP
3. Update memory with review status
```

### Personal Research Agent
```
Cron: daily at 6 AM
1. Check saved search queries in memory
2. Run Exa searches for each query
3. Summarize new findings
4. Compare against yesterday's results
5. Write digest to memory
6. Flag high-priority items for morning review
```

### Meeting Prep Agent
```
Trigger: 30 min before each calendar event
1. Read calendar event details
2. Search memory for context on attendees
3. Pull recent email/Slack threads with attendees
4. Prepare talking points and agenda suggestions
5. Write prep doc to memory
```

## Constraints

- Cron tasks run in isolated sessions — they don't share context with interactive sessions unless through memory.
- Computer use requires explicit permission grants. Don't assume access.
- Remote dispatch may have rate limits. Design crons with appropriate intervals.
- Memory files should be kept concise. Archive old data rather than letting files grow unbounded.
- Always verify that scheduled tasks completed successfully. Add error handling to cron prompts.