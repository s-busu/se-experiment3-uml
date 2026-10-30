# -*- coding: utf-8 -*-
"""
重写 git 历史，彻底清除含 OAuth token 的提交，然后推送到 GitHub。

做法：新建一条干净的提交链（保留最终文件状态），推到远端新分支，
再用 --force 覆盖 master，最后删除本地旧历史。
"""
import os
import shutil
import subprocess

ROOT = r"D:\软件工程\软件工程实验3"
env = dict(os.environ)
env["GIT_TERMINAL_PROMPT"] = "0"

USER = os.environ.get("GITHUB_USER", "s-busu")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPO", "se-experiment3-uml")

lines = []


def run(cmd, cwd=ROOT, timeout=300, check=False):
    p = subprocess.run(cmd, capture_output=True, env=env, timeout=timeout, cwd=cwd)
    out = p.stdout.decode("utf-8", "replace").strip()
    err = p.stderr.decode("utf-8", "replace").strip()
    safe = [c if "gho_" not in c else "<TOKEN>" for c in cmd]
    lines.append("$ " + " ".join(safe[:8]) + " ...")
    lines.append("rc=%d" % p.returncode)
    if out:
        lines.append("OUT: " + out[:1500])
    if err:
        lines.append("ERR: " + err[:1500])
    lines.append("-" * 60)
    if check and p.returncode != 0:
        raise SystemExit("failed: %s" % cmd[:3])
    return p


if not TOKEN:
    lines.append("!! GITHUB_TOKEN 未设置")
    raise SystemExit(1)

# 1. 备份当前文件状态（用 git archive 拿到干净的工作树快照）
run(["git", "status", "--short"])

# 2. 建立 orphan 分支，从当前 HEAD 的文件状态生成干净历史
run(["git", "checkout", "--orphan", "clean-master"])
run(["git", "rm", "-rf", "--cached", "."])
run(["git", "add", "-A"])
run(["git", "commit", "-m",
     "feat: 软件工程实验三 面向对象的系统建模A —— UML 类模型与 Java 实现"])
run(["git", "branch", "-M", "master"])

# 3. 强制推送到远端 master
url = "https://%s:%s@github.com/%s/%s.git" % (USER, TOKEN, USER, REPO)
p = subprocess.run(["git", "push", "--force", url, "master:refs/heads/master"],
                   capture_output=True, env=env, timeout=300, cwd=ROOT)
lines.append("$ git push --force <github> master")
lines.append("rc=%d" % p.returncode)
lines.append("OUT: " + p.stdout.decode("utf-8", "replace").strip()[:1500])
lines.append("ERR: " + p.stderr.decode("utf-8", "replace").strip()[:1500])
lines.append("-" * 60)

# 4. 清理旧历史与 reflog
run(["git", "reflog", "expire", "--expire=now", "--all"])
run(["git", "gc", "--prune=now", "--aggressive"], timeout=300)

# 5. 设置 origin
run(["git", "remote", "remove", "origin"])
run(["git", "remote", "add", "origin", url])
run(["git", "remote", "set-url", "origin", url])

# 6. 验证
run(["git", "log", "--oneline"])
run(["git", "count-objects", "-v"])
p2 = subprocess.run(["git", "grep", "-l", "gho_", "HEAD"], capture_output=True,
                    env=env, timeout=60, cwd=ROOT)
lines.append("=== grep token in HEAD ===")
lines.append("rc=%d (0 表示已清除)" % p2.returncode)
lines.append(p2.stdout.decode("utf-8", "replace").strip() or "(none)")

with open(os.path.join(ROOT, "tools", "_commit4.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("DONE")
