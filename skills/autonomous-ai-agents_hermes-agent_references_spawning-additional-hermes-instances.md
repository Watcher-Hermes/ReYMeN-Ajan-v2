---
name: autonomous-ai-agents_hermes-agent_references_spawning-additional-ReYMeN-instances
description: Spawning Additional ReYMeN Instances
title: "Autonomous Ai Agents ReYMeN Agent References Spawning Additional ReYMeN Instances"
version: 1.0.0
---


| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI/ML mühendisi |
| **Ne** | Spawning Additional ReYMeN Instances |
| **Nerede** | AI_ML/ |
| **Ne Zaman** | AI/ML görevi gerektiğinde |
| **Neden** | standardize etmek için |
| **Nasıl** | Skill adımlarını takip ederek |

## Spawning Additional ReYMeN Instances

Run additional ReYMeN processes as fully independent subprocesses — separate sessions, tools, and environments.

### When to Use This vs delegate_task

| | `delegate_task` | Spawning `ReYMeN` process |
|-|-----------------|--------------------------|
| Isolation | Separate conversation, shared process | Fully independent process |
| Duration | Minutes (bounded by parent loop) | Hours/days |
| Tool access | Subset of parent's tools | Full tool access |
| Interactive | No | Yes (PTY mode) |
| Use case | Quick parallel subtasks | Long autonomous missions |

### One-Shot Mode

```
terminal(command="ReYMeN chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)
