---
name: software-development_node-inspect-debugger_references_debugging-ReYMeN-ui-tui
description: Debugging ReYMeN ui-tui
title: "Software Development Node Inspect Debugger References Debugging ReYMeN Ui Tui"
version: 1.0.0
---


| 5N1K | Açıklama |
|:----:|:---------|
| **Kim** | AI/ML mühendisi |
| **Ne** | Debugging ReYMeN ui-tui |
| **Nerede** | AI_ML/ |
| **Ne Zaman** | AI/ML görevi gerektiğinde |
| **Neden** | standardize etmek için |
| **Nasıl** | Skill adımlarını takip ederek |

## Debugging ReYMeN ui-tui

The TUI is built Ink + tsx. Two common scenarios:

### Debugging a single Ink component under dev

`ui-tui/package.json` has `npm run dev` (tsx --watch). Add `--inspect-brk` by running tsx directly:

```bash
cd /home/bb/ReYMeN-agent/ui-tui
npm run build    # produce dist/ once so transpile isn't needed on first load
node --inspect-brk dist/entry.js
