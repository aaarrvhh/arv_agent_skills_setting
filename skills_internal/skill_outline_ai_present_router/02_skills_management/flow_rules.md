# 💥 技能管理與關聯規範 (Flow Rules)

此文件為 `skill_outline_ai_present_router` 的深度引用模組，專注於 Antigravity 工作空間中各技能的角色定位、與專案的映射關聯、技能之間的協作關係，以及生命週期治理規範。

---

## 📐 關聯圖 (Relationship Diagram) 繪製規範
本模組的每一頁都必須包含關聯圖，且特別強調「**各技能與 Project 之間的橫向關聯**」：
- **格式**：使用 Markdown 純文字的 ASCII 方框圖或箭頭流程圖。
- **核心要求**：關聯圖必須清楚呈現：
    - 技能的角色定位（服務對象是哪個 Project？）
    - 技能與技能之間的依賴或協作關係（例如 Router → Renderer）
    - 哪些技能有直接的 Project 對應，哪些是跨 Project 的通用工具。
- **禁止事項**：關聯圖中不得包含程式碼邏輯或函數實作細節。

---

## 🔑 核心概念（背景知識）

- **Load-on-Demand**：Agent 僅透過 `skills/README.md` 感知技能存在，只在明確觸發時才載入詳細的 `SKILL.md` 指令。
- **Context Flush**：任務結束後主動清理技能上下文，避免長期佔用 Token 影響思考純淨度。
- **Security Auditing**：外部引用技能在納入前必須通過 `skill_checkthreat` 靜態審計。
- **技能與 Project 的映射**：並非每個技能都對應一個 Project；部分技能是「跨 Project 的通用治理工具」（如 `skill_checkthreat`），部分是「特定 Project 的專屬賦能工具」（如 `skill_build_mcp_server`）。

---

## 📅 深度渲染頁面規劃 (共 8 頁)

### 🔄 Page 1: 技能生態治理與加載生命週期
- **介紹深度**：詳細描述。
- **內容焦點**：說明整個 Workspace 的技能庫並不是「啟動時全部載入」，而是採用精心設計的「沙盒生命週期」機制，實現 Token 效率最大化。
- **要求**：
    - 詳細闡述三階段完整生命週期：
        - **Discovery (靜態感知)**：Agent 只讀 `skills/README.md` 一份清單，不進入任何技能目錄。
        - **Load-on-Demand (按需載入)**：只在用戶觸發（`@[skill_name]`）或特許例外規則觸發時，才讀取對應 `SKILL.md`。
        - **Context Flush (執行後清除)**：任務完成後主動釋放技能佔用的 Context，維持思考空間純淨。
    - 說明此機制在高頻率長對話中對 Token 效率、幻覺防範與專注力維持的具體效益。
    - **必須繪製**：「技能沙盒生命週期閉環關聯圖」，展示技能從靜態存在到動態執行再到清除的完整迴圈。

### 🛡️ Page 2: 技能二元分流架構與安全審計機制
- **介紹深度**：詳細描述。
- **內容焦點**：介紹 Workspace 中的技能如何被系統性地分類為兩個分支，以及「安全看門狗」如何守護外部技能的引入安全。
- **要求**：
    - **Custom 原生專屬技能**：深度介紹此類技能的特徵 — 由內部自主研發、針對 Workspace 特定需求、具備高信任度與系統操作特權。代表性技能：`skill_build_mcp_server`、`skill_checkthreat`、`skill_open_calculator`、`skill_open_firefox`。
    - **Downloaded 社群生態技能**：深度介紹此類技能的特徵 — 引用自 GitHub 等開源社群、提供外部優秀設計與方法論、引入前必須審計。代表性技能：`Awesome-PPT-Design-Skills-main`（包含 6 種 PPT 風格子技能）。
    - 深入說明 `skill_checkthreat` 如何作為防火牆，對社群技能執行靜態威脅分析與安全分類。
    - **必須繪製**：「技能二元分流與安全審計關聯圖」，展示新技能進入 Workspace 的完整審查路徑（Custom 直通 / Downloaded 需經 `skill_checkthreat` 審計）。

