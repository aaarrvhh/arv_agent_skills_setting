---
name: skill_path_policy
description: 規範全工作空間之安全憑證存取策略與限制
---

# 技能：路徑與安全憑證策略 (Path & Security Policy)

此技能定義了在全工作空間中，所有涉及安全憑證 (Authentication, Tokens, IDs) 的讀取標準與路徑隱私策略。

## 🎯 核心原則

1. **集中式憑證獲取 (Centralized Credential Resolution)**
   - 往後所有專案遇到需要讀取密碼、Token、API Key 或特定帳號 ID 時，**嚴禁**在程式碼中自行寫死 (hardcode) 安全資料夾 (如 `private_security`) 的路徑。
   - **嚴禁硬編碼絕對路徑**：無論是工作空間根目錄 (`f:\...`) 或 `dump_info` 目錄，都禁止寫死在程式中，必須透過 `.agent/path_policy.py` 動態取得。
   - 所有憑證解析，**必須且只能**透過引入 `dump_info` 目錄內的 `dudu_byby.py` 進行取得。

2. **資料提供限制 (Data Exposure Restrictions)**
   - `dump_info` 內的工具 (如 `dudu_byby.py`) 僅允許對外部提供純資料 (Scalar values)，例如：
     - `URL`
     - `Token`
     - `ID`
   - **【嚴格禁止】** `dump_info` 的任何模組向外部呼叫者提供任何檔案系統的實體路徑 (File path)。底層的安全索引與儲存庫結構必須完全封裝在 `dump_info` 內部，不得對外洩漏。

## 🛠️ 實作與使用規範

當要求 Agent 撰寫或重構需要憑證的程式碼時，應遵循以下模式：
```python
import sys
import os

# 動態尋找 .agent 目錄並匯入 path_policy (嚴禁寫死絕對路徑)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 根據腳本深度向上推導至 .agent (視腳本所在位置調整)
agent_dir = os.path.abspath(os.path.join(current_dir, "..", "..", ".agent")) 
if agent_dir not in sys.path:
    sys.path.append(agent_dir)
import path_policy

if path_policy.DUMP_INFO_PATH not in sys.path:
    sys.path.append(path_policy.DUMP_INFO_PATH)
import dudu_byby

# 正確：僅取得 Token 或 ID
token = dudu_byby.get_credential('service_name', 'TOKEN_KEY')

# 錯誤示範 (嚴禁)：
# file_path = dudu_byby.get_config_path('service_name')  <- 絕對禁止提供此類介面
```
