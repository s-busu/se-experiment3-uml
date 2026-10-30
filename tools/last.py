# -*- coding: utf-8 -*-
"""清理 stale index.lock，完成最后一次提交与推送。"""
import os
import subprocess
import time

ROOT = r"D:\软件工程\软件工程实验3"
env = dict(os.environ)
env["GIT_TERMINAL_PROMPT"] = "0"
USER = os.environ.get("GITHUB_USER", "s-busu")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPO", "se-experiment3-uml")
STAMP = time.strftime("%H%M%S")
LOG = os.path.join(ROOT, "tools", "_y%s.log" % STAMP)

lines = []


def flush():
    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def clear_lock():
    lock = os.path.join(ROOT, ".git", "index.lock")
    if not os.path.exists(lock):
        return
    ps = subprocess.run(["tasklist", "/FI", "IMAGENAME eq git.exe"],
                        capture_output=True, env=env, timeout=60)
    out = ps.stdout.decode("utf-8", "replace")
    if "git.exe" not in out:
        try:
            os.remove(lock)
            lines.append("stale index.lock removed")
        except Exception as e:
            lines.append("lock remove failed: %s" % e)
    else:
        lines.append("git.exe running, lock kept")
    flush()


def run(cmd, timeout=300):
    clear_lock()
    p = subprocess.run(cmd, capture_output=True, env=env, timeout=timeout, cwd=ROOT)
    safe = [c if "gho_" not in c else "<TOKEN>" for c in cmd]
    lines.append("$ " + " ".join(safe[:8]) + " rc=%d" % p.returncode)
    o = p.stdout.decode("utf-8", "replace").strip()
    e = p.stderr.decode("utf-8", "replace").strip()
    if o:
        lines.append("OUT: " + o[:1200])
    if e:
        lines.append("ERR: " + e[:1000])
    flush()
    return p


# prune.py 已被删除（用 prune2.py 替代），从索引移除
run(["git", "rm", "--cached", "tools/prune.py"])
run(["git", "add", "-A"])
run(["git", "commit", "-m", "chore: 清理临时文件"])

if TOKEN:
    tmp_url = "https://%s:%s@github.com/%s/%s.git" % (USER, TOKEN, USER, REPO)
    run(["git", "push", tmp_url, "master:refs/heads/master"])

run(["git", "status", "--short"])
p = subprocess.run(["git", "ls-files"], capture_output=True, env=env,
                   timeout=60, cwd=ROOT)
tracked = p.stdout.decode("utf-8", "replace").splitlines()
lines.append("tracked=%d" % len(tracked))
lines.append("\n".join(tracked))
lines.append("root: " + ", ".join(sorted(os.listdir(ROOT))))

flush()
print("DONE")
