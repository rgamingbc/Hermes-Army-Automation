#!/usr/bin/env python3
"""pre_llm_call shell hook: auto-run hermes-startup-handover on first turn.

Reads the startup handover skill from the active HERMES_HOME and injects its
instructions as ephemeral context on the first turn of every new session.
Skips itself when spawned by the shutdown handover hook (HERMES_STARTUP_HANDOVER=skip).
"""

import json
import os
import re
import sys


def _skip() -> None:
    print("{}")
    sys.exit(0)


if os.environ.get("HERMES_STARTUP_HANDOVER") == "skip":
    _skip()

try:
    payload = json.load(sys.stdin)
except Exception:
    _skip()

if payload.get("hook_event_name") != "pre_llm_call":
    _skip()

extra = payload.get("extra", {})
if not extra.get("is_first_turn"):
    _skip()

home = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
skill_path = os.path.join(home, "skills", "productivity", "hermes-startup-handover", "SKILL.md")
if not os.path.exists(skill_path):
    _skip()

text = open(skill_path, encoding="utf-8").read()
body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL).strip()
if not body:
    _skip()

context = (
    "[AUTOMATIC STARTUP HANDOVER — execute these instructions before replying to the user]\n\n"
    + body
)
print(json.dumps({"context": context}))
