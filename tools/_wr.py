# -*- coding: utf-8 -*-
"""把会话辅助脚本 last.py 移出版本库并推送，保持仓库只含实验产物。"""
import os
import shutil
import subprocess
import time

ROOT = r"D:\软件工程\软件工程实验3"
env = dict(os.environ)
env["GIT_TERMINAL_PROMPT"] = "0"
USER = os.environ.get("GITHUB_USER", "s-busu")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPO", "se-experiment3-uml")
STAMP = time.strftime("%H%M%S")
LOG = os.path.join(ROOT, "tools", "_w%s.log" % STAMP)

lines = []


def flush():
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def clear_lock():
    lock = os.path.join(ROOT, ".git", "index.lock")
    if os.path.exists(lock):
        ps = subprocess.run(["tasklist", "/FI", "IMAGENAME eq git.exe"],
                            capture_output=True, env=env, timeout=60)
        if "git.exe" not in ps.stdout.decode("utf-8", "replace"):
            try:
                os.remove(lock)
                lines.append("lock cleared")
            except Exception as e:
                lines.append("lock err %s" % e)
            flush()


def run(cmd, timeout=300):
    clear_lock()
    p = subprocess.run(cmd, capture_output=True, env=env, timeout=timeout, cwd=ROOT)
    safe = [c if "gho_" not in c else "<TOKEN>" for c in cmd]
    lines.append("$ " + " ".join(safe[:8]) + " rc=%d" % p.returncode)
    o = p.stdout.decode("utf-8", "replace").strip()
    e = p.stderr.decode("utf-8", "replace").strip()
    if o:
        lines.append("OUT: " + o[:800])
    if e:
        lines.append("ERR: " + e[:800])
    flush()
    return p


# 把 last.py 移到 _scratch，并加进 .gitignore
scratch = os.path.join(ROOT, "tools", "_scratch")
os.makedirs(scratch, exist_ok=True)
try:
    shutil.move(os.path.join(ROOT, "tools", "last.py"),
                os.path.join(scratch, "last.py"))
    lines.append("last.py moved to _scratch")
except Exception as e:
    lines.append("move err %s" % e)

gi = os.path.join(ROOT, ".gitignore")
with open(gi, encoding="utf-8") as f:
    content = f.read()
if "tools/last.py" not in content:
    content = content.replace("tools/prune2.py", "tools/prune2.py\ntools/last.py")
    with open(gi, "w", encoding="utf-8") as f:
        f.write(content)
    lines.append("gitignore updated")
flush()

run(["git", "rm", "--cached", "tools/last.py"])
run(["git", "add", "-A"])
run(["git", "commit", "-m", "chore: 移除会话辅助脚本，仓库仅保留实验产物"])

if TOKEN:
    tmp_url = "https://%s:%s@github.com/%s/%s.git" % (USER, TOKEN, USER, REPO)
    run(["git", "push", tmp_url, "master:refs/heads/master"])

run(["git", "status", "--short"])
p = subprocess.run(["git", "ls-files", "tools/"], capture_output=True, env=env,
                   timeout=60, cwd=ROOT)
lines.append("tools tracked:\n" + p.stdout.decode("utf-8", "replace"))
run(["git", "log", "--oneline"])

flush()
print("DONE")
