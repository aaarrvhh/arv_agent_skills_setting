# GitHub 自動推送腳本使用指南 (Manual Run Guide)

本指南說明如何在沒有 AI 輔助的情況下，手動執行 `git_push_helper.py` 腳本，將 `.agent` 目錄的變更自動提交並推送到 GitHub 遠端儲存庫。

## 🎯 腳本功能

`git_push_helper.py` 是一個自動化 Git 工具，它會執行以下操作：
1. 自動讀取本機安全憑證工具（`dudu_byby.py`）中的 `GITHUB_REPO_URL` 與 `GITHUB_TOKEN`。
2. 自動執行 `git status` 與 `git add .`。
3. 建立提交（Commit），並附帶 Signature 標記。
4. 暫時將遠端倉庫的 URL 變更為包含 Token 的授權 URL 以完成 `git push`。
5. 推送完成後，**自動將遠端 URL 還原**，避免金鑰在設定檔中洩露。

---

## 🛠️ 前置需求

在執行腳本前，請確保您的系統符合以下條件：
1. **已安裝 Python 3**（可在終端機執行 `python --version` 確認）。
2. **已安裝 Git**（可在終端機執行 `git --version` 確認）。
3. 已存在有效的憑證解析模組 `dudu_byby.py`（通常位於工作區的 `dump_info` 目錄下）。

---

## 🚀 執行步驟

請開啟命令提示字元（CMD）或 PowerShell，並依據以下步驟執行：

### 步驟 1：開啟終端機並切換至腳本目錄

執行以下指令切換至 `skill_github` 目錄：
```powershell
cd "d:\fxn_arvin\antigravity_ai_\.agent\skills_internal\skill_github"
```

### 步驟 2：執行 Python 腳本

* **使用者自行執行（預設無簽名）**：
  ```powershell
  python git_push_helper.py
  ```
* **Agent 執行（附帶動態簽名）**：
  ```powershell
  python git_push_helper.py --agent "Antigravity Agent in VS Code"
  ```

### 💡 執行時的輸出範例

當您執行腳本時（以使用者自行手動執行為例，僅進行推送，跳過 add/commit），會看到類似以下的終端機輸出，說明每個步驟的執行狀態：
```text
User manual execution detected. Skipping git add and commit. Proceeding directly to push.

Temporarily setting remote origin URL for push...
Running: git remote set-url origin https://<TOKEN_HIDDEN>@github.com/aaarrvhh/arv_agent_skills_setting.git
Pushing changes to origin main...
Running: git push origin main
Push succeeded!

Reverting remote origin URL back to original non-token URL...
Running: git remote set-url origin https://github.com/aaarrvhh/arv_agent_skills_setting.git
```

---

## ⚠️ 注意事項

* **安全性**：此腳本在執行 push 時，會將包含 `GITHUB_TOKEN` 的 URL 短暫寫入 `.git/config`，並在結束時不論成功或失敗都會嘗試將其還原為原本的 URL。請勿在腳本執行中途強制中斷（如按下 `Ctrl + C`），以免還原程序未執行完成。
* **手動還原**：若因意外中斷導致遠端 URL 殘留 Token，您可以手動執行以下指令將遠端 URL 重設：
  ```powershell
  git remote set-url origin https://github.com/aaarrvhh/arv_agent_skills_setting.git
  ```
