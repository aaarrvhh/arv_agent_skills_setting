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
dudu_byby = __import__(path_policy.CREDENTIAL_RESOLVER_TOOL)

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
    # Mask any potential authorization headers in logs
    printed_args = []
    for arg in args:
        if "http.extraheader=Authorization: Basic" in arg:
            printed_args.append("http.extraheader=Authorization: Basic <TOKEN_MASKED>")
        else:
            printed_args.append(arg)
    print(f"Running: git {' '.join(printed_args)}")
    res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error executing git command: {res.stderr.strip()}")
        return False, res.stdout, res.stderr
    return True, res.stdout, res.stderr

import argparse

def main():
    parser = argparse.ArgumentParser(description="Git Push Helper with Dynamic Agent Signature")
    parser.add_argument("-m", "--message", type=str, default="Upload .agent changes", help="Commit message")
    parser.add_argument("--agent", type=str, default=None, help="Agent signature, e.g., 'Antigravity Agent in VS Code'")
    args_cli = parser.parse_args()

    repo_url, token = read_config()
    
    if args_cli.agent:
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
        commit_msg = args_cli.message
        signature = f" (committed by {args_cli.agent})"
        if signature not in commit_msg:
            commit_msg += signature

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
    else:
        print("User manual execution detected. Skipping git add and commit. Proceeding directly to push.")
        
    # Get current branch
    success, stdout, _ = run_git_cmd(["rev-parse", "--abbrev-ref", "HEAD"], AGENT_DIR)
    branch = stdout.strip() if success else "main"
    
    # 4. Push using http.extraheader
    import base64
    auth_string = f"git:{token}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()
    
    print(f"Pushing changes to origin {branch} with temporary in-memory authentication...")
    success, stdout, stderr = run_git_cmd([
        "-c", f"http.extraheader=Authorization: Basic {b64_auth}",
        "push", "origin", branch
    ], AGENT_DIR)
    
    if success:
        print("Push succeeded!")
        print(stdout)
    else:
        print("Push failed.")
        print(stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
