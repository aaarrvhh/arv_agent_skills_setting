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
| **當前主要專案** | `無` | 當前正在進行或優先執行的專案目錄 |
| **工作空間結構** | `wrkSpace_ai/antigravity_wrkSpace.code-workspace` | 管理各子專案的核心工作空間設定 |

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

## Developer Preferences
- **Architecture Philosophy**: I prefer heavily offloading tasks to local Python tools rather than relying on pure LLM generation. 
- **Tool Development**: When I ask you to automate a task (e.g., firmware analysis, log monitoring), you should automatically design and implement it as a reusable Python tool/script or MCP server first, rather than just giving me a one-off text explanation.

## 備忘錄與環境

- **MCP Servers 集成**:
  - **PMS AutoReport**: `PMS_AutoReport_teddy20260505/src/mcp_server.py`
  - **Discord Connection**: `discord_connection/src/mcp_server.py`
- **Skill 載入原則**:
  - 存放於根目錄 `skills/` 與 `.agent/skills_internal/`、`.agent/skills_external/`。
  - 嚴格遵守 **按需加載 (Load-on-Demand)**，不得隨意遍歷。

- **Git 與指令執行規範**:
  - 嚴禁在修改或新增檔案後自動執行任何 Git 操作（包括 `git status`、`git add`、`git commit`、`git push` 等），以避免打擾用戶審批。
  - 所有 Git 操作必須在用戶於對話中明確下達指示後方可執行。

