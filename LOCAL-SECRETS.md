# LOCAL-SECRETS.md

Hermes Agent Setup 嘅 secret 管理規則。

## 核心原則

1. **所有 secret 嘅值統一擺喺 `~/.hermes/.env`。**
2. **Obsidian vault 只記索引，唔記值。**
3. **除非用戶明確要求，否則唔用 macOS Keychain**（automation 較麻煩，而且跨 profile 難共享）。

## 實際做法

### 新增 secret

1. 將 secret 寫入 `~/.hermes/.env`（或對應 profile 嘅 `.env`）：
   ```bash
   echo 'MY_API_KEY=sk-...' >> ~/.hermes/.env
   ```
2. 喺 Obsidian vault 更新索引：
   - `~/Documents/Hermes Vault/System/Assistant/secrets-index.md`
3. 喺對應 project handover 記錄：
   - 變數名、用途、擺放位置。

### 開工時

Startup handover 會檢查：
- `~/.hermes/.env` 入面有冇 handover 引用嘅變數
- 如果搵唔到，即刻通知用戶：「老公，XXX creds 搵唔到，要你再俾一次。」

### 收工時

Shutdown handover 會：
- 將今次用過嘅新 secret 寫入 `~/.hermes/.env`
- 更新 `secrets-index.md`
- 喺 handover 記錄 storage location

## 為什麼唔用 Keychain

- macOS Keychain 需要 GUI approval，headless / automation 環境會卡住。
- Hermes 同各 profile 讀取 `.env` 最一致。
- 備份 `.hermes` 資料夾就等於備份所有設定同 secret（請自行加密備份）。

## 例外

只有當用戶主動講「呢個 secret 我要用 Keychain」先可以用 Keychain，並且要在 handover 寫明原因。

---

*本規則適用於 default profile 同所有 army profiles。*
