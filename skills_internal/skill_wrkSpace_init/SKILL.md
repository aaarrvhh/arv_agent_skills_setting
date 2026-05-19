---
name: wrkSpace_init
description: 負責在切換工作空間時，比對專案清單的差異，並自動更新 .agent 目錄下的引導與配置 md 文件。
---

# 技能：工作空間初始化與同步 (Workspace Initialization & Sync)

此技能定義了在切換工作空間或重新載入環境時，Agent 如何自動檢查並對齊專案目錄結構，以確保 `.agent/` 底下的所有導引與偏好設定文件始終與真實磁碟目錄及工作空間結構保持 100% 一致。

## 🎯 核心功能

1. **真實環境探索 (Discovery)**:
   - 掃描工作空間父目錄（例如 `f:\arv_google_antigravity`）下的實際資料夾結構。
   - 讀取系統環境所提供的 active workspaces 清單。

2. **配置清單比對 (Comparison)**:
   - 載入並分析 `.agent/USER.md`、`.agent/WORKSPACE_GUIDE_zh.md` 與 `.agent/WORKSPACE_GUIDE_en.md`。
   - 提取上述文件中記載的專案列表與核心路徑。
   - 比對兩者差異，特別注意：
     - **新專案**：出現在磁碟或 active workspaces 但未被記載於文件中的目錄。
     - **已移除專案**：記載於文件中但磁碟上已不存在的目錄。
     - **大小寫或路徑拼寫差異**：如 `wrkspace_antigravity` 與 `wrkSpace_antigravity` 的大小寫不一致。

3. **自動同步更新 (Auto-Sync)**:
   - 針對有差異的部分，自動修改 `.agent/*.md` 中的對應路徑與清單內容。
   - 保持中英文版引導手冊（`WORKSPACE_GUIDE_zh.md` 與 `WORKSPACE_GUIDE_en.md`）及用戶偏好存檔（`USER.md`）的同步更新。

4. **安全防護邊界 (Security Boundary)**:
   - **嚴格限制**：此同步過程**嚴禁**修改或遍歷任何 `.skills_*`（如 `skills_internal/`、`skills_external/`）目錄底下的內容。所有技能目錄的細部調整必須在之後手動且個別地進行。

## 🛠️ 執行時機與使用工具 (MCP Tool)

- **執行時機**：每次進入工作空間、切換 Active Workspaces、或用戶要求對齊環境配置時。
- **使用工具**：
  AI Agent 不需要透過終端機執行任何 Python 指令，可以直接調用註冊好的全域 MCP 工具 `sync_workspace`：
  1. **唯讀比對 (Dry-run)**：
     調用 `sync_workspace(action="check")` 來比對專案與配置檔的差異。
  2. **自動同步更新 (Auto-Sync)**：
     若發現大小寫拼寫等差異，直接調用 `sync_workspace(action="sync")` 自動修正並更新檔案。
  3. **指定工作空間 (Optional)**：
     可傳入參數 `workspace` 指定特定之 `.code-workspace` 檔名（例如 `workspace_ai_antigravity.code-workspace`）。
- **核心特色**：
  - **極致節省 Token**：AI Agent 無須讀取或載入 Python 原始碼，也不需讀取大篇幅的 Markdown 原文字至 Context 中，僅需透過結構化的 MCP Schema 進行一鍵呼叫，每次初始化可省下數萬個脈絡 Token。
