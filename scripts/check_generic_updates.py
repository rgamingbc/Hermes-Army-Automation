#!/usr/bin/env python3
"""
Check whether the generic Hermes-Agent-Setup repo has new commits that the
Army repo has not merged yet.

Prints a concise reminder with:
- number of new commits
- a short commit log
- a compare link to review the changes

Designed to be run from a cron job or manually.
"""

import subprocess
import sys
from pathlib import Path

ARMY_DIR = Path(__file__).resolve().parent.parent
UPSTREAM_URL = "https://github.com/rgamingbc/Hermes-Agent-Setup.git"
COMPARE_URL = "https://github.com/rgamingbc/Hermes-Agent-Setup/compare/{}...{}"


def run(cmd, cwd=ARMY_DIR, check=True):
    result = subprocess.run(
        cmd, cwd=cwd, text=True, capture_output=True, check=False
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n{result.stderr.strip()}"
        )
    return result


def ensure_upstream():
    result = run(["git", "remote", "get-url", "upstream"], check=False)
    if result.returncode != 0:
        print("Adding upstream remote for Hermes-Agent-Setup...")
        run(["git", "remote", "add", "upstream", UPSTREAM_URL])


def main() -> int:
    if not (ARMY_DIR / ".git").exists():
        print(f"Error: {ARMY_DIR} does not look like a git repository.", file=sys.stderr)
        return 1

    ensure_upstream()
    run(["git", "fetch", "upstream", "main"])

    local = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    upstream = run(["git", "rev-parse", "upstream/main"]).stdout.strip()

    if local == upstream:
        print("✅ 通用設定 Hermes-Agent-Setup 已經係最新，無需更新。")
        return 0

    base = run(["git", "merge-base", "HEAD", "upstream/main"]).stdout.strip()
    count = run(
        ["git", "rev-list", "--count", f"{base}..upstream/main"]
    ).stdout.strip()
    log = run(
        ["git", "log", "--oneline", "-10", f"{base}..upstream/main"]
    ).stdout.strip()
    compare = COMPARE_URL.format(base[:12], upstream[:12])

    print(f"⚠️ 通用設定 Hermes-Agent-Setup 有 {count} 個新 commit 未 merge 到 Army repo：")
    print()
    print(log)
    print()
    print(f"對比連結：{compare}")
    print()
    print("建議做法：")
    print(f"  cd {ARMY_DIR}")
    print("  git checkout main")
    print("  git pull origin main")
    print("  git merge upstream/main")
    print("  # 解決衝突後 push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
