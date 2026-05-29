---
name: skill_rag
description: RAG 規格書檢索與資料庫建置技能
---

# 技能：RAG 規格書檢索與資料庫建置 (RAG Spec Retrieval & DB Builder)

此技能提供跨專案的規格書（docx 與 xlsx 格式）解析、區塊化（chunking），並將其建置為向量資料庫（ChromaDB）與關聯式資料庫（SQLite）之功能。

## 🎯 核心原則

1. **模組化雙引擎**：
   - 支援 ChromaDB（Dense Vector Embedding 語意相似度檢索）。
   - 支援 SQLite（輕量關鍵字比對）。
   - 建置 ChromaDB 時，系統會**自動同時建置並輸出 SQLite 資料庫**，確保兩種引擎資料同步。

2. **保留標題階層與表格結構**：
   - 解析 docx 時，會保留段落所屬的標題路徑（例如：`Chapter 1 > Section 2`）及標準 Markdown 表格結構。
   - 解析 xlsx 時，會將工作表 rows 轉換為結構化的 key-value 欄位記錄。

3. **建置前確認資料筆數**：
   - 在執行資料庫寫入（Build DB）前，系統必須**先計算並輸出解析出的區塊總筆數（Chunk Count）**。若總筆數超過 ChromaDB 的單次寫入上限（例如 5461 筆），必須以小於或等於 2000 筆為一批次進行分批（batching）寫入，以確保資料庫安全匯入。

## 🛠️ 使用規範

### 依賴套件
- `python-docx`
- `chromadb`
- `sentence-transformers`

### 常用命令

#### 1. 建置資料庫 (Build Database)
使用 `chroma` 引擎（此操作會自動同時建立 SQLite 資料庫）：
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --build --db-type chroma
```

僅建置 `sqlite` 資料庫：
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --build --db-type sqlite
```

#### 2. 檢索資料 (Query Database)
使用 `chroma` 語意搜尋檢索：
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --query "查詢問題" --db-type chroma
```

使用 `sqlite` 關鍵字檢索：
```powershell
python ./.agent/skills_internal/skill_rag/skill_rag.py --config ./rag_doc_gg/rag_project_gg.json --query "查詢問題" --db-type sqlite
```
