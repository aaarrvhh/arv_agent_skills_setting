# 🎨 Skill: HTML AI Present Renderer

此技能專注於「視覺呈現」，將結構化的大綱轉化為高品質的互動式簡報。

## 🎯 核心功能與要求
1. **HTML5 封裝**：產出具備翻頁功能的單一 HTML5 檔案。
2. **動態關聯圖渲染 (Mermaid.js)**：
   - 嚴禁在最終簡報中直接顯示生硬的 ASCII 純文字方框圖。
   - **必須引入 `Mermaid.js`**，將 Markdown 大綱中的架構圖、流程圖、數據流圖轉化為精美的 SVG 向量圖形。
   - **支援圖表**：Flowcharts, Sequence Diagrams, State Diagrams, Architecture Maps 等。
3. **視覺風格套用 (Awesome PPT Skills)**：
   - 渲染前，必須根據用戶需求或大綱氛圍，從 `Awesome-PPT-Design-Skills-main` 庫中選擇**一種**特定的風格子技能作為視覺基礎。
   - 必須主動讀取所選風格子目錄內的指南（例如 CSS 變數、字體建議、排版佈局），並將其應用於 HTML5 中。
   - **可用的 6 大風格庫清單**：
     - 🚀 `futuristic-tech-editorial-ppt-skill` (未來科技雜誌風)
     - ✍️ `japanese-hand-drawn-editorial-ppt-skill` (日系手繪排版風)
     - 🎌 `japanese-style-ppt-skill` (日式傳統/和風)
     - 💎 `minimalist-luxury-branding-ppt-skill` (極簡奢華品牌風)
     - 🎨 `modern-illustration-editorial-ppt-skill` (現代插畫排版風)
     - ☁️ `soft-3d-clay-ppt-skill` (柔和 3D 黏土風)
4. **分頁導覽系統**：自動生成可跳轉的數字選單、鍵盤控制或縮圖導航。
5. **跨平台兼容**：確保在主流瀏覽器中展現一致的動態效果與完美的圖表縮放。

## 📥 輸入規範
- 接收由 `skill_outline_ai_present_router` 產出的 Markdown 大綱（大綱內可能包含邏輯描述與 ASCII 草圖，需由本技能轉化為視覺圖形）。

## 🛠️ 使用規範
- **執行前置**：先確定要採用哪一個 Awesome-PPT 風格，讀取該風格的特定參數再行渲染。
- **產出物存放於**：`ppt_ai_present/`。
- **檔名格式**：`[Name]_YYYYMMDD_HHMM.html`。
