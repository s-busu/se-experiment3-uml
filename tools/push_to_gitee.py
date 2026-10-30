# -*- coding: utf-8 -*-
"""
一键推送脚本：在生成 gitee 私人令牌后运行即可。

用法：
    python tools/push_to_gitee.py <你的gitee私人令牌>

说明：
  1. gitee 自 2022 年起已禁用「账号 + 密码」方式推送代码，必须使用私人令牌；
  2. 令牌在 gitee 页面生成：右上角头像 -> 设置 -> 安全设置 -> 私人令牌 ->
     生成新令牌，勾选 projects 权限（只显示一次，务必复制）；
  3. 本脚本会用令牌创建仓库（若不存在）并把 master 分支推上去。
"""
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

GITEE = "https://gitee.com"
LOGIN = "skinpipi"
REPO = "se-exp3-uml"
ROOT = r"D:\软件工程\软件工程实验3"

lines = []


def log(msg):
    print(msg)
    lines.append(str(msg))


def api(path, token, method="GET", data=None):
    """gitee API 调用，token 走 access_token 参数。"""
    url = GITEE + path
    body = None
    headers = {"User-Agent": "workbuddy-agent"}
    if method == "GET":
        url += "?" + urllib.parse.urlencode({"access_token": token})
    else:
        body = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        return resp.getcode(), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main():
    if len(sys.argv) < 2:
        log("用法: python tools/push_to_gitee.py <gitee私人令牌>")
        log("")
        log("令牌获取步骤：")
        log("  1. 浏览器打开 https://gitee.com 并用 skinpipi 账号登录（需短信验证）")
        log("  2. 右上角头像 -> 设置 -> 安全设置 -> 私人令牌")
        log("  3. 点击「生成新令牌」，勾选 projects 权限，填写备注后生成")
        log("  4. 复制令牌（仅显示一次），然后运行本脚本")
        return 2

    token = sys.argv[1].strip()

    log("=== 1. 校验令牌 ===")
    code, body = api("/user", token)
    log("status=%d" % code)
    if code != 200:
        log("令牌无效或无权限：%s" % body[:300])
        return 1
    user = json.loads(body)
    log("登录用户: %s (%s)" % (user.get("login"), user.get("name")))

    log("=== 2. 确认/创建仓库 %s ===" % REPO)
    code, body = api("/repos/%s/%s" % (LOGIN, REPO), token)
    if code == 404:
        code, body = api("/user/repos", token, "POST", {
            "name": REPO, "path": REPO,
            "description": "软件工程实验三：面向对象的系统建模A — UML 类模型与 Java 实现",
            "private": "false", "auto_init": "false",
        })
        log("create status=%d %s" % (code, body[:300]))
        if code not in (200, 201):
            return 1
    else:
        log("仓库已存在: %s" % body[:120])

    log("=== 3. 推送到 gitee ===")
    os.chdir(ROOT)
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    url = "https://%s:%s@gitee.com/%s/%s.git" % (LOGIN, token, LOGIN, REPO)
    p = subprocess.run(["git", "push", "-u", url, "master:refs/heads/master"],
                       capture_output=True, env=env, timeout=600)
    log("push rc=%d" % p.returncode)
    log(p.stdout.decode("utf-8", "replace").strip())
    log(p.stderr.decode("utf-8", "replace").strip())

    if p.returncode == 0:
        log("")
        log("推送成功！仓库地址: https://gitee.com/%s/%s" % (LOGIN, REPO))
        # 设为 origin
        subprocess.run(["git", "remote", "add", "origin", url],
                       capture_output=True, env=env, timeout=60)
        subprocess.run(["git", "remote", "set-url", "origin", url],
                       capture_output=True, env=env, timeout=60)
        log("已设为 origin 远程仓库。")
        log("")
        log("请把报告第六节的仓库地址确认为：")
        log("  https://gitee.com/%s/%s" % (LOGIN, REPO))
    else:
        log("推送失败，请检查令牌权限（需包含 projects）。")

    with open(os.path.join(ROOT, "tools", "_push_gitee.log"), "w",
              encoding="utf-8") as f:
        f.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
