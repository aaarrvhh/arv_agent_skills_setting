---
name: build_mcp_server
description: Instructions on how to build an MCP (Model Context Protocol) Server with low-level and FastMCP methods.
---
# MCP Tool Build Specifications

## Skill Description
This skill defines the two development and construction modes for custom tools within the project. Developers and Agents must choose the appropriate mode based on the "generality requirement" of the tool and the "model scale (e.g., large models vs. 1B~2B small models)".

## Mode 1: Standard Decoupled Mode
*Use Case: For ultimate cross-platform generality, integration with small models (e.g., Gemma 3:1b, Qwen 2.5:1.5b), or when you do not want the tool to be tied to the high-level syntax of the FastMCP framework.*

### File Responsibilities
1. **schema.json (Specification Document)**
   - The sole specification standard of the tool, using the general JSON Schema format.
   - Contains the tool name, functional description, and parameter types required when called by the Agent.
   - **PROHIBITED** from writing any specific syntax bound to the MCP protocol in this file, ensuring this specification can be directly reused by any other AI platform (such as pure OpenAI/Gemini API, LangChain, CrewAI).
2. **mcp_server.py (Logic Implementation & MCP Encapsulation)**
   - The codebase of the tool, utilizing the low-level `mcp.server` library.
   - During runtime, it dynamically reads `schema.json` in the same directory as the specification for external declaration and registration to the IDE.
   - Contains the core execution logic of the tool directly (without a separate main.py), receiving AI parameters and executing them.

## Mode 2: FastMCP Integrated Mode
*Use Case: Only used in local IDE environments supporting MCP (e.g., Antigravity, Cursor), interfacing with powerful large models, and aiming for rapid development and "Code-as-Schema".*

### File Responsibilities
1. **fastmcp_server.py (Single Integrated File)**
   - This mode **does not** require an independent `schema.json`.
   - Uses Anthropic's official high-level library `mcp.server.fastmcp`.
   - The name, description, and parameter types of the tool are directly written in the same file using Python's Type Hints and Docstrings.
   - The framework automatically introspects this file at startup and dynamically publishes the specifications to the IDE.

## File Naming and Responsibility Specifications

### 【Option A: Standard Decoupled Mode】— For Small Models / Cross-Platform
- Specification File Name: Must be `schema.json`
- Server File Name: Must be `mcp_server_[tool_name].py` (e.g., `mcp_server_bootloader.py`)
- Note: This Python file uses the low-level SDK and will actively read `schema.json` in the same directory upon startup.

### 【Option B: FastMCP Integrated Mode】— For Large Models / Rapid Development
- File Naming: Must be `fastmcp_[tool_name].py` (e.g., `fastmcp_bootloader.py`)
- Note: This mode does not allow `schema.json` to exist. Specifications are embedded directly within Python's Type Hints and Docstrings.
