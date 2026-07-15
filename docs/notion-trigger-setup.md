# Notion → Hermes 觸發器（輪詢）

用 Notion database 做 army team 的「任務輸入」：每次有人新增／修改一列，Hermes 就會收到 Telegram 通知。

> 注意：Notion iOS／Android app 都可以建立同修改 database，手機改嘅內容輪詢一樣會捉到。
> 個人免費版已經夠用；唔需要 webhook。

---

## 1. 建立 Notion integration

1. 開 https://www.notion.so/my-integrations （登入緊你嘅 workspace）。
2. 撳 **New integration**。
3. 名稱填 `Hermes Army`，Capabilities 留 **Read** 同 **Read user information**。
4. 複製 **Internal Integration Token**（通常以 `ntn_` 或 `secret_` 開頭）。

```
+------------------------------------------+
|  My integrations                           |
|  [ + New integration ]                     |
|                                            |
|  Name: Hermes Army                         |
|  Associated workspace: Your Workspace      |
|  Capabilities: [x] Read content            |
|                [x] Read user information   |
|                                            |
|  [ Submit ]                                |
|                                            |
|  Internal Integration Token:               |
|  ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    |
+------------------------------------------+
```

---

## 2. 將 integration 連到 database

1. 開你想監察嘅 Notion database。
2. 撳右上角 `...` → **Connect to** → 揀 `Hermes Army`。

> 如果漏咗呢步，API 會回 404，即使個 page 真係存在。

---

## 3. 取得 database ID

Database URL 例子：

```
https://www.notion.so/workspace/1a2b3c4d5e6f7g8h9i0j1a2b3c4d5e6f?v=...
```

URL 入面 32 個字符嗰串就係 **database ID**：

```
1a2b3c4d5e6f7g8h9i0j1a2b3c4d5e6f
```

---

## 4. 將憑證放入 army-hq profile

編輯 `~/.hermes/profiles/army-hq/.env`：

```bash
NOTION_API_KEY=ntn_...
NOTION_DATABASE_ID=1a2b3c4d...
```

---

## 5. 測試輪詢腳本

```bash
python3 /Users/chloe/.hermes/scripts/notion_poll.py
```

預期會輸出最近新增／修改嘅 row，例如：

```
NEW: Q3 rebrand brief | 2026-07-15T09:12:00.000Z | https://notion.so/...
Total: 1 row(s). Watermark -> 2026-07-15T09:12:00.000Z
```

---

## 6. 註冊 Hermes cron job

讓 Hermes 每 10 分鐘檢查一次，並將結果送到 Telegram：

```bash
~/.local/bin/hermes --profile army-hq cron create \
  --name notion-to-hermes \
  --schedule "*/10 * * * *" \
  --command "python3 /Users/chloe/.hermes/scripts/notion_poll.py" \
  --deliver telegram
```

想密啲可以改 `*/5`，想疏啲可以改 `*/30`。

---

## 7. 驗證

1. 喺 Notion database 改一列。
2. 等一個 interval（例如 10 分鐘）。
3. 確認 Telegram 收到通知。

```bash
~/.local/bin/hermes --profile army-hq cron list
```

應該見到 `notion-to-hermes`。

---

## 常見問題

| 問題 | 原因 | 解法 |
|---|---|---|
| API 回 404 | integration 未 connect 到 database | 撳 `...` → Connect to → Hermes Army |
| 收唔到 cron 通知 | `NOTION_API_KEY` 未 set 或錯 | `grep NOTION_API_KEY ~/.hermes/profiles/army-hq/.env` |
| 每次 rerun 都出晒所有 row | watermark 檔案遺失 | 腳本會從最新 row 重新建立 watermark |
| 頻繁 hit rate limit | interval 太密 | 改 `*/30` 或更疏 |

---

## 相關檔案

- 輪詢腳本：[`../scripts/notion_poll.py`](../scripts/notion_poll.py)
- Telegram Topics 教學：[`telegram-topics-tutorial.md`](telegram-topics-tutorial.md)