### 📋 Page 3: 各技能角色定位與橫向對比
- **介紹深度**：詳細描述。
- **內容焦點**：對 Workspace 中所有技能進行系統性的角色定位說明，並以橫向對比的視角呈現各技能的職責邊界與差異。
- **要求**：
    - 按照技能的功能類別分組介紹：
        - **簡報製作類**：`skill_outline_ai_present_router`（規劃大腦）、`skill_html_ai_present_renderer`（視覺畫筆）
        - **系統工具類**：`skill_open_calculator`（計算機綁定）、`skill_open_firefox`（瀏覽器綁定）
        - **技術建設類**：`skill_build_mcp_server`（MCP 伺服器建置範本）
        - **安全治理類**：`skill_checkthreat`（技能庫威脅審計）
        - **社群設計類**：`Awesome-PPT-Design-Skills-main`（6 種 PPT 風格設計技能包）
    - 說明各技能的**服務對象**（特定 Project / 通用工具 / 跨技能協作）。
    - **必須繪製**：「技能角色地圖關聯圖」，以分組方式展示所有技能及其服務對象的橫向關係。

### 🗺️ Page 4: 專案資料夾與技能的精確映射關聯
- **介紹深度**：詳細描述。
- **內容焦點**：精確呈現 Workspace 中哪些 Project 資料夾與哪些技能有明確的對應使用關係，以及關聯的業務邏輯理由。
- **要求**：
    - **僅列出有確認對應關係的映射項目**（不臆測未確認的關係）：
        - 📁 `ppt_ai_present` ➔ 🛠️ `skill_outline_ai_present_router` (簡報大綱路由規劃) & `skill_html_ai_present_renderer` (簡報 HTML5 視覺渲染)
        - 📁 `skills/` (技能庫本身) ➔ 🛠️ `skill_checkthreat` (技能庫的安全審計守門員)
        - 📁 `PMS_AutoReport_teddy20260505` ➔ 🛠️ `skill_build_mcp_server` (MCP 伺服器建置最佳實踐範本)
    - 對每個映射關係說明「**為什麼是這個技能服務這個 Project？**」的業務邏輯理由。
    - **必須繪製**：「Project-to-Skill 精確映射關聯圖」，以箭頭方式清晰呈現三組映射關係及各自的服務語義。

### 🧩 Page 5: `skill_outline_ai_present_router` 的獨特模組化架構 [專頁]
- **介紹深度**：詳細描述。這是整個技能庫中**唯一具備子規格模組化結構**的技能，值得獨立一頁深度介紹。
- **內容焦點**：解析 `skill_outline_ai_present_router` 為何不同於其他所有技能 — 它不只是一個 `SKILL.md`，而是一套由「母規格 + 多個子模組規格」組成的**遞進式深度指令系統**。
- **要求**：
    - 說明其三層結構的設計邏輯：
        - **頂層 `SKILL.md`**：定義 Router 的核心行為、Topic 規劃與執行總原則。
        - **子模組一 `01_mcp_spec/mcp_rules.md`**：當執行 Topic 3（MCP Server 介紹）時，由頂層委派至此，提供 MCP 的深度渲染規範（5 頁細節）。
        - **子模組二 `02_skills_management/flow_rules.md`**：當執行 Topic 4（技能管理介紹）時，由頂層委派至此，提供技能的深度渲染規範（本文件，8 頁細節）。
    - 說明這種「**按需委派 (Delegated Loading)**」架構的優勢：頂層保持精簡，只在需要深度內容時才動態引用子模組，極大節省 AI 不必要的 Context 消耗。
    - **必須繪製**：`skill_outline_ai_present_router` 的**模組化委派架構關聯圖**，展示頂層 `SKILL.md` 如何在特定 Topic 時動態委派至各子模組規格：
        ```
        [ skill_outline_ai_present_router/SKILL.md ]
                      |
          +-----------+------------+
          | Topic 3 觸發           | Topic 4 觸發
          v                        v
        [ 01_mcp_spec/          [ 02_skills_management/
          mcp_rules.md ]          flow_rules.md ]
          (MCP 深度規範            (技能管理深度規範
           5 頁指令)                8 頁指令 ← 本文件)
        ```

