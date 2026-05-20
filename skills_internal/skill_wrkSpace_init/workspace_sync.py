# -*- coding: utf-8 -*-
import os
import sys
import re
import json
import argparse

# 確保控制台輸出使用 UTF-8 編碼以防止亂碼
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 定義檔案與目錄路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.dirname(os.path.dirname(current_dir))
parent_dir = os.path.dirname(agent_dir)

target_files = {
    "USER.md": os.path.join(agent_dir, "USER.md"),
    "WORKSPACE_GUIDE_zh.md": os.path.join(agent_dir, "WORKSPACE_GUIDE_zh.md"),
    "WORKSPACE_GUIDE_en.md": os.path.join(agent_dir, "WORKSPACE_GUIDE_en.md")
}

# 忽略的非專案關鍵字列表
ignored_keywords = {
    "USER.md", "SOUL.md", "WORKSPACE_GUIDE_zh.md", "WORKSPACE_GUIDE_en.md",
    ".agent", "skills", "skills_internal", "skills_external", "FastMCP",
    "docstrings", "type hints", "private_info.json", "trigger_auth_gui",
    "wipe_sensitive_data", "get_auth_status", "mcp_server.py", "fastmcp_workspace_sync.py", "skills/",
    "calc", "workspace_sync.py", "mcp_config.json", "wrkSpace_ai", "arv"
}

