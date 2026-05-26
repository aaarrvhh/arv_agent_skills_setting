---
name: skill_github
description: 負責將本機特定資料夾初始化為 Git 儲存庫，並自動推送到指定的 GitHub 遠端位址。
---

# 技能：GitHub 儲存庫初始化與推播 (GitHub Repository Initialization & Push)

此技能定義了當用戶需要將一個尚未進行版本控制的本機資料夾（例如 `.agent`），上傳至特定的 GitHub 遠端儲存庫時，Agent 應執行的標準操作流程。

## 🎯 核心功能

1. **環境狀態確認 (Environment Check)**:
   - 檢查目標資料夾是否已經是 Git 儲存庫。
   - 檢查系統是否已安裝 Git（透過檢查預設路徑 `C:\Program Files\Git\cmd\git.exe` 或是以 `winget --version` 確認是否能透過包管理員安裝）。
   - 若未安裝，主動提議使用 `winget install --id Git.Git -e --source winget` 進行自動安裝。

2. **Git 初始化與配置 (Git Initialization & Configuration)**:
   - 進入目標資料夾，執行 `git init` 建立本地追蹤。
   - 執行 `git branch -M main` 將預設分支設為 `main`。
   - 確認本地 `core.pager` 設定：檢查本地設定是否為 `cat`，若非 `cat` 則自動設定本地 `git config --local core.pager cat`（**重要**：若使用預設分頁器如 `less`，會導致 Agent CLI 在讀取指令輸出時卡住）。
   - 若為首次使用 Git，自動在該儲存庫層級設定必要的使用者身分資訊：
     - `git config user.email "<email>"`
     - `git config user.name "<username>"`

3. **提交與推播 (Commit & Push)**:
   * **環境分流設計**：
     * **手動執行 (User Mode)**：跳過 `git status`、`git add` 與 `git commit`，直接執行安全推播。
     * **代理執行 (Agent Mode)**：在使用者授權後，自動執行暫存與帶有動態簽名標記的 Commit。
   * **Commit 規範**：所有由 Agent 發起的 Commit，必須於 Commit Message 末端動態加註簽名（例如：` (committed by Antigravity Agent in VS Code)`）。

4. **安全授權與推播 (Secure Authentication & Push)**:
   * **記憶體內認證 (Stateless Auth)**：**嚴禁**將包含 Token 的 URL 寫入本地磁碟之遠端設定（`git remote set-url`），亦無需觸發外部瀏覽器進行 Git Credential Manager 授權。
   * **一次性 Header 注入**：利用 Base64 將 GITHUB_TOKEN 編碼，並透過 `git -c http.extraheader="Authorization: Basic <base64>"` 在執行推播時進行一次性記憶體內授權注入，確保認證安全無殘留。

## 🛠️ 執行時機與使用工具

* **執行時機**：當用戶要求「將這個 folder/資料夾 upload 到 GitHub」時。
* **使用工具**：
  * **輔助腳本 (`git_push_helper.py`)**：支援手動與代理的分流自動化推播。
  * **MCP 全域工具 (`git_push`)**：透過 `fastmcp_github.py` 提供同等安全的指令封裝，便於 Agent 直接呼叫。
  * **`run_command`**：執行 Git 相關狀態確認與推播輔助腳本。