### 🎨 Page 6: Router ↔ Renderer 協作關聯與職責分工
- **介紹深度**：詳細描述。
- **內容焦點**：深度剖析 `skill_outline_ai_present_router` 與 `skill_html_ai_present_renderer` 這對核心技能的協作模式，解釋「為什麼要拆成兩個技能，而不是合併成一個」的設計哲學。
- **要求**：
    - **Router 的職責邊界**：專注於架構分析與深度 Markdown 大綱產出。它只「思考與規劃」，不「繪圖與渲染」。
    - **Renderer 的職責邊界**：接收 Router 的大綱輸入，注入美學風格，渲染為互動式 HTML5 簡報。它只「執行與呈現」，不「分析與規劃」。
    - 說明兩者之間的**接口協定**：Router 輸出的 Markdown 大綱格式，如何作為 Renderer 的標準化輸入。
    - 說明此解耦設計帶來的三大優勢：1. 單一職責、2. 可獨立更換任一技能、3. Token 效率（規劃階段不消耗渲染的 Context）。
    - **必須繪製**：「Router ↔ Renderer 協作數據流關聯圖」，展示從 AI 分析 Workspace 到最終 HTML5 簡報落盤的完整協作流程：
        ```
        [ AI Agent ]
             | 呼叫
             v
        [ skill_outline_ai_present_router ]
             | 產出 Markdown 大綱
             v
        [ 深度大綱 .md 文件 ] ---> ppt_ai_present/
             | 授權後輸入
             v
        [ skill_html_ai_present_renderer ]
             | 渲染
             v
        [ HTML5 互動簡報 .html ] ---> ppt_ai_present/
        ```

### 🌐 Page 7: 跨技能協作全局關聯大圖 [獨佔整頁]
- **介紹深度**：詳細描述。這是整個技能模組中**最重要的一頁**，單獨佔據完整一頁以確保全局大圖有足夠的呈現空間。
- **內容焦點**：以一張全景大圖，完整呈現 Workspace 中所有技能的角色定位、相互之間的協作關係，以及與各 Project 資料夾的映射聯動，讓讀者一眼看懂整個技能生態系的神經網絡。
- **要求**：
    - 說明大圖的閱讀邏輯：從 Project 需求出發，找到對應技能；從技能關係出發，理解協作鏈路。
    - 說明圖中有哪些不同類型的連接關係（使用 / 委派 / 審計 / 協作）。
    - **必須繪製**：這是整份報告最重要的全景圖，必須完整呈現：
        - 所有 Project 資料夾（僅有映射關係的）與技能的連接
        - `skill_outline_ai_present_router` 的內部模組化結構（對外是一個技能，對內委派子模組）
        - Router → Renderer 的協作箭頭
        - `skill_checkthreat` 作為安全審計對 Downloaded 技能的守門關係
        - `Awesome-PPT-Design-Skills-main` 作為設計靈感源頭對 Renderer 的影響

### 📜 Page 8: 技能開發規範與生態擴充指南
- **介紹深度**：詳細描述。
- **內容焦點**：定義新技能加入 Workspace 的「黃金標準」流程，確保技能生態在持續擴充的過程中維持高度一致性、可讀性與安全性。
- **要求**：
    - **自描述規範 (`SKILL.md`)**：每個新技能目錄必須配備自描述的 `SKILL.md`，包含技能名稱、核心功能描述、適用的 Project 範圍、輸入/輸出協定說明。
    - **清單註冊 (`skills/README.md`)**：新技能必須在總清單中完成表格化登記，標明名稱、來源（內部/GitHub）、主要用途與當前審計狀態。
    - **安全審計發佈流程**：Custom 技能需自我安全審查；Downloaded 技能強制通過 `skill_checkthreat` 掃描，通過後方可正式納入按需載入沙盒。
    - **必須繪製**：「新技能發佈流程關聯圖」，展示從技能開發完成到正式進入 Workspace 生態的完整審查與發佈鏈路（Custom 路徑 / Downloaded 路徑的分叉與匯合）。
