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
   - 若為首次使用 Git，自動在該儲存庫層級設定必要的使用者身分資訊：
     - `git config user.email "<email>"`
     - `git config user.name "<username>"`

3. **提交與推播 (Commit & Push)**:
   - 執行 `git remote add origin <github_url>` 加入指定的遠端位址。
   - 執行 `git add .` 將所有檔案加入暫存區。
   - 執行 `git commit -m "<Commit Message> (committed by Antigravity Agent in VS Code)"` 建立提交。
     - **規範**：所有由 Agent 發起或執行的 Commit，必須在 Commit Message 的末尾加註 Signature，說明是由何種 Agent 於何種 IDE 下進行提交。
   - 執行 `git push -u origin main` 將代碼推送到遠端儲存庫。

4. **授權處理 (Authentication Handling)**:
   - 認知到首次執行 `git push` 時，Git Credential Manager 會觸發外部瀏覽器或彈出視窗要求 GitHub 授權。
   - 在執行推播指令時，應妥善設置等待時間，並引導用戶查看畫面上的授權提示，完成後再利用 `command_status` 檢查最終的指令回傳碼 (Exit code 0)。

## 🛠️ 執行時機與使用工具

- **執行時機**：當用戶要求「將這個 folder/資料夾 upload 到 GitHub」時。
- **使用工具**：
  - `run_command`：用於執行環境檢測與一系列的 Git 指令。
  - `command_status`：用於確認背景安裝 (如 winget) 或是等待授權推播指令的最終狀態。
