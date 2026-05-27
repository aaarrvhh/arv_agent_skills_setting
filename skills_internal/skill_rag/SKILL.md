---
name: skill_rag
description: RAG 規格書檢索與資料庫建置技能
---

# 技能：RAG 規格書檢索與資料庫建置 (RAG Spec Retrieval & DB Builder)

此技能提供跨專案的規格書（docx 格式）解析、區塊化（chunking），並將其建置為向量資料庫（ChromaDB）與關聯式資料庫（SQLite）之功能。

## 🎯 核心原則

1. **模組化雙引擎**：
   - 支援 ChromaDB（Dense Vector Embedding 語意相似度檢索）。
   - 支援 SQLite（輕量關鍵字比對）。
   - 建置 ChromaDB 時，系統會**自動同時建置並輸出 SQLite 資料庫**，確保兩種引擎資料同步。

2. **保留標題階層**：
   - 解析 docx 時，會保留段落所屬的標題路徑（例如：`Chapter 1 > Section 2`），以便在檢索時提供更佳的上下文資訊。

3. **保留表格結構**：
   - 自動將 Word 規格書中的表格提取並轉換成標準 Markdown 表格結構儲存。

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
