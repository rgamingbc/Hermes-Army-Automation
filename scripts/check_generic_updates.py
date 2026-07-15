#!/usr/bin/env python3
"""
Check whether the vendored Hermes-Agent-Setup (under vendor/hermes-agent-setup)
is behind the upstream generic repo.

Prints a reminder with:
- number of new commits
- a short commit log
- the exact git subtree pull command to update
"""

import subprocess
import sys
from pathlib import Path

ARMY_DIR = Path(__file__).resolve().parent.parent
VENDOR_DIR = ARMY_DIR / "vendor" / "hermes-agent-setup"
UPSTREAM_URL = "https://github.com/rgamingbc/Hermes-Agent-Setup.git"
COMPARE_URL = "https://github.com/rgamingbc/Hermes-Agent-Setup/compare/{}...{}"


def run(cmd, cwd=VENDOR_DIR, check=True):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n{result.stderr.strip()}"
        )
    return result


def is_ancestor(ancestor, descendant):
    result = run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant], check=False
    )
    return result.returncode == 0


def main() -> int:
    if not VENDOR_DIR.exists():
        print(f"Error: {VENDOR_DIR} not found.", file=sys.stderr)
        print("This script expects the generic repo to be imported via git subtree:")
        print(
            "  git subtree add --prefix=vendor/hermes-agent-setup "
            f"{UPSTREAM_URL} main --squash"
        )
        return 1

    remotes = run(["git", "remote"]).stdout.strip().splitlines()
    if "origin" not in remotes:
        run(["git", "remote", "add", "origin", UPSTREAM_URL])

    run(["git", "fetch", "origin", "main"])

    local = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    upstream = run(["git", "rev-parse", "origin/main"]).stdout.strip()

    if local == upstream or is_ancestor(upstream, local):
        print("✅ vendor/hermes-agent-setup 已經係最新，無需更新。")
        return 0

    base = run(["git", "merge-base", "HEAD", "origin/main"]).stdout.strip()
    count = run(
        ["git", "rev-list", "--count", f"{base}..origin/main"]
    ).stdout.strip()
    log = run(
        ["git", "log", "--oneline", "-10", f"{base}..origin/main"]
    ).stdout.strip()
    compare = COMPARE_URL.format(base[:12], upstream[:12])

    print(f"⚠️ 通用設定 Hermes-Agent-Setup 有 {count} 個新 commit 未更新到 Army repo：")
    print()
    print(log)
    print()
    print(f"對比連結：{compare}")
    print()
    print("更新做法（喺 Army repo root 執行）：")
    print("  git subtree pull --prefix=vendor/hermes-agent-setup ")
    print(f"    {UPSTREAM_URL} main --squash")
    return 0


if __name__ == "__main__":
    sys.exit(main())
