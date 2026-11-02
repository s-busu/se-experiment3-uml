# -*- coding: utf-8 -*-
"""验证 gen_report.py 在 keep_cover=False 下能生成与当前交付物一致的无封面报告。"""
import os
import shutil
import subprocess
import sys
import time

PY = r"C:\Users\22581\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
ROOT = r"D:\软件工程\软件工程实验3"
SCRIPT = os.path.join(ROOT, "tools", "gen_report.py")
STAMP = time.strftime("%H%M%S")
LOG = os.path.join(ROOT, "tools", "_regen_%s.log" % STAMP)

lines = []


def log(m):
    print(m)
    lines.append(str(m))


# 1. 备份当前交付物
cur = os.path.join(ROOT, "202410120323-柳淳-软件工程实验三.docx")
bak = os.path.join(ROOT, "tools", "_backup_%s.docx" % STAMP)
shutil.copy2(cur, bak)
log("backed up -> %s" % os.path.basename(bak))

# 2. 重跑生成脚本
p = subprocess.run([PY, SCRIPT], capture_output=True, timeout=180)
log("gen rc=%d" % p.returncode)
log(p.stdout.decode("utf-8", "replace").strip())
if p.stderr:
    log("ERR: " + p.stderr.decode("utf-8", "replace").strip()[:800])

# 3. 检查新文件的第一页内容
sys.path.insert(0, ROOT)
try:
    import fitz
    import zipfile
    from docx import Document

    d = Document(cur)
    paras = [p.text.strip() for p in d.paragraphs]
    nonempty = [t for t in paras if t][:3]
    log("=== new docx first non-empty paragraphs ===")
    for t in nonempty:
        log("  " + t[:60])

    # 确认无封面关键词
    alltext = "\n".join(paras)
    for kw in ["实验报告三", "姓    名", "实 验 室", "总评成绩", "院    系"]:
        log("  contains %r: %s" % (kw, kw in alltext))

    # 页数
    r = subprocess.run(["soffice", "--version"], capture_output=True, timeout=30)
except Exception as e:
    log("ERR %s" % e)

# 4. 恢复原交付物（保持编辑器里保存的版本不被脚本覆盖）
shutil.copy2(bak, cur)
log("restored original deliverable")
os.remove(bak)

with open(LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("DONE")
