---
name: autonomous-ai-agents_claude-code_references_claude-code-ReYMeN-orchestration-guide
description: Claude Code — ReYMeN Orchestration Guide
title: "Autonomous Ai Agents Claude Code References Claude Code ReYMeN Orchestration Guide"
version: 1.0.0
---


| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI/ML mühendisi |
| **Ne** | Claude Code — ReYMeN Orchestration Guide |
| **Nerede** | AI_ML/ |
| **Ne Zaman** | AI/ML görevi gerektiğinde |
| **Neden** | standardize etmek için |
| **Nasıl** | Skill adımlarını takip ederek |

# Claude Code — ReYMeN Orchestration Guide

Delegate coding tasks to [Claude Code](https://code.claude.com/docs/en/cli-reference) (Anthropic's autonomous coding agent CLI) via the ReYMeN terminal. Claude Code v2.x can read files, write code, run shell commands, spawn subagents, and manage git workflows autonomously.

## Important

This guide is a navigation index. For Windows-specific orchestration details (VS Code bridge, VT stack, clipboard injection, focus management), load the dedicated reference:

```
skill_view(name="claude-code", file_path="references/windows-orchestration-bridge.md")
```

## Two Modes

| Mode | When to Use | Key File |
|------|-------------|----------|
| **VS Code GUI Bridge** | User wants to see changes in VS Code, or `claude` CLI unavailable | `references/windows-orchestration-bridge.md` |
| **CLI Print Mode** | Fully autonomous, no approval needed, terminal-only | `claude-code-cli-autonomous` skill |

## Orchestration Pattern

```
🧠 ReYMeN (analysis + strategy)
   → 1. Scan code, find issue, determine fix strategy
   → 2. Prepare structured task prompt (files + what to fix)
   → 3. Send to Claude Code (via VS Code bridge or CLI pipe)
🛠️ Claude Code (implements fix + runs tests)
🔍 ReYMeN (verify result + save as skill/memory)
```
