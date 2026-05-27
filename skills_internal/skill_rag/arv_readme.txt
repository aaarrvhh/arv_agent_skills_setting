# For User only,  AI Agent do not read this file.

├── rag_skill/
│   └── project_rag_manager.py     <-- 您的 Python Main Skill (共用)
│
├── project_vault/                 <-- 自動生成的隔離向量資料庫 (共用產出區)
│   ├── db_PROJECT_A/
│   └── db_PROJECT_B/
│
└── projects/                      <-- 專案資料夾
    ├── PROJECT_A/
    │   ├── config_projectA.json   <-- 專案 A 的專案設定檔
    │   └── specs/                 <-- 專案 A 的多份規格書
    │       ├── chip_datasheet.pdf
    │       └── protocol_spec.docx
    │
    └── PROJECT_B/
        ├── config_projectB.json   <-- 專案 B 的專案設定檔
        └── specs/
            └── main_spec.pdf
