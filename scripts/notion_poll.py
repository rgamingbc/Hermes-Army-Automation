#!/usr/bin/env python3
"""
Poll a Notion database for rows whose last_edited_time is newer than the stored
watermark. Prints a concise summary to stdout so Hermes can deliver it via cron.

Environment variables:
  NOTION_API_KEY     - Internal integration token (starts with ntn_ or secret_)
  NOTION_DATABASE_ID - 32-character database ID

Watermark file:
  ~/.hermes/.notion_poll_watermark.json

Rate limit: one query per run, sleeping ≥ 0.34 s before the API call so bursts
stay under 3 req/sec.
"""

import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
WATERMARK_PATH = os.path.expanduser("~/.hermes/.notion_poll_watermark.json")


def load_watermark() -> str | None:
    if not os.path.exists(WATERMARK_PATH):
        return None
    try:
        with open(WATERMARK_PATH, "r", encoding="utf-8") as f:
            return json.load(f).get("last_edited_time")
    except Exception:
        return None


def save_watermark(timestamp: str) -> None:
    os.makedirs(os.path.dirname(WATERMARK_PATH), exist_ok=True)
    with open(WATERMARK_PATH, "w", encoding="utf-8") as f:
        json.dump({"last_edited_time": timestamp}, f)


def notion_request(url: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        },
        method="POST" if payload else "GET",
    )
    # Stay under 3 requests per second.
    time.sleep(0.34)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_title(row: dict) -> str:
    props = row.get("properties", {})
    for value in props.values():
        if value.get("type") == "title":
            titles = value.get("title", [])
            if titles:
                return titles[0].get("plain_text", row["id"])
    return row["id"]


def main() -> int:
    if not API_KEY or not DATABASE_ID:
        print("Error: NOTION_API_KEY and NOTION_DATABASE_ID must be set.", file=sys.stderr)
        return 1

    watermark = load_watermark()
    payload = {"page_size": 100}
    if watermark:
        payload["filter"] = {
            "timestamp": "last_edited_time",
            "last_edited_time": {"after": watermark},
        }

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    result = notion_request(url, payload)
    rows = result.get("results", [])

    if not rows:
        print(f"No new/updated Notion rows since {watermark or 'start'}.")
        return 0

    newest = max(r["last_edited_time"] for r in rows)

    for row in rows:
        title = extract_title(row)
        edited = row["last_edited_time"]
        created = row.get("created_time", "")
        kind = "NEW" if created and created > watermark else "UPD"
        print(f"{kind}: {title} | {edited} | {row.get('url', '')}")

    save_watermark(newest)
    print(f"Total: {len(rows)} row(s). Watermark -> {newest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
