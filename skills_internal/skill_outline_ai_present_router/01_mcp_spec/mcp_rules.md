# 💥 MCP 技術規範 (Deep Spec)

此文件為 `skill_outline_ai_present_router` 的深度引用模組，專注於 Workspace 內各個 MCP Server 的核心機制、各 Project 間 MCP Server 的關聯比較，以及與 AI Agent 的信號交互關係。

---

## 📐 關聯圖 (Relationship Diagram) 繪製規範
本模組的每一頁都必須包含關聯圖，且特別強調「**各 Project MCP Server 之間的橫向關聯**」：
- **格式**：使用 Markdown 純文字的 ASCII 方框圖或箭頭流程圖。
- **核心要求**：關聯圖必須清楚呈現：
    - AI Agent 如何同時與多個 MCP Server 交互。
    - 各 MCP Server 的角色定位與服務邊界。
    - MCP Server 之間是否有協作關係（例如：先查 PMS 報工狀態，再透過 Discord 通知）。
- **禁止事項**：關聯圖中不得包含程式碼邏輯或函數實作細節。

---

## 🔑 核心概念（背景知識）

- **Stateless JSON-RPC**：Agent 與 MCP Server 之間採用無狀態的 JSON-RPC 協議溝通，每次工具調用獨立、原子性強。
- **Dynamic Tool Discovery**：Agent 啟動時透過 `initialize` 指令動態探索各 Server 暴露的工具列表，無需硬編碼知識。
- **Stdio Transport**：本地 MCP Server 使用 stdio 作為傳輸層，提供高安全性的進程間通訊。
- **`build_mcp_server` 對齊設計哲學**：邏輯解耦（Client vs Tool 分層）、安全憑證管理（本地 GUI 輸入）、主動診斷（get_auth_status）與敏感抹除（wipe_sensitive_data）。

---

## 📅 深度渲染頁面規劃 (共 5 頁)

### 📊 Page 1: MCP 技術原理與 AI Agent 的多伺服器交互架構
- **介紹深度**：詳細描述。
- **內容焦點**：介紹 MCP 協議的核心運作原理，並重點說明 AI Agent 如何「同時配置並管理多個 MCP Server」的架構設計。
- **要求**：
    - 說明 JSON-RPC 無狀態協議如何確保每個工具調用的原子性與可靠性。
    - 說明 Agent 在 `mcp_config.json` 中同時配置 `PMS AutoReport` 與 `Discord Connection` 兩個 MCP Server 的機制。
    - 解釋 AI Agent 如何在同一個對話中，按需切換調用不同 MCP Server 的工具，而不產生狀態污染。
    - **必須繪製**：展示 AI Agent 同時連接多個 MCP Server 的**多伺服器交互架構關聯圖**：
        ```
        [ AI Agent (LLM) ]
               |
               | JSON-RPC via stdio
               |
        +------+-------+
        |              |
        v              v
        [ PMS AutoReport    ]     [ Discord Connection ]
          MCP Server              MCP Server
          (報工工具池)              (機器人控制工具池)
               |                        |
               v                        v
        [ PMS 報工系統 ]        [ Discord 平台後端 ]
          (外部 Web 服務)         (長連接 Bot 服務)
        ```

### 🤖 Page 2: PMS AutoReport MCP Server 深度剖析
- **介紹深度**：詳細描述。
- **內容焦點**：從 AI 架構的角度深度介紹 `PMS_AutoReport_teddy20260505` 的 MCP Server 設計，聚焦在「AI 如何感知並使用它」而非程式碼實作。
- **要求**：
    - 說明此 MCP Server 向 AI 暴露的**工具語義**（工具名稱的意義、參數的業務含義、呼叫的觸發條件）。
    - 解釋 AI 如何依賴 `get_auth_status` 進行執行前自我診斷，以及 `trigger_auth_gui` 如何在不洩漏密碼的前提下完成憑證驗證。
    - 說明 `wipe_sensitive_data` 工具如何保障 AI 在完成任務後的隱私安全清理。
    - **必須繪製**：`PMS AutoReport MCP Server` 的**工具池結構與 AI 調用邏輯關聯圖**，展示各工具之間的依賴關係（例如：必須先調用 `get_auth_status`，才能安全執行 `submit_project_report`）。

