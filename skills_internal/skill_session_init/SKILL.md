---
name: skill_session_init
description: 負責管理 Agent 啟動時的 Session 初始化程序，包含動態列出工作空間中所有可用技能的工具。
---

# 技能：Session Initialization & Skill Discovery

此技能用於管理 Agent 啟動時載入的預設技能與動態探勘工作空間內的技能列表。

## 🎯 核心功能

1. **動態列出可用技能 (Dynamic Skill Listing)**
   - 使用 `list_skills.py` 腳本動態掃描並列出所有支援的技能，避免 Agent 自行走訪資料夾或將過多無用資訊存入 Context。
   - **執行指令** (於工作空間根目錄下執行): 
     `python .agent/skills_internal/skill_session_init/list_skills.py`
     或加上 `--json` 取得 JSON 格式輸出。

2. **Session 預設載入清單 (Session Default Loading)**
   - 記錄在 `session_skills.json` 中的技能陣列。
   - 啟動時，若有需預先載入的技能，將會在此清單中定義。
   - 目前的預設載入清單為：`["skill_path_policy", "skill_github"]`。

3. **載入狀態確認 (Load Status Confirmation)**
   - 在完成 Session Initialization（讀取本技能及預設載入清單）之後，Agent **必須主動**向用戶列出目前在自己 Context 記憶中實際「已載入」的技能清單。
   - 目的：讓用戶能隨時確認並驗證 Agent 的實際載入狀態，確保沒有冗餘的技能佔用 Context 空間，並嚴格落實按需加載（Load-on-Demand）。
