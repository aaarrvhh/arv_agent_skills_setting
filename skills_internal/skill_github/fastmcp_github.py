import os
import subprocess
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("GithubConnectionServer")

def run_cmd(cmd_list, cwd):
    try:
        res = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL)
        return True, res.stdout, res.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except Exception as e:
        return False, "", str(e)

def ensure_git_pager(repo_path: str):
    # Check local config. Using a pager like less will cause the Agent CLI to hang indefinitely,
    # so we enforce setting core.pager to 'cat' locally if it's not already 'cat'.
    local_success, local_stdout, _ = run_cmd(["git", "config", "--local", "core.pager"], repo_path)
    local_pager = local_stdout.strip() if local_success else ""
    
    if local_pager != "cat":
        run_cmd(["git", "config", "--local", "core.pager", "cat"], repo_path)

@mcp.tool()
def git_status(repo_path: str) -> str:
    """
    Run 'git status' in the target repository.
    - repo_path: The absolute path of the git repository.
    """
    if not os.path.exists(repo_path):
        return f"Error: Path '{repo_path}' does not exist."
    ensure_git_pager(repo_path)
    success, stdout, stderr = run_cmd(["git", "status"], repo_path)
    return stdout if success else f"Error:\n{stderr}\nStdout:\n{stdout}"

@mcp.tool()
def git_add(repo_path: str, files: list[str] = None) -> str:
    """
    Run 'git add' on specific files or all files in the target repository.
    - repo_path: The absolute path of the git repository.
    - files: List of files to add. Defaults to ["."] (add all changes).
    """
    if not os.path.exists(repo_path):
        return f"Error: Path '{repo_path}' does not exist."
    ensure_git_pager(repo_path)
    if files is None:
        files = ["."]
    success, stdout, stderr = run_cmd(["git", "add"] + files, repo_path)
    return "Files added successfully." if success else f"Error adding files:\n{stderr}"

@mcp.tool()
def git_commit(repo_path: str, message: str) -> str:
    """
    Run 'git commit -m' to commit staged changes.
    - repo_path: The absolute path of the git repository.
    - message: The commit message. A signature '(committed by Antigravity Agent in VS Code)' will be appended.
    """
    if not os.path.exists(repo_path):
        return f"Error: Path '{repo_path}' does not exist."
    ensure_git_pager(repo_path)
    
    signature = " (committed by Antigravity Agent in VS Code)"
    if signature not in message:
        message += signature
        
    success, stdout, stderr = run_cmd(["git", "commit", "-m", message], repo_path)
    return stdout if success else f"Error committing:\n{stderr}\nStdout:\n{stdout}"

@mcp.tool()
def git_push(repo_path: str, remote: str = "", branch: str = "") -> str:
    """
    Run 'git push' to push committed changes to remote repository.
    - repo_path: The absolute path of the git repository.
    - remote: The remote name (e.g. 'origin'). Optional.
    - branch: The branch name (e.g. 'main'). Optional.
    """
    if not os.path.exists(repo_path):
        return f"Error: Path '{repo_path}' does not exist."
    ensure_git_pager(repo_path)
    
    github_txt_path = None
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_paths = [
        os.path.abspath(os.path.join(script_dir, "..", "..", "..", "private_security", "arv_ps_index.txt")),
        r"d:\fxn_arvin\antigravity_ai_\private_security\arv_ps_index.txt",
        r"f:\arv_google_antigravity\private_security\arv_ps_index.txt"
    ]
    fallback = r"d:\fxn_arvin\antigravity_ai_\private_security\arv_github.txt"
    for ip in index_paths:
        if os.path.exists(ip):
            try:
                with open(ip, "r", encoding="utf-8") as f:
                    for line in f:
                        if "=" in line:
                            key, value = line.split("=", 1)
                            if key.strip() == "SYS_NODE_93":
                                github_txt_path = os.path.join(os.path.dirname(ip), value.strip())
                                break
            except Exception as e:
                print(f"Error reading index file {ip}: {e}")
            if github_txt_path:
                break
    if not github_txt_path:
        github_txt_path = fallback

    repo_url = ""
    token = ""
    if github_txt_path and os.path.exists(github_txt_path):
        try:
            with open(github_txt_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith("GITHUB_REPO_URL="):
                        repo_url = line.split("=", 1)[1].strip()
                    elif line.startswith("GITHUB_TOKEN="):
                        token = line.split("=", 1)[1].strip()
        except Exception as e:
            return f"Error reading credentials file: {str(e)}"
            
    auth_url = ""
    if repo_url and token:
        if repo_url.startswith("https://"):
            auth_url = repo_url.replace("https://", f"https://{token}@")
            
    revert_url = False
    if auth_url:
        remote_name = remote if remote else "origin"
        success, _, stderr = run_cmd(["git", "remote", "set-url", remote_name, auth_url], repo_path)
        if success:
            revert_url = True
        else:
            return f"Error setting authenticated remote URL: {stderr}"
            
    try:
        cmd = ["git", "push"]
        if remote and branch:
            cmd.extend(["-u", remote, branch])
        elif branch:
            cmd.extend(["origin", branch])
            
        success, stdout, stderr = run_cmd(cmd, repo_path)
        return stdout if success else f"Error pushing:\n{stderr}\nStdout:\n{stdout}"
    finally:
        if revert_url:
            remote_name = remote if remote else "origin"
            run_cmd(["git", "remote", "set-url", remote_name, repo_url], repo_path)

@mcp.tool()
def git_diff(repo_path: str) -> str:
    """
    Run 'git diff' to view unstaged changes.
    - repo_path: The absolute path of the git repository.
    """
    if not os.path.exists(repo_path):
        return f"Error: Path '{repo_path}' does not exist."
    ensure_git_pager(repo_path)
    success, stdout, stderr = run_cmd(["git", "diff"], repo_path)
    return stdout if success else f"Error diffing:\n{stderr}"

@mcp.tool()
def git_log(repo_path: str, limit: int = 5) -> str:
    """
    Run 'git log' to see recent commit history.
    - repo_path: The absolute path of the git repository.
    - limit: The maximum number of commits to display (default is 5).
    """
    if not os.path.exists(repo_path):
        return f"Error: Path '{repo_path}' does not exist."
    ensure_git_pager(repo_path)
    success, stdout, stderr = run_cmd(["git", "log", "-n", str(limit)], repo_path)
    return stdout if success else f"Error loading log:\n{stderr}"

if __name__ == "__main__":
    mcp.run(transport='stdio')
