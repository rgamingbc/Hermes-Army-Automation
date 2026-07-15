---
date: 2026-07-14
project: Hermes Agent Setup
type: tracker
---

# Hermes Ecosystem Tools Tracker

> 記錄 Hermes Agent 相關 ecosystem tools 嘅安裝狀態、位置、驗證方法。
> 每次開工/收工都要快速核對一次，確保狀態同記錄一致。

---

## 1. 工具狀態總覽

| 工具 | 狀態 | 位置 | 驗證指令 | 備註 |
|------|------|------|----------|------|
| `agent-browser` | ✅ 運作中 | `/opt/homebrew/bin/agent-browser` | `which agent-browser` | Hermes 內建 browser 工具底層 |
| `ponytail` skill | ✅ 已安裝 | `~/.hermes/skills/software-development/ponytail/` | `ls ~/.hermes/skills/software-development/ponytail/` | Lazy-senior coding rules |
| **Hermes WebUI** | ✅ 運行中 | `~/.hermes/tools/hermes-webui` | `curl -s http://127.0.0.1:8789/health` | port 8789 listening, health ok |
| **agentic-stack** | ✅ 已整合 | `~/.hermes/.agent/` | `python3 ~/.hermes/.agent/tools/show.py` | Portable brain layer |
| **awesome-hermes-agent** | ✅ 已複製 | `~/.hermes/tools/awesome-hermes-agent` | `ls ~/.hermes/tools/awesome-hermes-agent` | Resource collection |
| **hermes-agent-self-evolution** | ✅ 已安裝 | `~/.hermes/tools/hermes-agent-self-evolution` | `python3.11 -c "import evolution; print('OK')"` | DSPy + GEPA optimizer |
| **gbrain** | ⚠️ warnings（resolver 已修復） | `~/.gbrain` | `gbrain doctor --json` | Health score 65；resolver_health ✅；skill_conformance ✅；剩餘 warnings 全部可選 |
| **repomix** | ✅ 已安裝 | `~/.hermes/tools/repomix` | `~/.hermes/bin/repomix --version` | v1.16.1，已入 PATH via `~/.hermes/bin` |
| **Vision 修復** | ✅ 已設定 | `~/.hermes/config.yaml` 第 167 行 | `grep -n "vision" ~/.hermes/config.yaml` | 使用 Kimi OpenAI endpoint |

---

## 2. 詳細狀態

### 2.1 agent-browser

- 二進制位置：`/opt/homebrew/bin/agent-browser`
- 用途：Hermes browser 工具底層，用於網站 capture 同自動化
- 驗證：`which agent-browser`
- 狀態：✅ 可用

### 2.2 ponytail skill

- 位置：`~/.hermes/skills/software-development/ponytail/SKILL.md`
- 用途：lazy-senior-dev coding rules
- 驗證：`ls ~/.hermes/skills/software-development/ponytail/`
- 狀態：✅ 已安裝

### 2.3 Hermes WebUI

- 位置：`~/.hermes/tools/hermes-webui`
- 狀態：✅ 運行中
- 監聽：`http://127.0.0.1:8789`
- 驗證：
  ```bash
  lsof -i :8789
  curl -s http://127.0.0.1:8789/health
  ```
- 日誌：`~/.hermes/webui.log`

### 2.4 agentic-stack

- 位置：`~/.hermes/.agent/`
- 狀態：✅ 已整合
- 驗證：
  ```bash
  python3 ~/.hermes/.agent/tools/show.py
  ```
- 注意：adapter 已安裝喺 Hermes profile，但 `~/.agent/` 係獨立 brain root。

### 2.5 awesome-hermes-agent

- 位置：`~/.hermes/tools/awesome-hermes-agent`
- 狀態：✅ 已複製
- 驗證：
  ```bash
  ls -la ~/.hermes/tools/awesome-hermes-agent
  ```

### 2.6 hermes-agent-self-evolution

- 位置：`~/.hermes/tools/hermes-agent-self-evolution`
- 狀態：✅ 已安裝
- 驗證：
  ```bash
  python3.11 -c "import evolution; print('OK')"
  ```
- 注意：必須用 Python 3.11。

### 2.7 gbrain

- 位置：`~/.gbrain`
- 狀態：⚠️ `warnings`（health score **65**）
- 驗證：
  ```bash
  gbrain doctor --json
  gbrain check-resolvable --json
  ```
