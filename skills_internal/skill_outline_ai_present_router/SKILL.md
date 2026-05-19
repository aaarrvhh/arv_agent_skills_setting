# 🎨 Skill: Outline AI Present Router

引導 AI 提取當前 Workspace 架構並生成**深度且詳細**的 Markdown 大綱報告。本技能採取「模組化引用」，請 AI 在生成特定頁面時，主動讀取對應的子技能。

---

## 🎯 核心功能
1. **深度架構分析 (Deep Architectural Analysis)**：全方位深入分析 Workspace 的 AI 架構（`.agent`, `skills`, `wrkSpace_ai`, MCP Server 等），著重說明各層級之間的**關聯性、依賴關係與信號流向**。
2. **深度大綱生成 (Deep Outline)**：產出詳細且具深度的 Markdown 大綱報告。
    - **原則**：
        - ✅ 專注介紹 **Workspace 架構邏輯** 與 **AI 設定 (SOUL, GUIDE, cursorrules 等) 的關聯性**。
        - ✅ **每個 Topic 必須包含至少一個關聯圖 (Relationship Diagram)**，使用 ASCII 或 Markdown 格式呈現元件之間的關係。
        - ❌ 嚴禁介紹任何 Python、C、C++ 或其他語言的**程式碼實作細節**（包含函數定義、Class 架構、迴圈邏輯等）。
        - ❌ 嚴禁複製貼上任何程式碼片段。
    - **銜接**：此大綱將作為 `skill_html_ai_present_renderer` 的輸入。
3. **授權後分流**：在展示大綱並獲得同意後，負責「呼叫」對應的渲染技能。

---

## 📐 關聯圖 (Relationship Diagram) 繪製規範
在每個 Topic 的介紹中，AI **必須** 根據實際讀取到的 Workspace 內容，自行繪製關聯圖。關聯圖的格式要求如下：
- **格式**：使用 Markdown 純文字的 ASCII 方框圖或箭頭流程圖。
- **內容**：必須呈現該 Topic 的**核心元件**、**元件之間的關係方向**（讀取、觸發、控制、輸出等），以及**與其他 Topic 的銜接點**。
- **範例格式**（參考，AI 應依據實際情況自行繪製）：
    ```
    [ .cursorrules 路由總機 ]
           |  讀取
           v
    [ .agent/WORKSPACE_GUIDE_en.md ]
           |  定義優先 Focus
           v
    [ ppt_ai_present/ ]  <--- 當前主要產出目標
    ```

---

## 📑 Topic 頁面規劃

### Topic 0: 全景概覽 — Antigravity Workspace 鳥瞰圖 [1 Page]
- **介紹深度**：高度精煉的全景總覽，作為整份報告的「第一印象頁」。
- **內容焦點**：在正式深入各層級之前，先以一張大圖呈現整個工作空間的架構與核心元件間的關係，讓讀者一眼掌握全局。
- **要求**：
    - 介紹 Workspace 的 5 大核心層次（路由層、中樞層、技能層、執行層、產出層）。
    - **必須繪製**：完整呈現 `.cursorrules` → `.agent` → `skills/` → `mcp_server` → `ppt_ai_present` 的全局鳥瞰架構關聯圖，各元件之間標明關係類型（觸發、讀取、驅動、輸出等）。

### Topic 1: 封面與核心導航 (.cursorrules) [1 Page]
- **介紹深度**：詳細描述。
- **內容焦點**：工作空間的路由總機與行為邊界。
- **要求**：
    - 直接分析根目錄的 `.cursorrules` 規則邏輯，說明它如何「定義 AI 的第一行為」。
    - 解釋 `.cursorrules` 與 `.agent/WORKSPACE_GUIDE_en.md` 的啟動關係。
    - **必須繪製**：`.cursorrules` 觸發 AI 初始化讀取流程的關聯圖。

### Topic 2: 核心大腦 (.agent) [2 Pages]

#### Page A: 三文件職責分工與 AI 人格定義
- **介紹深度**：詳細描述。
- **內容焦點**：分別解析 `.agent` 資料夾內三份核心文件各自的職責定位。
- **要求**：
    - `SOUL.md`：定義 AI 的人格語氣（繁體中文、專業親切）、美學標準（視覺至上）與開發規範（全英文 code）。
    - `USER.md`：儲存用戶的個性化偏好（技術棧、MCP 設定狀態、工作習慣），使 AI 能記住特定開發者的工作方式。
    - `WORKSPACE_GUIDE_zh.md / en.md`：定義初始化時的讀取優先順序，明確哪些資料夾是首要 Focus 目標。
    - **必須繪製**：三文件各自職責的橫向對比關聯圖，展示「人格 (SOUL) ← → 偏好 (USER) ← → 導航 (GUIDE)」的分工架構。