### 💬 Page 3: Discord Connection MCP Server 深度剖析
- **介紹深度**：詳細描述。
- **內容焦點**：從 AI 架構的角度深度介紹 `discord_connection` 的 MCP Server 設計，聚焦在「AI 如何控制一個長連接的非同步進程」。
- **要求**：
    - 說明此 MCP Server 向 AI 暴露的**工具語義**（`start_bot`、`stop_bot`、`get_bot_status` 各自的業務含義與調用時機）。
    - 解釋「AI 作為進程守護者」的角色：AI 如何透過 MCP 感知 Discord Bot 的執行狀態，並在異常時主動重新啟動。
    - 說明此 MCP Server 與 PMS AutoReport MCP Server 的**角色差異**：一個是「任務提交型」，一個是「常駐服務控制型」。
    - **必須繪製**：`Discord Connection MCP Server` 的**進程生命週期控制關聯圖**，展示 AI 如何透過工具調用控制 Discord Bot 的啟動、運行與關閉狀態機。

### 🔗 Page 4: 跨 Project MCP Server 橫向比較與角色定位
- **介紹深度**：詳細描述。
- **內容焦點**：以**橫向比較**的視角，呈現 Workspace 中兩個 MCP Server 在設計哲學、角色定位、工具性格上的根本差異，說明「為什麼需要兩個不同的 Server，而不是合併成一個」。
- **要求**：
    - **橫向比較分析**：對比兩個 MCP Server 在以下維度的差異與設計理由：
        - **服務類型**：任務提交型 (PMS) vs 常駐服務控制型 (Discord)
        - **連接模式**：無狀態的一次性請求 vs 需要感知長連接的存活狀態
        - **安全機制**：憑證驗證前置的必要性 vs 只需確認進程存活
        - **工具的語義複雜度**：提交需要業務資料完整性 vs 控制只需要指令明確性
    - 說明 `mcp_config.json` 如何作為「多伺服器配置中樞」，統一宣告並管理兩個 MCP Server 的啟動路徑與環境參數。
    - 說明 AI Agent 如何依據**任務語義**自動選擇調用哪一個 Server（工作報告相關 → PMS；訊息推送相關 → Discord）。
    - **必須繪製**：**雙 MCP Server 角色定位對比關聯圖**，以並列方式展示兩個 Server 各自的工具池內容、服務對象與角色邊界：
        ```
        ┌─────────────────────┐     ┌─────────────────────┐
        │  PMS AutoReport     │     │  Discord Connection  │
        │  MCP Server         │     │  MCP Server         │
        │─────────────────────│     │─────────────────────│
        │  類型：任務提交型    │     │  類型：常駐控制型    │
        │  工具：             │     │  工具：             │
        │  - get_auth_status  │     │  - get_bot_status   │
        │  - trigger_auth_gui │     │  - start_bot        │
        │  - submit_report    │     │  - stop_bot         │
        │  - wipe_data        │     │─────────────────────│
        │─────────────────────│     │  服務對象：         │
        │  服務對象：         │     │  Discord 長連接後端  │
        │  PMS 報工 Web 服務  │     └─────────────────────┘
        └─────────────────────┘
                    ↑ 兩者均由 mcp_config.json 統一管理 ↑
        ```

### 🌐 Page 5: 跨 Project MCP Server 協作場景與全局關聯大圖
- **介紹深度**：詳細描述。這是整個 MCP 模組中**最重要的一頁**，單獨佔據完整一頁以確保全局大圖有足夠的呈現空間。
- **內容焦點**：以具體的**協作場景**說明兩個 MCP Server 如何在 AI 的統一調度下，完成跨系統的複合型任務，並以一張大型關聯圖呈現整個 MCP 生態的完整面貌。
- **要求**：
    - **協作場景深度說明**：以「AI 完成每日自動化工作流」為例，描述以下跨 Server 協作鏈路的完整流程與決策邏輯：
        - Step 1：AI 調用 PMS Server 的 `get_auth_status` 確認憑證就緒。
        - Step 2：AI 讀取今日工作記錄，調用 `submit_project_report` 完成自動上報。
        - Step 3：AI 調用 Discord Server 的 `get_bot_status` 確認 Bot 存活。
        - Step 4：AI 透過 Discord Bot 將「今日報工完成」推送至指定頻道，完成閉環通知。
    - 說明這個協作場景的**價值主張**：打破系統孤島，AI 成為跨系統的智能調度中樞。
    - **必須繪製**：這是整份報告中**最重要、最需要完整空間**的一張全局關聯大圖，必須同時清楚呈現：
        - `mcp_config.json` 作為配置入口的頂層位置
        - AI Agent 作為調度中樞連接兩個 MCP Server 的雙向信號流
        - 兩個 MCP Server 各自連接後端系統的服務邊界
        - 跨 Server 協作的完整數據流向（PMS 結果 → AI 決策 → Discord 通知）

