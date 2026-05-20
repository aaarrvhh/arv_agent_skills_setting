# 工作空間導引規範 (WORKSPACE_GUIDE_zh.md)

此文件定義了 Agent 進入此多專案工作空間後的行為準則、目錄讀取優先順序與安全性規範。

---

## 1. 資料夾讀取優先順序 (工作流引導)

當本工作空間開啟時，Agent 必須 **嚴格按照以下優先級** 進行探索與對焦，避免盲目遍歷：

### 第一優先級 (核心上下文)
1. **`.agent`**: 優先載入核心指令（`.init_agent.md`）、用戶偏好（`USER.md`）與靈魂規範（`SOUL.md`）。

### 第二優先級 (架構與專案資料夾)
2. **`wrkSpace_ai`**: 探索工作空間的基礎結構定義。
3. **專案開發資料夾**:
   - `ppt_ai_present` (簡報生成與 AI 整合專案)
   - `PMS_AutoReport_teddy20260505` (自動工作日誌系統)
   - `discord_connection` (Discord 機器人整合系統)
   - `NPCM845D_DTS` (硬體描述與 DTS 專案)
   - `private_security` (安全合規與隱私抹除模組)
   - `merge_uboot_` (Bootloader 與 U-Boot 韌體合併工具)
   - `dump_info` (系統日誌與資訊傾印)

---

## 2. MCP Server 配置清單

目前工作空間已註冊並可運作的 Model Context Protocol 伺服器：

- **PMS AutoReport**: `PMS_AutoReport_teddy20260505/src/mcp_server.py`
- **Discord Connection**: `discord_connection/src/mcp_server.py`
- **Github Connection**: `.agent/skills_internal/skill_github/fastmcp_github.py`

---

## 3. SKILL 加載與執行規則

> [!CAUTION]
> **嚴格的安全限制 (Security Boundary)**
> - **加載路徑**: `skills/` (根目錄)
> - **預設禁令**: Agent **嚴禁** 在初始化或未獲得授權時，主動遍歷、讀取或載入 `skills/` 資料夾下的任何檔案。

### 觸發載入條件：
1. **按需加載 (Load-on-Demand)**: 僅當用戶明確要求時（例如：*"請學習 skill_build_mcp_server 技能"*），才可載入特定技能。所有技能皆須遵循按需加載，無自動加載之例外專案。

---
*最後更新：2026-05-19*


