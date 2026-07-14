# Hermes Agent Setup

通用 Hermes Agent 設定指南與可重用 skills。

適用於任何新 Hermes agent / 團隊成員，唔限於單一 project。

## 內容

- `README.md` — 通用 onboarding、設定檢查清單、skill 安裝方法
- `skills/` — 可重用 skill 副本，已按 Hermes 嘅 `<category>/<skill-name>/SKILL.md` 結構擺放
  - `autonomous-ai-agents/hermes-memory-architecture` — 3-tier 記憶架構
  - `autonomous-ai-agents/hermes-setup-checklist` — 新 profile / team 開箱檢查清單
  - `note-taking/obsidian` — Obsidian vault 讀寫指引
  - `productivity/hermes-startup-handover` — 每次開工先讀 handover
  - `productivity/hermes-shutdown-handover` — 每次收工更新 handover
  - `software-development/site-clone-css-validation` — 新舊網站 CSS/DOM 比較 workflow

## 快速開始

### 1. 安裝 Hermes Agent

按照官方指引安裝 Hermes Agent。

### 2. Clone 本 repo

```bash
cd ~
gh repo clone rgamingbc/Hermes-Agent-Setup
```

### 3. 安裝本 repo 嘅 skills

```bash
cd ~/Hermes-Agent-Setup
./install-skills.sh
```

或者手動複製到 `~/.hermes/skills/`：

```bash
rsync -av skills/ ~/.hermes/skills/
```

### 4. 設定新 profile

```bash
hermes profile create my-team-member
```

然後編輯 `~/.hermes/profiles/my-team-member/config.yaml`，加入基本設定：

```yaml
model:
  default: kimi-k2.7-code
  provider: kimi-coding
  base_url: https://api.kimi.com/coding/v1
  supports_vision: true

toolsets:
  - kanban

skills:
  external_dirs:
    - /Users/chloe/.hermes/skills/custom
```

再編輯 `~/.hermes/profiles/my-team-member/.env`：

```bash
KIMI_API_KEY=sk-...
HERMES_KANBAN_BOARD=army
OBSIDIAN_VAULT_PATH="/Users/$USER/Documents/Hermes Vault"
```

### 5. 建立 Obsidian Vault 結構

```bash
vault="/Users/$USER/Documents/Hermes Vault"
mkdir -p "$vault/Daily"
mkdir -p "$vault/System/Assistant/logs"
mkdir -p "$vault/Work/Projects"
mkdir -p "$vault/Personal/Projects"
mkdir -p "$vault/People"
mkdir -p "$vault/Inbox"
```

### 6. 驗證

```bash
hermes --version
hermes --profile my-team-member config show
hermes --profile my-team-member skills list
hermes --profile my-team-member kanban show
```

## 通用設定重點

| 設定 | 作用 | 位置 |
|---|---|---|
| `model.default` | 用邊個模型 | `config.yaml` |
| `model.supports_vision` | 開啟圖片原生識別 | `config.yaml` |
| `toolsets: [kanban]` | 開啟 kanban 工具 | `config.yaml` |
| `skills.external_dirs` | 共享 custom skills | `config.yaml` |
| `HERMES_KANBAN_BOARD` | 指定共用 board | `.env` |
| `OBSIDIAN_VAULT_PATH` | Obsidian vault 路徑 | `.env` |
| `TELEGRAM_BOT_TOKEN` | Telegram bot | `.env` |

## 使用 skills

啟動 Hermes 後，可以直接用 slash command：

```
/hermes-setup-checklist
/hermes-startup-handover
/hermes-shutdown-handover
```

或者 preload：

```bash
hermes -s hermes-startup-handover
```

## 自動開工／收工（可選）

想 Hermes 喺每個 session 開始／結束時自動執行 startup / shutdown handover，
請參考 [`extras/agent-hooks/README.md`](extras/agent-hooks/README.md) 安裝兩個 shell hook。

重點：

1. 複製 `extras/agent-hooks/*.py` 到 `~/.hermes/agent-hooks/`。
2. 喺 `~/.hermes/config.yaml` 加入 `hooks:` 區塊，指向絕對路徑。
3. 設定 `hooks_auto_accept: true`（非 TTY 環境必需）。
4. 預設只喺 `cli` 同 `telegram` platform 觸發，避免 cron / tool session 燒 token。

## Secret 管理

- 所有 secret 嘅值統一擺喺 `~/.hermes/.env`。
- Obsidian vault 只記索引（`System/Assistant/secrets-index.md`），唔記值。
- 詳情見 [`LOCAL-SECRETS.md`](LOCAL-SECRETS.md)。

## 客製化

- 修改 `skills/` 入面嘅 SKILL.md 後，重新執行 `./install-skills.sh` 即可同步到 `~/.hermes/skills/`。
- 如果有項目專用內容，請開新 skill 放喺 `~/.hermes/skills/custom/`，唔好把通用 skill 變成項目專用。

## 注意

- 一個 Telegram bot token 只可以有一個 live consumer，唔好共用。
- `site-clone-css-validation` 嘅 browser 工具選擇要配合你嘅 `CLAUDE.md` / 全局指引。
- Hermes built-in memory 只有 ~2,200 字符，長期資料請存到 Obsidian vault。

## License

MIT
