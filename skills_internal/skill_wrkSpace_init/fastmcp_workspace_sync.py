# -*- coding: utf-8 -*-
import os
import sys
import io
import contextlib
from mcp.server.fastmcp import FastMCP

# 將當前路徑加入模組搜尋路徑以導入 workspace_sync
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from workspace_sync import perform_sync

# 初始化 FastMCP 伺服器
mcp = FastMCP("Workspace Sync")

@mcp.tool()
async def sync_workspace(action: str = "check", workspace: str = None) -> str:
    """
    Compare and sync the project list in the current active workspace.
    
    - action: 'check' (dry-run comparison) or 'sync' (automatic capitalization correction).
    - workspace: Optional. Specify a target .code-workspace file name (e.g. 'workspace_ai_antigravity.code-workspace').
    """
    apply_sync = (action.lower() == "sync")
    
    # 捕獲 perform_sync 的 stdout 輸出
    stdout_buffer = io.StringIO()
    with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stdout_buffer):
        try:
            perform_sync(apply_changes=apply_sync, target_workspace=workspace)
        except Exception as e:
            print(f"[錯誤] 執行同步時發生異常: {str(e)}")
            
    return stdout_buffer.getvalue()

if __name__ == "__main__":
    mcp.run()
