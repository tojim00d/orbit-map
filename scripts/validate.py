#!/usr/bin/env python3
"""Structure check for the Orbit Map package.

  python3 scripts/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins" / "orbit-map" / "skills"
EXPECTED = {"project-map", "project-diagram"}
FRONTMATTER = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n", re.S)
LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def main() -> int:
    mds = sorted(SKILLS.glob("*/SKILL.md"))
    names = {p.parent.name for p in mds}
    if names != EXPECTED:
        err(f"expected skills {sorted(EXPECTED)}, found {sorted(names)}")

    for md in mds:
        text = md.read_text(encoding="utf-8")
        m = FRONTMATTER.match(text)
        if not m:
            err(f"{md}: missing frontmatter")
            continue
        if f"name: {md.parent.name}" not in m.group(1):
            err(f"{md}: name does not match folder")

    for f in [ROOT / ".claude-plugin" / "marketplace.json",
              ROOT / "plugins" / "orbit-map" / ".claude-plugin" / "plugin.json"]:
        try:
            json.loads(f.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            err(f"{f}: invalid JSON: {exc}")

    if not (ROOT / "docs" / "index.html").is_file():
        err("missing docs/index.html (demo page)")
    if not (ROOT / "LICENSE").is_file():
        err("missing LICENSE")

    for md in [ROOT / "README.md", ROOT / "README.ru.md", ROOT / "AGENTS.md"]:
        text = md.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            if not (md.parent / target.split("#")[0]).exists():
                err(f"{md.name}: broken relative link {target}")

    for junk in ROOT.rglob("*"):
        if junk.name in {".DS_Store", "__pycache__"} or junk.suffix == ".pyc":
            err(f"junk file: {junk.relative_to(ROOT)}")

    for e in errors:
        print("ERROR", e)
    if errors:
        print(f"\nFAILED: {len(errors)} error(s)")
        return 1
    print(f"OK: {len(mds)} skills, manifests, docs and links are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
