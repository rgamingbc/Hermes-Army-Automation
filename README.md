# Hermes Army Automation

Army Team 專用 Hermes 自動化設定。通用 Hermes 設定透過 `git subtree` 引入，唔會同 Army 專用檔案混埋，亦唔會 divergence。

## 結構

```
Hermes-Army-Automation/
├── README.md                         # 呢份文件
├── scripts/
│   ├── setup-army-team.sh            # 一鍵開箱腳本
│   └── check_generic_updates.py      # 檢查通用 repo 更新
├── skills/
│   └── custom/
│       └── army-ceo-delegate/        # Army CEO 委派 skill
├── templates/
│   └── army-profiles/                # army-hq / marketing / dev / research 模板
├── docs/
│   └── telegram-topics-tutorial.md   # Telegram Topics 教學
└── vendor/
    └── hermes-agent-setup/           # git subtree 引入嘅通用設定
```

## 開箱（一次性）

```bash
cd ~
gh repo clone rgamingbc/Hermes-Army-Automation
cd Hermes-Army-Automation
./scripts/setup-army-team.sh
```

`setup-army-team.sh` 會做：
1. 用 `vendor/hermes-agent-setup/install-skills.sh` 安裝通用 skills。
2. 將 `army-ceo-delegate` skill 複製到 `~/.hermes/skills/custom/`。
3. 建立 `army-hq`、`army-marketing-head`、`army-dev-head`、`army-research-head` 四個 profile。
4. 複製 profile 模板，並將 `/Users/chloe` 路徑換成你嘅 `$HOME`。
5. 建立 `army` kanban board。
6. 如果有 `KIMI_API_KEY`、`TELEGRAM_BOT_TOKEN`、`TELEGRAM_ALLOWED_USERS` 環境變數，會自動替換 placeholder。

### 手動填入 API keys / tokens

執行完腳本後，**一定要**檢查以下檔案：

```bash
~/.hermes/profiles/{army-hq,army-marketing-head,army-dev-head,army-research-head}/.env
~/.hermes/profiles/{army-hq,army-marketing-head,army-dev-head,army-research-head}/config.yaml
```

最少要填：
- `.env`：`KIMI_API_KEY`、`TELEGRAM_BOT_TOKEN`、`TELEGRAM_ALLOWED_USERS`
- `config.yaml`：`auxiliary.vision.api_key`（如果你用 Kimi，通常同 `KIMI_API_KEY` 一樣）

如果你用緊唔同嘅 model provider（例如 OpenRouter、Gemini），請將 `config.yaml` 嘅 `model` 區塊同 `auxiliary.vision` 改成對應設定。

每個 profile 應該有自己獨立嘅 Telegram bot token。setup script 支援 per-profile env var：

```bash
ARMY_HQ_TELEGRAM_BOT_TOKEN=...
ARMY_MARKETING_HEAD_TELEGRAM_BOT_TOKEN=...
ARMY_DEV_HEAD_TELEGRAM_BOT_TOKEN=...
ARMY_RESEARCH_HEAD_TELEGRAM_BOT_TOKEN=...
```

如果冇設 per-profile，會 fallback 用通用 `TELEGRAM_BOT_TOKEN`。

### 驗證

```bash
for p in army-hq army-marketing-head army-dev-head army-research-head; do
  ~/.local/bin/hermes --profile "$p" skills list | grep army-ceo-delegate
  ~/.local/bin/hermes --profile "$p" kanban show
done
```

## 可選：啟用 YOLO mode / EXEC_ASK（高風險！）

預設 `.env` template **唔會**開啟呢兩個選項。如果你需要非互動 automation（例如 cron job 唔想每次被問），可以手動加入，但**必須清楚風險**。

### HERMES_YOLO_MODE=1

 Hermes 遇到 `rm`、覆蓋檔案、改系統設定等危險指令時，會**直接執行，唔再問**。適合全自動環境，但極高危，尤其 Telegram bot 對外開放時。

### HERMES_EXEC_ASK=false

喺 Telegram / Discord 等 messaging gateway 中，Hermes 執行工具前通常會問「確定？」。設 `false` 後會**直接執行**。同樣只適合受控自動化環境。

啟用方法：喺每個 profile 嘅 `.env` 加入：

```bash
HERMES_YOLO_MODE=1
HERMES_EXEC_ASK=false
```

> ⚠️ 只喺你 100% 信任所有可觸發 bot 嘅人同流程時先好開。

## Telegram Topics 工作空間

跟住 [`docs/telegram-topics-tutorial.md`](docs/telegram-topics-tutorial.md) 開 `Army HQ` group，啟用 Topics，關閉 bot Group Privacy，再開 `#general`、`#marketing`、`#dev`、`#research`、`#ceo-delegation`。

## 更新通用設定

通用 repo 有新內容時，`check_generic_updates.py` 會提醒你。

手動檢查：

```bash
python3 scripts/check_generic_updates.py
```

建議每星期用 Hermes cron 檢查一次：

```bash
~/.local/bin/hermes --profile army-hq cron create \
  --name check-generic-updates \
  --schedule "0 9 * * 1" \
  --command "python3 /Users/$USER/Hermes-Army-Automation/scripts/check_generic_updates.py" \
  --deliver telegram
```

見到提醒後，喺 Army repo root 執行：

```bash
git subtree pull --prefix=vendor/hermes-agent-setup \
  https://github.com/rgamingbc/Hermes-Agent-Setup.git main --squash
```

## Secret 管理

- 所有 secret 值統一擺喺 `~/.hermes/.env` 或 profile `.env`。
- Obsidian vault 只記索引，唔記值。
- 詳情見 `vendor/hermes-agent-setup/LOCAL-SECRETS.md`。

## 客製化

- Army 專用 skill：改 `skills/custom/`，再跑一次 `setup-army-team.sh` 或手動複製。
- Profile 模板：改 `templates/army-profiles/`。
- 開新 team：fork 呢個 repo，改 `templates/army-profiles/` 入面嘅名同 placeholder。

## License

MIT
