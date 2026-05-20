# Workspace Onboarding Guidelines (WORKSPACE_GUIDE_en.md)

This document defines the Agent's behavior, directory priority, and safety protocols within this multi-project workspace.

---

## 1. Directory Focus Priority (Initialization & First Open)

When this workspace is first opened, the Agent MUST **strictly focus and align with the following priority hierarchy** rather than traversing the workspace blindly:

### Priority 1 (Core Guidelines & Active Task)
1. **`.agent`**: Core instructions (`.init_agent.md`), user profile (`USER.md`), and soul rules (`SOUL.md`).
2. **`ppt_ai_present`**: The primary project directory currently in progress or set for execution.

### Priority 2 (Workspace Core & Side Projects)
3. **`wrkSpace_ai`**: High-level structure definitions of the workspace.
4. **Other Project Directories**:
   - `PMS_AutoReport_teddy20260505` (Automated Daily Reporting system)
   - `discord_connection` (Discord Bot Integration workspace)
   - `NPCM845D_DTS` (Hardware Device Trees & DTS files)
   - `private_security` (Safety & privacy-wipe automation)
   - `merge_uboot_` (Bootloader & U-Boot firmware merging utility)
   - `dump_info` (System log and info dump)

---

## 2. MCP Server Configuration List

Model Context Protocol (MCP) servers configured and operational in this environment:

- **PMS AutoReport**: `PMS_AutoReport_teddy20260505/src/mcp_server.py`
- **Discord Connection**: `discord_connection/src/mcp_server.py`
- **Github Connection**: `.agent/skills_internal/skill_github/fastmcp_github.py`

---

## 3. Skill Loading & Execution Protocols

> [!CAUTION]
> **Strict Security Boundaries (Safety Policy)**
> - **Path**: `skills/` (located at workspace root)
> - **Default Restriction**: The Agent **MUST NOT** proactively load, read, or traverse the contents of the `skills/` directory during initialization or without authorization.

### Activation Rules:
1. **Load-on-Demand**: The `skills/` contents are strictly loaded on-demand. Only read specific skill folders if explicitly instructed by the user (e.g., *"Read the build_mcp_server skill"*).
2. **Active Project Exception**: 
   - When the Agent is working inside the **`ppt_ai_present`** project, the Agent **is permitted and expected to proactively load and follow** the instructions in `skills/skill_outline_ai_present_router` and `skills/skill_html_ai_present_renderer` without waiting for manual prompts.

---
*Last Updated: 2026-05-19*


