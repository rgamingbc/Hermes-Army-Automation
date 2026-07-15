# Hermes Army Automation

呢個 repo 包含兩部分：

1. **通用 Hermes Agent 設定** — 適用於任何新 Hermes agent / 團隊成員。
2. **Army Team 專用自動化** — `army-hq`、`army-marketing-head`、`army-dev-head`、`army-research-head` 嘅協作設定：Kanban、CEO delegation skill、Telegram Topics 教學、Notion 輪詢觸發器。

目標：之後開新 Team Bot 可以直接 fork / clone 呢個 repo，改幾個 placeholder 就開工。

## 內容

### 通用 skills

- `skills/autonomous-ai-agents/hermes-memory-architecture` — 3-tier 記憶架構
- `skills/autonomous-ai-agents/hermes-setup-checklist` — 新 profile / team 開箱檢查清單
- `skills/note-taking/obsidian` — Obsidian vault 讀寫指引
- `skills/productivity/hermes-startup-handover` — 每次開工先讀 handover
- `skills/productivity/hermes-shutdown-handover` — 每次收工更新 handover
- `skills/software-development/site-clone-css-validation` — 新舊網站 CSS/DOM 比較 workflow
- `skills/RESOLVER.md` + `skills/manifest.json` — gbrain 解析用
- `templates/RESOLVER-full.md` + `templates/manifest-full.json` — 完整 routing template

### Army 專用

- `skills/custom/army-ceo-delegate/SKILL.md` — CEO 委派 protocol
- `templates/army-profiles/<profile>/{config.yaml,.env}` — 四個 army profile 模板
- `docs/telegram-topics-tutorial.md` — Telegram Topics 群組教學
- `docs/notion-trigger-setup.md` — Notion integration + 輪詢觸發器
- `scripts/notion_poll.py` — Notion database 輪詢腳本

## 快速開始（通用）

```bash
cd ~
gh repo clone rgamingbc/Hermes-Army-Automation
cd Hermes-Army-Automation
./install-skills.sh
```

`install-skills.sh` 會備份舊嘅 `~/.hermes/skills/RESOLVER.md`，再同步 repo 嘅 skills。

## Army Team 開箱

### 1. 建立 profiles

```bash
for p in army-hq army-marketing-head army-dev-head army-research-head; do
  hermes profile create "$p"
done
```

### 2. 複製模板

```bash
cp templates/army-profiles/army-hq/config.yaml ~/.hermes/profiles/army-hq/config.yaml
cp templates/army-profiles/army-hq/.env       ~/.hermes/profiles/army-hq/.env
# 對其餘三個 profile 做同樣動作
```

### 3. 填 placeholder

- `config.yaml` 入面 `auxiliary.vision.api_key` → 換成實際 Kimi key。
- `.env` 入面 `KIMI_API_KEY`、`TELEGRAM_BOT_TOKEN`、`TELEGRAM_ALLOWED_USERS`。
- `army-hq/.env` 再填 `NOTION_API_KEY`、`NOTION_DATABASE_ID`。

### 4. 建立共用 kanban board

```bash
~/.local/bin/hermes kanban boards create army \
  --name "Army Team" \
  --description "Cross-department army team board" \
  --icon 🎖️ \
  --switch \
  --default-workdir /Users/chloe/hermes-army/launch-2026
```

### 5. 安裝 CEO delegation skill

```bash
mkdir -p ~/.hermes/skills/custom
cp -r skills/custom/army-ceo-delegate ~/.hermes/skills/custom/
```

### 6. 驗證

```bash
for p in army-hq army-marketing-head army-dev-head army-research-head; do
  ~/.local/bin/hermes --profile "$p" skills list | grep army-ceo-delegate
  ~/.local/bin/hermes --profile "$p" kanban show
done
```

## Telegram Topics 工作空間

跟住 [`docs/telegram-topics-tutorial.md`](docs/telegram-topics-tutorial.md) 開 `Army HQ` group，啟用 Topics，關閉 bot Group Privacy，再開 `#general`、`#marketing`、`#dev`、`#research`、`#ceo-delegation`。

記住：**一個 Telegram bot token 只可以有一個 live consumer**，每個 profile 要用自己嘅 bot。

## Notion → Hermes 觸發器

跟住 [`docs/notion-trigger-setup.md`](docs/notion-trigger-setup.md) 建立 integration、連 database、填 `.env`、測試腳本，再註冊 cron：

```bash
~/.local/bin/hermes --profile army-hq cron create \
  --name notion-to-hermes \
  --schedule "*/10 * * * *" \
  --command "python3 /Users/chloe/.hermes/scripts/notion_poll.py" \
  --deliver telegram
```

## Secret 管理

- 所有 secret 值統一擺喺 `~/.hermes/.env` 或 profile `.env`。
- Obsidian vault 只記索引，唔記值。
- 詳情見 [`LOCAL-SECRETS.md`](LOCAL-SECRETS.md)。

## gbrain resolver / manifest

Repo 自帶 `skills/RESOLVER.md` 同 `skills/manifest.json`。如果你有大量 gbrain routing，參考 `templates/RESOLVER-full.md` 合併而唔係覆蓋。

安裝後驗證：

```bash
cd ~
gbrain check-resolvable --json
gbrain doctor --json
```

## 客製化

- 通用 skill 改 `skills/`，再跑 `./install-skills.sh`。
- Army 專用 skill 改 `skills/custom/`。
- 開新 team 時 fork 呢個 repo，改 `templates/army-profiles/` 入面嘅名同 placeholder。

## License

MIT
