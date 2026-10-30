# -*- coding: utf-8 -*-
"""清理诊断阶段的一次性脚本，只保留有复用价值的工具。"""
import os
import shutil

ROOT = r"D:\软件工程\软件工程实验3"
TOOLS = os.path.join(ROOT, "tools")

# 保留：与实验产物直接相关、可复用的脚本
KEEP = {
    "model_def.py",        # 模型的单一事实来源
    "gen_xmi.py",          # 生成 UML 2.1 XMI
    "gen_report.py",       # 生成实验报告
    "pdf_preview.py",      # 报告 PDF 分页渲染（目检）
    "push_to_gitee.py",    # 一键推送脚本
    "cleanup.py",          # 清理临时文件
}

removed = []
for fn in sorted(os.listdir(TOOLS)):
    fp = os.path.join(TOOLS, fn)
    if not os.path.isfile(fp):
        continue
    if fn in KEEP:
        continue
    # 删掉所有诊断日志与一次性脚本
    os.remove(fp)
    removed.append(fn)

# 清理 tools 下残留的 log
for fn in os.listdir(TOOLS):
    fp = os.path.join(TOOLS, fn)
    if os.path.isfile(fp) and (fn.endswith(".log") or fn.startswith("_")):
        os.remove(fp)
        removed.append(fn)

with open(os.path.join(TOOLS, ".keep"), "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(os.listdir(TOOLS))))

print("removed %d files" % len(removed))
print("kept:", ", ".join(sorted(os.listdir(TOOLS))))