def get_actual_projects(target_workspace=None):
    """獲取實際存在的專案列表，優先從指定或自動偵測的 .code-workspace 檔案讀取，並以實體目錄為備援。"""
    projects = {}
    found_workspace = False
    
    wrkspace_folder_name = "wrkSpace_ai"
    wrkspace_path = os.path.join(parent_dir, wrkspace_folder_name)
    
    # 1. 蒐集所有可能的 .code-workspace 檔案
    workspace_files = []
    if os.path.exists(wrkspace_path):
        for f in os.listdir(wrkspace_path):
            if f.endswith(".code-workspace"):
                workspace_files.append(os.path.join(wrkspace_path, f))
                
    for f in os.listdir(parent_dir):
        if f.endswith(".code-workspace"):
            workspace_files.append(os.path.join(parent_dir, f))
            
    # 2. 確定要使用哪一個 workspace 檔案
    selected_workspace = None
    
    # A. 優先使用命令列指定的檔案
    if target_workspace:
        for wf in workspace_files:
            if os.path.basename(wf) == target_workspace or wf == target_workspace:
                selected_workspace = wf
                break
                
    # B. 其次使用 VS Code 環境變數
    if not selected_workspace:
        vscode_env = os.environ.get('VSCODE_WORKSPACE_FILE')
        if vscode_env and os.path.exists(vscode_env):
            selected_workspace = vscode_env
            
    # C. 自動偵測：若有多個，比對 USER.md 的當前主要專案來決定
    if not selected_workspace and len(workspace_files) > 1:
        active_project = None
        user_md_path = os.path.join(agent_dir, "USER.md")
        if os.path.exists(user_md_path):
            try:
                with open(user_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                m = re.search(r'\|\s*\*\*當前主要專案\*\*\s*\|\s*`([^`]+)`', content)
                if m:
                    active_project = m.group(1).lower()
            except Exception:
                pass
                
        if active_project:
            for wf in workspace_files:
                try:
                    with open(wf, 'r', encoding='utf-8') as file:
                        data = json.load(file)
                        folders = data.get("folders", [])
                        for folder in folders:
                            path = folder.get("path")
                            if path and active_project in path.lower():
                                selected_workspace = wf
                                break
                except Exception:
                    pass
                if selected_workspace:
                    break
                    
    # D. 若仍未選定，且有 workspace 檔案，預設使用第一個
    if not selected_workspace and workspace_files:
        selected_workspace = workspace_files[0]
        
    # 3. 解析選定的 workspace 檔案
    if selected_workspace:
        try:
            print(f"[環境探索] 使用之工作空間設定檔: {os.path.basename(selected_workspace)}")
            with open(selected_workspace, 'r', encoding='utf-8') as file:
                data = json.load(file)
                folders = data.get("folders", [])
                wf_dir = os.path.dirname(selected_workspace)
                for folder in folders:
                    path = folder.get("path")
                    if path:
                        abs_path = os.path.abspath(os.path.join(wf_dir, path))
                        if os.path.exists(abs_path) and os.path.isdir(abs_path):
                            basename = os.path.basename(abs_path)
                            if not basename:
                                basename = abs_path
                            # 過濾掉 .agent 與當前目錄
                            if basename not in {".agent", wrkspace_folder_name, "skills"}:
                                projects[basename.lower()] = {
                                    "name": basename,
                                    "path": abs_path
                                }
                                found_workspace = True
        except Exception:
            pass
            
    # 若無 workspace 配置，直接遍歷 parent_dir 實體目錄
    if not found_workspace:
        print("[環境探索] 未使用工作空間設定檔，改為直接掃描實體目錄")
        for f in os.listdir(parent_dir):
            full_path = os.path.join(parent_dir, f)
            if os.path.isdir(full_path) and not f.startswith('.'):
                if f not in {wrkspace_folder_name, "skills"}:
                    projects[f.lower()] = {
                        "name": f,
                        "path": full_path
                    }
                    
    return projects, selected_workspace

def perform_sync(apply_changes=False, target_workspace=None):
    """執行比對，並選擇性套用自動同步修正。"""
    actual_projects, selected_workspace = get_actual_projects(target_workspace)
    
    # Generate path_policy.py dynamically
    path_policy_path = os.path.join(agent_dir, "path_policy.py")
    try:
        with open(path_policy_path, "w", encoding="utf-8") as f:
            f.write(f'# 自動產生的路徑設定檔 (Auto-generated Path Policy)\n')
            f.write(f'WORKSPACE_ROOT = r"{parent_dir}"\n')
            f.write(f'DUMP_INFO_PATH = r"{os.path.join(parent_dir, "dump_info")}"\n')
        print(f"[系統] 已自動產生 {path_policy_path}")
    except Exception as e:
        print(f"[錯誤] 無法產生 path_policy.py: {str(e)}")

    print("=" * 60)
    print(" 工作空間專案清單比對工具 (Workspace Project Sync Tool)")
    print("=" * 60)
    print(f"實際偵測到之專案項目數: {len(actual_projects)}")
    for key, info in sorted(actual_projects.items()):
        print(f" - {info['name']} ({info['path']})")
    print("-" * 60)

    differences_found = False
    all_updates = {} # 記錄每個檔案的變更細節

    for filename, filepath in target_files.items():
        if not os.path.exists(filepath):
            print(f"[警告] 找不到目標文件: {filename}")
            continue

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.splitlines()
        modified = False
        file_updates = []

        # 1. 大小寫拼寫比對與更正
        # 尋找所有 markdown 反引號內的單字
        for i, line in enumerate(lines):
            # 匹配例如 `wrkspace_ai`
            matches = re.findall(r'`([^`]+)`', line)
            for match in matches:
                # 排除忽略的關鍵字或路徑
                parts = re.split(r'[/\\]', match)
                if not parts:
                    continue
                match_clean = parts[0]
                match_lower = match_clean.lower()
                
                correct_first = None
                # 另外特別處理 wrkSpace_ai，因為它有時被忽略
                if match_lower == "wrkspace_ai":
                    correct_first = "wrkSpace_ai"
                elif match_lower in actual_projects:
                    correct_first = actual_projects[match_lower]["name"]
                
                if correct_first and match_clean != correct_first:
                    correct_name = correct_first + match[len(match_clean):]
                    if match != correct_name:
                        # 進行替換
                        new_line = line.replace(f"`{match}`", f"`{correct_name}`")
                        if new_line != line:
                            lines[i] = new_line
                            line = new_line
                            modified = True
                            differences_found = True
                            file_updates.append(f"行 {i+1}: 大小寫修正 `{match}` -> `{correct_name}`")

        # 2. 僅針對導引指南 (WORKSPACE_GUIDE) 進行完整專案清單完整性檢查
        if "WORKSPACE_GUIDE" in filename:
            documented_projects = set()
            for line in lines:
                matches = re.findall(r'`([^`]+)`', line)
                for match in matches:
                    parts = re.split(r'[/\\]', match)
                    if not parts:
                        continue
                    match_clean = parts[0]
                    if match_clean not in ignored_keywords and not match_clean.endswith(('.md', '.py', '.json')):
                        if match_clean.lower() not in actual_projects and match_clean != "wrkSpace_ai":
                            # 檢查是否為專案名稱特徵（無特殊符號、字母底線組成）
                            if re.match(r'^[a-zA-Z0-9_\-]+$', match_clean):
                                documented_projects.add(match_clean)

            for dp in documented_projects:
                file_updates.append(f"警告: 文件記載但實際不存在的專案 `{dp}`")
                differences_found = True

            # 3. 檢查是否有實際存在但文件完全未提及的專案 (新專案)
            content_lower = content.lower()
            for key, info in actual_projects.items():
                if info["name"].lower() not in content_lower:
                    file_updates.append(f"缺失: 實際存在但文件未提及的專案 `{info['name']}`")
                    differences_found = True

        # 4. 針對 USER.md 特別更新「工作空間結構」中的設定檔名稱
        if filename == "USER.md" and selected_workspace:
            ws_basename = os.path.basename(selected_workspace)
            for idx, l in enumerate(lines):
                if "| **工作空間結構** |" in l:
                    expected_content = f"wrkSpace_ai/{ws_basename}"
                    m = re.search(r'`([^`]+)`', l)
                    if m and m.group(1) != expected_content:
                        new_line = l.replace(f"`{m.group(1)}`", f"`{expected_content}`")
                        if new_line != l:
                            lines[idx] = new_line
                            modified = True
                            differences_found = True
                            file_updates.append(f"行 {idx+1}: 更新工作空間設定檔為 `{expected_content}`")
                            break

        if file_updates:
            all_updates[filename] = {
                "updates": file_updates,
                "lines": lines,
                "filepath": filepath,
                "modified": modified
            }

    # 輸出比對結果
    if not differences_found:
        print("[資訊] 比對完成：所有設定檔與實際專案清單 100% 一致，無須更新。")
        return 0

    print("[發現差異] 以下為各設定檔的比對結果：")
    for filename, data in all_updates.items():
        print(f"\n* 檔案: {filename}")
        for update in data["updates"]:
            print(f"  - {update}")

    # 套用變更
    if apply_changes:
        print("\n" + "=" * 60)
        print(" 開始套用自動同步修正...")
        print("=" * 60)
        
        for filename, data in all_updates.items():
            if data["modified"]:
                try:
                    new_content = "\n".join(data["lines"]) + "\n"
                    with open(data["filepath"], 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"[成功] 已自動更新並儲存: {filename}")
                except Exception as e:
                    print(f"[錯誤] 無法寫入檔案 {filename}: {str(e)}")
            else:
                print(f"[跳過] 檔案 {filename} 無須進行大小寫實體更正 (僅含結構性警告)")
        print("\n[同步完成] 設定檔大小寫已對齊完畢。")
    else:
        print("\n[提示] 當前為唯讀比對模式。若要自動修正大小寫差異，請加上 `--sync` 參數執行。")

    return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Workspace project synchronization and comparison utility.")
    parser.add_argument("--check", action="store_true", help="Perform read-only project check (default).")
    parser.add_argument("--sync", action="store_true", help="Automatically sync project names and capitalization.")
    parser.add_argument("--workspace", type=str, default=None, help="Specify target .code-workspace file name (e.g. workspace_ai_antigravity.code-workspace).")
    
    args = parser.parse_args()
    
    # 預設為 check 模式
    apply_sync = False
    if args.sync:
        apply_sync = True
        
    sys.exit(perform_sync(apply_changes=apply_sync, target_workspace=args.workspace))
