---
name: User Profile
last_updated: 2026-05-19
---

# 用戶偏好存檔 (USER.md)

> "個性化你的開發體驗，讓我更了解你的工作方式。"

---

## 基本資訊

| 項目 | 內容 | 說明 |
| :--- | :--- | :--- |
| **開發者名稱** | `arv` | 本工作空間的開發者主要稱呼 |
| **當前主要專案** | `ppt_ai_present` | 當前正在進行或優先執行的專案目錄 |
| **工作空間結構** | `wrkSpace_antigravity/workspace_ai_antigravity.code-workspace` | 管理各子專案的核心工作空間設定 |

## 技術偏好

- **前端/UI 框架**:
  - 優先使用 **Vanilla CSS** & **Vanilla HTML/JS** 以維持最大彈性與極致美學控制。
  - 除非有明確要求，否則不隨意引入第三方 UI 庫。
- **視覺與美學**:
  - 追求 **Premium & Modern UI**（極簡、漸層、玻璃擬態、流暢微動畫）。
  - 拒絕粗糙的 Default 預設樣式。
- **程式碼風格**:
  - **全英文開發**：代碼內部的命名、Log、註解等均維持 100% 英文。
  - **Clean Code**：追求高可讀性、重構性與模組化。

## 備忘錄與環境

- **MCP Servers 集成**:
  - **PMS AutoReport**: `PMS_AutoReport_teddy20260505/src/mcp_server.py`
  - **Discord Connection**: `discord_connection/src/mcp_server.py`
- **Skill 載入原則**:
  - 存放於根目錄 `skills/` 與 `.agent/skills_internal/`、`.agent/skills_external/`。
  - 嚴格遵守 **按需加載 (Load-on-Demand)**，不得隨意遍歷。

- **Git 與指令執行規範**:
  - 嚴禁在每次修改或新增檔案後自動執行 `git status` 或其他狀態檢查指令，以避免頻繁打擾用戶審批。
  - 僅在完成階段性工作、或用戶明確要求進行儲存庫同步時，才執行 Git 相關指令。

