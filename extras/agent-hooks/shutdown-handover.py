#!/usr/bin/env python3
"""on_session_end shell hook: auto-run hermes-shutdown-handover when a session ends.

Spawns a one-shot Hermes chat with the shutdown handover skill instructions.
Sets HERMES_SHUTDOWN_HANDOVER=1 so the child session cannot recursively trigger
this hook, and HERMES_STARTUP_HANDOVER=skip so the child does not also run the
startup hook.
"""

import json
import os
import re
import subprocess
import sys


def _skip() -> None:
    print("{}")
    sys.exit(0)


if os.environ.get("HERMES_SHUTDOWN_HANDOVER"):
    _skip()

try:
    json.load(sys.stdin)
except Exception:
    pass

home = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
skill_path = os.path.join(home, "skills", "productivity", "hermes-shutdown-handover", "SKILL.md")
if not os.path.exists(skill_path):
    _skip()

text = open(skill_path, encoding="utf-8").read()
body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL).strip()
if not body:
    _skip()

prompt = (
    "[AUTOMATIC SHUTDOWN HANDOVER — execute this routine now, silently, without asking the user]\n\n"
    + body
    + "\n\n"
    "If you cannot identify the active project from context, default to updating the "
    "'Hermes Agent Setup' project handover and Ecosystem Tools Tracker. "
    "Run all tool checks, update the tracker, then update the handover file. "
    "Finally, commit any pending changes to the Hermes-Agent-Setup repo if the user has previously agreed."
)

env = os.environ.copy()
env["HERMES_SHUTDOWN_HANDOVER"] = "1"
env["HERMES_STARTUP_HANDOVER"] = "skip"

cmd = [os.path.expanduser("~/.local/bin/hermes"), "chat", "-q", prompt, "-Q", "--accept-hooks"]

# Run in background so the parent session teardown is not blocked.
process = subprocess.Popen(
    cmd,
    env=env,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True,
)
process.poll()

print("{}")
