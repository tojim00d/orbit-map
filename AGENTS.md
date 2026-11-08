# AGENTS.md — Orbit Map for any coding agent

This repository ships two agent skills as standard `SKILL.md` folders:

- `plugins/orbit-map/skills/project-map/SKILL.md` — interactive one-file HTML project map;
- `plugins/orbit-map/skills/project-diagram/SKILL.md` — static SVG/PNG diagrams.

They are native Claude Code plugin skills, but the instructions are portable: Codex,
Qwen Code, Cursor and any tool that can read a Markdown skill file can use them.

## Use from a non-Claude agent

```bash
./install.sh --skills-dir ~/.agents/skills   # or any directory your agent reads
```

Then ask in words: *"build a project map of this repository"* or *"draw the phases and
steps as an SVG"*. The skills are self-contained; they reference each other and the
project files, never Claude-only tools. Where a skill mentions Claude Code, adapt:

- slash commands are not needed — describe the task in words;
- `${CLAUDE_PLUGIN_ROOT}` = the skill directory where `--skills-dir` copied it;
- subagents: use your agent's delegation tool or do the work inline.

## Full pack

These two skills are part of **Orbit** — 89 skills in one pipeline with shared `.orbit/`
artifacts: https://github.com/tojim00d/Orbit-skills (see its `AGENTS.md`).
