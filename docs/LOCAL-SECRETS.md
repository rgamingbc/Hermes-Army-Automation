# 本地 Secret 管理規範

> 所有敏感資料（密碼、API key、Server creds、登入憑證）**只儲存在本地**，唔上雲、唔入 public repo。

---

## 1. 主要儲存位置

| 類型 | 位置 | 權限 |
|------|------|------|
| Hermes secrets | `~/.hermes/.env` | `chmod 600`（只有 owner 可讀寫） |
| 憑證索引 | `~/Documents/Hermes Vault/System/Assistant/secrets-index.md` | 明文，但只記名稱/用途，唔記值 |
| 項目相關 creds | `~/.hermes/.env` 為主，索引指向 Obsidian | 同上 |

---

## 2. 命名規則

所有 secret 用一致命名：

```
<SERVICE>_<ACCOUNT>_USERNAME
<SERVICE>_<ACCOUNT>_PASSWORD
<SERVICE>_<ACCOUNT>_URL
<SERVICE>_<ACCOUNT>_NOTES
```

例子：

```bash
CROWN_M473_USERNAME=ccc38a
CROWN_M473_PASSWORD=BBcc1122
CROWN_M473_URL=https://m473.mos077.com
CROWN_M473_NOTES=登入後「快速設定」要按否，留意 viewport 唔好遮住個按鈕
```

---

## 3. 當用戶提供新 creds 時嘅流程

1. 立即 append 到 `~/.hermes/.env`
2. 用 `chmod 600` 確保權限
3. 同時更新 `~/Documents/Hermes Vault/System/Assistant/secrets-index.md`
4. 唔反問用戶點存、唔上傳雲端

---

## 4. Obsidian 索引範本

```markdown
---
date: 2026-07-14
---

# Secret Index

| 服務 | 帳號/用途 | 儲存位置 | 備註 |
|------|-----------|----------|------|
| Crown 舊站 | m473.mos077.com | `~/.hermes/.env` (`CROWN_M473_*`) | 登入後按「否」快速設定 |
```

---

## 5. 注意事項

- `~/.hermes/.env` 係 Hermes 嘅 credential store，Hermes tool 可以經內部渠道讀取。
- 永遠唔好把 `.env` 內容 paste 入 chat 或寫入 repo。
- 如果雲端備份，只備份 `.env` 以外嘅文件；`.env` 必須靠本地備份（Time Machine / 手動）。

---

*本規範由 Hermes 維護，隨新 creds 加入即時更新。*
