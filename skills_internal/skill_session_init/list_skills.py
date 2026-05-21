import os
import sys
import json
import re
from pathlib import Path

# Ensure stdout uses UTF-8 encoding for Windows compatibility
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def parse_skill_md(file_path):
    """Parse the YAML frontmatter from a SKILL.md file."""
    skill_info = {"name": "Unknown", "description": "No description available", "path": str(file_path)}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Simple regex to extract frontmatter
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if match:
                frontmatter = match.group(1)
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key == 'name':
                            skill_info['name'] = value
                        elif key == 'description':
                            skill_info['description'] = value
    except Exception as e:
        skill_info['description'] = f"Error reading skill metadata: {e}"
        
    return skill_info

def list_skills(workspace_root):
    """Scan predefined directories and list all available skills."""
    skill_dirs = [
        Path(workspace_root) / "skills",
        Path(workspace_root) / ".agent" / "skills_internal",
        Path(workspace_root) / ".agent" / "skills_external"
    ]
    
    skills = []
    
    for base_dir in skill_dirs:
        if not base_dir.exists() or not base_dir.is_dir():
            continue
            
        for skill_md_path in base_dir.rglob("SKILL.md"):
            # Compute relative path from workspace root for cleaner output
            rel_path = skill_md_path.parent.relative_to(Path(workspace_root))
            info = parse_skill_md(skill_md_path)
            info['path'] = str(rel_path).replace('\\', '/')
            skills.append(info)
                    
    return skills

if __name__ == "__main__":
    # 動態尋找 .agent 目錄並匯入 path_policy (嚴禁寫死絕對路徑)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    agent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    if agent_dir not in sys.path:
        sys.path.append(agent_dir)
    import path_policy

    workspace_root = path_policy.WORKSPACE_ROOT
    
    all_skills = list_skills(workspace_root)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(all_skills, indent=2, ensure_ascii=False))
    else:
        print("Available Skills:\n")
        for skill in all_skills:
            print(f"- {skill['name']} ({skill['path']})")
            print(f"  Description: {skill['description']}\n")
