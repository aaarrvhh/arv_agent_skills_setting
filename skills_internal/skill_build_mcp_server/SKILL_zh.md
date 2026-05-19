---
name: build_mcp_server
description: 引導 AI Agent 建立 MCP (Model Context Protocol) Server 的技能方法。
---
# MCP Tool Build Specifications (MCP 工具建構規範)

## 技能描述
本技能定義了專案內自訂工具的兩種開發與建構模式。開發者與 Agent 必須依據工具的「通用性需求」與「模型規模（如大模型或 1B~2B 小模型）」，選擇適當的模式進行開發。

## 模式一：標準解耦模式 (Standard Decoupled Mode)
*適用場景：追求終極跨平台通用、需要對接小模型（如 Gemma 3:1b、Qwen 2.5:1.5b），或不希望工具與特定的 FastMCP 框架高階語法綁定時。*

### 檔案分工說明
1. **schema.json (規格定義書)**
   - 本工具的唯一規格標準，採用通用 JSON Schema 格式。
   - 內含工具名稱、功能描述、以及 Agent 呼叫時必須帶入的參數型態。
   - **禁止**在此檔案中寫入任何與 MCP 協定綁定的特定語法，確保此規格書可以被任意其他 AI 平台（如純 OpenAI/Gemini API、LangChain、CrewAI）直接複用。
2. **mcp_server.py (邏輯實作與 MCP 封裝)**
   - 本工具的程式碼本體，使用 `mcp.server` 的基礎低階庫。
   - 運作時，它會動態讀取同目錄下的 `schema.json` 作為對外宣告的規格並向 IDE 註冊。
   - 內部直接包含本工具的核心執行邏輯（不另設 main.py），負責接收 AI 參數並執行。

## 模式二：FastMCP 整合模式 (FastMCP Integrated Mode)
*適用場景：僅在本地端支援 MCP 的 IDE 環境（如 Antigravity, Cursor）中使用、對接推理能力強的大模型，追求極速開發與「程式碼即規格（Code-as-Schema）」時。*

### 檔案分工說明
1. **fastmcp_server.py (單一整合檔)**
   - 本模式**不需要**獨立的 `schema.json`。
   - 使用 Anthropic 官方的 `mcp.server.fastmcp` 高階庫。
   - 工具的名稱、描述與參數型態，直接透過 Python 的型態提示（Type Hints）與 Docstring 寫在同一個檔案中。
   - 框架在啟動時，會自動內省（Introspect）此檔案並動態將規格發布給 IDE。

## 檔案命名與分工規範

### 【選擇 A：標準解耦模式】— 適用於小模型/跨平台
- 規格書命名：必須為 `schema.json`
- 伺服器命名：必須為 `mcp_server_[工具名稱].py` (例如：`mcp_server_bootloader.py`)
- 註記：此 Python 檔使用 low-level SDK，啟動時會主動讀取同目錄下的 `schema.json`。

### 【選擇 B：FastMCP 整合模式】— 適用於大模型/極速開發
- 檔案命名：必須為 `fastmcp_[工具名稱].py` (例如：`fastmcp_bootloader.py`)
- 註記：此模式不允許存在 `schema.json`，規格直接內嵌於 Python 的 Type Hints 與 Docstring 中。