- 注意：
  - `~/.hermes/.env` 已加入 `~/.bun/bin`，PATH 問題已修復。
  - `~/.hermes/skills/RESOLVER.md` 已修正：移除不存在嘅引用、補齊實際路徑（`gbrain/*`、`productivity/*` 等）、加入 `computer-use` / `dogfood` / `yuanbao` trigger rows。
  - `~/.hermes/skills/manifest.json` 已建立，skill conformance 通過。
  - `resolver_health` 同 `skill_conformance` 已變成 ✅。
  - 剩餘 warnings 全部屬可選項目，唔影響基本運作：
    - `embeddings`：未建立 embedding，keyword-only mode 可用。
    - `jsonb_integrity` / `pgvector`：PGLite 限制，正常。
    - `retrieval_reflex_health`：retrieval-reflex policy skill 未裝，可選。
    - `pack_upgrade_available`：有新 pack 可升級，可選。
    - `takes_count`：takes.bootstrap_enabled=false，可選。
    - `ze_embedding_health`：未設 `ZEROENTROPY_API_KEY`。

### 2.8 repomix

- 位置：`~/.hermes/tools/repomix`
- 狀態：✅ 已安裝（v1.16.1）
- PATH：`~/.hermes/bin/repomix`
- 驗證：
  ```bash
  ~/.hermes/bin/repomix --version
  ```
- 使用：
  ```bash
  ~/.hermes/bin/repomix /path/to/repo
  ```

### 2.9 Vision 修復

- 設定位置：`~/.hermes/config.yaml` 第 167 行
- 狀態：✅ 已設定
- 設定內容：
  ```yaml
  auxiliary:
    vision:
      provider: custom
      base_url: https://api.kimi.com/coding/v1
      model: kimi-k2.7-code
      timeout: 120
      api_key: «redacted»
  ```
- 驗證：
  ```bash
  grep -n "vision" ~/.hermes/config.yaml
  ```
  或
  ```bash
  grep -n "auxiliary.vision" ~/.hermes/config.yaml
  ```
- 注意：API key 來自 `~/.hermes/.env` 嘅 `KIMI_API_KEY`。`auth.json` 亦有 credential pool entry。

---

## 3. 已知 Warning / 待跟進

| 項目 | 嚴重程度 | 狀態 | 備註 |
|------|----------|------|------|
| gbrain embedding key 未設定 | 低 | 可選 | keyword-only mode 可用，semantic search 需要 key |
| gbrain retrieval-reflex 未 install | 低 | 可選 | 需要時再裝 |
| gbrain pgvector / jsonb integrity warning | 低 | PGLite 正常 | PGLite 無獨立 pgvector 插件 |
| gbrain pack upgrade 可用 | 低 | 可選 | `gbrain-base-v2` 可升級 |
| gbrain takes bootstrap | 低 | 可選 | `takes.bootstrap_enabled=false` |
| Hermes update 可用 | 低 | 待低峰期處理 | `hermes update --check` 顯示落後 origin/main |
| gbrain resolver_health / skill_conformance | ✅ 已修復 | 完成 | `gbrain check-resolvable` 0 errors 0 warnings |

---

## 4. 每日驗證 Checklist

開工時：
- [ ] Hermes WebUI health check 過到
- [ ] `gbrain doctor --json` status 為 `warnings` 或更好（resolver_health ✅）
- [ ] `gbrain check-resolvable --json` 0 errors
- [ ] repomix 版本正常
- [ ] 必要時測試一張圖 vision_analyze

收工時：
- [ ] 如有工具狀態變更，更新呢份 tracker
- [ ] 把完成事項記錄入 handover

---

## 5. 更新日誌

| 日期 | 內容 | 更新者 |
|------|------|--------|
| 2026-07-14 | 建立 tracker，確認所有工具已安裝並記錄實際狀態 | Hermes |
| 2026-07-14 | 正式把 repomix 由 `/tmp/repomix` 遷移到 `~/.hermes/tools/repomix` 並入 PATH | Hermes |
| 2026-07-14 | 更新 gbrain 狀態：health score 65→40，resolver_health fail，manifest.json 未建立 | Hermes |
| 2026-07-14 | 更新 Vision 設定行數為 167，驗證指令加入 `grep -n "auxiliary.vision"` | Hermes |
| 2026-07-14 | 收工驗證：Hermes WebUI/agentic-stack/agent-browser/repomix/ponytail 正常；gbrain 需先 export PATH；Vision 位於第 5 同 167 行 | Hermes |
| 2026-07-14 | 更新 tracker：gbrain 驗證需要載入 `.bun/bin` PATH，加入 gbrain PATH 未載入問題 | Hermes |
| 2026-07-14 | 修復 gbrain PATH：喺 `~/.hermes/.env` 加入 `~/.bun/bin`；gbrain doctor 可直接執行 | Hermes |
| 2026-07-14 | 加入自動 handover hook platform guard（只限 cli/telegram）同 unified secret 規則 | Hermes |
| 2026-07-14 | 徹底修復 gbrain resolver：修正 `~/.hermes/skills/RESOLVER.md` 錯誤路徑、補齊 trigger rows、建立 `manifest.json`；`gbrain check-resolvable` 0 errors；health score 由 40 升至 65 | Hermes |

---

*本 tracker 應隨工具安裝/狀態變更即時更新。*
