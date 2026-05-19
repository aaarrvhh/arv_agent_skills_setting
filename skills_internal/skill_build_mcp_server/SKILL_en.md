---
name: build_mcp_server
description: Guidelines for building an MCP (Model Context Protocol) Server for AI agents.
---
# Build MCP Server

This skill provides instructions on how to design and build an MCP Server to expose local application capabilities to AI agents (like Claude or Antigravity).

## Architecture & Workflow

Based on the PMS AutoReport architecture, an effective MCP integration should follow a layered approach:

### 1. Extract Core Logic (The Client Layer)
Do not mix AI tool definitions directly with complex logic.
- Extract all core operations (e.g., HTTP requests, scraping, database queries) into a clean, standalone Python class (e.g., `PMSClient`).
- Ensure this layer is independent of any GUI or CLI logic.

### 2. Setup the MCP Server (The Tool Layer)
Create a dedicated entry point (e.g., `src/mcp_server.py`) using a library like `FastMCP`.
- Use the `@mcp.tool()` decorator to expose specific methods.
- **CRITICAL**: Write clear `docstrings` and `type hints` for each tool. The AI uses these as the "instruction manual" to understand how and when to use the tool.

### 3. Handle Credentials & Privacy Securely
Do not force the user to type passwords directly into the AI chat interface (this consumes tokens and risks privacy).
- **Local Storage**: Read credentials from a local file (e.g., `private_info.json`).
- **Trigger Local UI**: Provide a tool (e.g., `trigger_auth_gui`) that the AI can call when credentials are missing. This tool should pop up a local GUI dialog (like Tkinter) for the user to enter their password securely.
- **Wipe Utility**: Consider adding a `wipe_sensitive_data` tool to help users clean up their credentials before sharing the project.

### 4. Provide Diagnostic Tools
Include tools that help the AI understand its own readiness.
- Example: `get_auth_status` allows the AI to proactively check if it has the necessary credentials before attempting complex tasks, preventing mid-execution failures.

## Example Reference
For a complete, working example of this pattern, refer to the `PMS_AutoReport_teddy` project. It demonstrates how to transition a legacy script into a robust MCP Server while maintaining backwards compatibility with traditional CLI/GUI execution.
