import os
import sys
import subprocess

# Dynamically resolve .agent path and import path_policy
current_dir = os.path.dirname(os.path.abspath(__file__))
agent_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if agent_dir not in sys.path:
    sys.path.append(agent_dir)
import path_policy

if path_policy.DUMP_INFO_PATH not in sys.path:
    sys.path.append(path_policy.DUMP_INFO_PATH)
import dudu_byby

# Paths
WORKSPACE_ROOT = path_policy.WORKSPACE_ROOT
AGENT_DIR = os.path.join(WORKSPACE_ROOT, ".agent")

def read_config():
    try:
        repo_url = dudu_byby.get_credential('github', 'GITHUB_REPO_URL')
        token = dudu_byby.get_credential('github', 'GITHUB_TOKEN')
        if not repo_url or not token:
            print("Error: GITHUB_REPO_URL or GITHUB_TOKEN not found in config.")
            sys.exit(1)
        return repo_url, token
    except Exception as e:
        print(f"Error reading config: {e}")
        sys.exit(1)


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