#### Page B: 三文件協同影響 AI 行為的動態關聯
- **介紹深度**：詳細描述。
- **內容焦點**：說明三份文件不是孤立的，而是**層層協作**共同塑造出 AI 在每次對話中的決策流程。
- **要求**：
    - 說明 AI 在收到用戶指令時，依序讀取 SOUL（語氣基準）→ USER（偏好記憶）→ GUIDE（任務導向）的情境感知邏輯。
    - 解釋 WORKSPACE_GUIDE 中「首次開啟時 Focus on `.agent` 與 `ppt_ai_present`」的設計意圖與初始化意義。
    - **必須繪製**：三文件的**動態協作影響流程圖**（輸入指令 → SOUL 限定語氣 → USER 調取偏好 → GUIDE 設定任務方向 → AI 行為輸出）。

### Topic 3: 神經延伸 (MCP Server)
- **介紹深度**：依據子技能規則決定頁數，每頁詳細描述。
- **內容焦點**：透過 Model Context Protocol 實現本地與外部工具的動態綁定，以及工具與 Workspace 專案的對應關係。
- **💥 AI 執行指令**：請在此步驟**主動讀取並載入 `./01_mcp_spec/mcp_rules.md`**，並依據該文件內的「深度渲染規範」決定頁面數與內容深度產出。
- **關聯圖規定**：每頁必須包含一個 MCP Server 與專案資料夾、AI Agent 之間關係的關聯圖。

### Topic 4: 模組化武器庫 (Skills 二元分流)
- **介紹深度**：依據子技能規則決定頁數，每頁詳細描述。
- **內容焦點**：
    - 區分團隊自製的原生技能與社群生態技能。
    - 介紹各技能與 Workspace 專案的對應關係（Folder-to-Skill Mapping）。
    - 說明技能加載的生命週期與 AI Context 管理策略。
- **💥 AI 執行指令**：**主動讀取並載入 `./02_skills_management/flow_rules.md`**，並依據該文件內的「深度渲染規範」決定頁面數與內容深度產出。
- **關聯圖規定**：必須包含一頁「跨專案與技能全局關聯圖」，精確呈現 Folder ➔ Skill 的映射。

### Topic 5: 全局情境感知 (wrkSpace_ai) [2 Pages]

#### Page A: 多資料夾工作區整合結構
- **介紹深度**：詳細描述。
- **內容焦點**：解析 `wrkSpace_ai` 如何作為「目錄整合中樞」，將分散的多個專案統一納入單一 VS Code Workspace 進行管理。
- **要求**：
    - 說明 `antigravity_wrkSpace.code-workspace` 如何宣告並整合所有 8 個 Active Folders（`.agent`、`skills`、`ppt_ai_present`、`PMS_AutoReport_teddy20260505`、`discord_connection`、`NPCM845D_DTS`、`private_security`、`wrkSpace_ai` 本身）。
    - 解釋各資料夾在生態系中的角色定位（中樞腦、技能庫、執行器、產出區等）。
    - **必須繪製**：以`wrkSpace_ai` 為核心，輻射呈現 8 個 Active Folders 的結構歸屬與各自角色的關聯圖。

#### Page B: 全局端到端數據流閉環
- **介紹深度**：詳細描述。
- **內容焦點**：呈現整個 Antigravity Workspace 從「用戶指令輸入」到「最終簡報落盤」的完整端到端數據流路徑。
- **要求**：
    - 串聯所有 Topic 的關鍵節點，完整呈現信號如何在各層之間流動。
    - 涵蓋：用戶指令 → `.cursorrules` 路由 → `.agent` 中樞感知 → `skills/` 技能加載 → `mcp_server` 工具執行 → 最終產出至 `ppt_ai_present/`。
    - 同時標示旁路數據流：`PMS_AutoReport` 與 `discord_connection` 的外部系統連接節點。
    - **必須繪製**：完整的**端到端全局數據流關聯圖**，這是整份報告中最重要的一張全景大圖，必須清楚標示每個節點與流向箭頭的語義。

---

## 🛠️ 使用規範
- **產出格式**：Markdown（深度版，包含關聯圖）。
- **存放路徑**：所有產出物必須存放於 `ppt_ai_present/`。
- **檔名格式**：`[Name]_YYYYMMDD_HHMM`。
- **禁止清單**：嚴禁洩漏任何 Python, C, C++ 或其他語言的程式碼實作細節。
- **執行前置**：展示大綱並詢問「是否呼叫 HTML Renderer 進行視覺渲染？」。

## 📜 關聯技能
- `japanese-hand-drawn-editorial-ppt-skill`
- `skill_html_ai_present_renderer`
