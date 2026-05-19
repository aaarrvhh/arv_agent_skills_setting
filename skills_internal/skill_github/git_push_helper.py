import os
import sys
import subprocess

# Paths
WORKSPACE_ROOT = r"d:\fxn_arvin\antigravity_ai_"
AGENT_DIR = os.path.join(WORKSPACE_ROOT, ".agent")

def get_github_txt_path():
    index_paths = [
        os.path.join(WORKSPACE_ROOT, "private_security", "arv_ps_index.txt"),
        r"d:\fxn_arvin\antigravity_ai_\private_security\arv_ps_index.txt",
        r"f:\arv_google_antigravity\private_security\arv_ps_index.txt"
    ]
    fallback = os.path.join(WORKSPACE_ROOT, "private_security", "arv_github.txt")
    for ip in index_paths:
        if os.path.exists(ip):
            try:
                with open(ip, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            key, value = line.split("=", 1)
                            if key.strip() == "SYS_NODE_93":
                                return os.path.join(os.path.dirname(ip), value.strip())
            except Exception as e:
                print(f"Error reading index file {ip}: {e}")
    return fallback

GITHUB_TXT_PATH = get_github_txt_path()

def read_config():
    if not os.path.exists(GITHUB_TXT_PATH):
        print(f"Error: Config file not found at {GITHUB_TXT_PATH}")
        sys.exit(1)
        
    repo_url = ""
    token = ""
    with open(GITHUB_TXT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("GITHUB_REPO_URL="):
                repo_url = line.split("=", 1)[1].strip()
            elif line.startswith("GITHUB_TOKEN="):
                token = line.split("=", 1)[1].strip()
                
    if not repo_url or not token:
        print("Error: GITHUB_REPO_URL or GITHUB_TOKEN not found in config file.")
        sys.exit(1)
        
    return repo_url, token

def run_git_cmd(args, cwd):
    print(f"Running: git {' '.join(args)}")
    res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error executing git command: {res.stderr.strip()}")
        return False, res.stdout, res.stderr
    return True, res.stdout, res.stderr

def main():
    repo_url, token = read_config()
    
    # 1. Get current status
    success, stdout, _ = run_git_cmd(["status"], AGENT_DIR)
    if not success:
        sys.exit(1)
    print("\nGit Status Output:")
    print(stdout)
    
    # 2. Add files
    success, _, _ = run_git_cmd(["add", "."], AGENT_DIR)
    if not success:
        sys.exit(1)
        
    # 3. Commit changes
    commit_msg = "Upload .agent changes (committed by Antigravity Agent in VS Code)"
    print(f"Committing changes with message: '{commit_msg}'")
    res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=AGENT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        if "nothing to commit" in res.stdout or "nothing to commit" in res.stderr:
            print("Nothing to commit, repository is clean.")
        else:
            print(f"Error committing: {res.stderr.strip()}")
            sys.exit(1)
    else:
        print(res.stdout.strip())
        
    # 4. Construct authenticated URL
    auth_url = repo_url
    if repo_url.startswith("https://"):
        auth_url = repo_url.replace("https://", f"https://{token}@")
    else:
        print("Error: GITHUB_REPO_URL must start with https://")
        sys.exit(1)
        
    # Get current branch
    success, stdout, _ = run_git_cmd(["rev-parse", "--abbrev-ref", "HEAD"], AGENT_DIR)
    branch = stdout.strip() if success else "main"
    
    # 5. Push using the authenticated URL
    try:
        print("Temporarily setting remote origin URL for push...")
        run_git_cmd(["remote", "set-url", "origin", auth_url], AGENT_DIR)
        
        print(f"Pushing changes to origin {branch}...")
        success, stdout, stderr = run_git_cmd(["push", "origin", branch], AGENT_DIR)
        if success:
            print("Push succeeded!")
            print(stdout)
        else:
            print("Push failed.")
            print(stderr)
            sys.exit(1)
    finally:
        print("Reverting remote origin URL back to original non-token URL...")
        run_git_cmd(["remote", "set-url", "origin", repo_url], AGENT_DIR)

if __name__ == "__main__":
    main()
