# Agent Hooks — 自動開工／收工

呢兩個 shell hook 會令 Hermes 喺每個 session 開始時自動執行 `hermes-startup-handover`，
喺 session 結束時自動執行 `hermes-shutdown-handover`。

## 檔案

- `startup-handover.py` — `pre_llm_call` hook，只喺新 session 嘅第一個 turn 注入 startup skill 內容。
- `shutdown-handover.py` — `on_session_end` hook，session 完結時 background 跑 shutdown skill。

## 安裝步驟

1. 複製兩個 script 到 `~/.hermes/agent-hooks/`，並加執行權：

```bash
cp extras/agent-hooks/*.py ~/.hermes/agent-hooks/
chmod +x ~/.hermes/agent-hooks/*.py
```

2. 喺 `~/.hermes/config.yaml`（或你嘅 profile `config.yaml`）加入：

```yaml
hooks:
  pre_llm_call:
    - command: /Users/YOUR_USERNAME/.hermes/agent-hooks/startup-handover.py
      timeout: 30
  on_session_end:
    - command: /Users/YOUR_USERNAME/.hermes/agent-hooks/shutdown-handover.py
      timeout: 60
hooks_auto_accept: true
```

> 注意：`command` 必須用**絕對路徑**，`~` 唔會自動展開。

3. 允許 hook（非 TTY 環境必需）：

```bash
hermes hooks list
hermes hooks doctor
```

或者手動寫入 `~/.hermes/shell-hooks-allowlist.json`：

```json
{
  "approvals": [
    {"event": "pre_llm_call", "command": "/Users/YOUR_USERNAME/.hermes/agent-hooks/startup-handover.py"},
    {"event": "on_session_end", "command": "/Users/YOUR_USERNAME/.hermes/agent-hooks/shutdown-handover.py"}
  ]
}
```

4. 驗證：

```bash
hermes hooks test pre_llm_call --payload-file /tmp/first-turn.json
```

可用呢個 payload 測試：

```json
{
  "hook_event_name": "pre_llm_call",
  "session_id": "test-session",
  "user_message": "hi",
  "extra": {"is_first_turn": true, "model": "kimi-k2.7-code", "platform": "cli"}
}
```

成功會見到一段注入嘅 startup handover context。

## 防 recursion 機制

- `shutdown-handover.py` 會設定 `HERMES_SHUTDOWN_HANDOVER=1`，避免子 session 再次觸發 shutdown hook。
- 同時設定 `HERMES_STARTUP_HANDOVER=skip`，避免子 session 觸發 startup hook。

## 注意

- `on_session_end` 喺 CLI 入面會喺你 `/exit` 或 Ctrl+C 時觸發；喺 Telegram/Discord gateway 會喺 session timeout 或 `/new` 時觸發。
- Shutdown 會 background 跑一個 one-shot `hermes chat -q`，唔會阻塞你現有 session。
