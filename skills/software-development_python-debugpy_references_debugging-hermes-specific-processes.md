---
name: software-development_python-debugpy_references_debugging-ReYMeN-specific-processes
description: Debugging ReYMeN-specific Processes
title: "Software Development Python Debugpy References Debugging ReYMeN Specific Processes"
version: 1.0.0
---


| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI/ML mühendisi |
| **Ne** | Debugging ReYMeN-specific Processes |
| **Nerede** | AI_ML/ |
| **Ne Zaman** | AI/ML görevi gerektiğinde |
| **Neden** | standardize etmek için |
| **Nasıl** | Skill adımlarını takip ederek |

## Debugging ReYMeN-specific Processes

### Tests
See Recipe 3. Always add `-p no:xdist` or run single tests without xdist.

### `run_agent.py` / CLI — one-shot
Easiest: add `breakpoint()` near the suspect line, then run `ReYMeN` normally. Control returns to your terminal at the pause point.

### `tui_gateway` subprocess (spawned by `ReYMeN --tui`)
The gateway runs as a child of the Node TUI. Options:

**A. Source-edit the gateway:**
```python
