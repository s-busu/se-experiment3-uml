# -*- coding: utf-8 -*-
"""清理探测过程中产生的临时文件。"""
import glob
import os
import shutil

root = r"D:\软件工程\软件工程实验3"
removed = []

for p in glob.glob(os.path.join(root, "_*.txt")):
    try:
        os.remove(p)
        removed.append(os.path.basename(p))
    except Exception as e:
        pass

for name in ["page411.html", "report_preview.pdf"]:
    p = os.path.join(root, name)
    if os.path.isfile(p):
        try:
            os.remove(p)
            removed.append(name)
        except Exception:
            pass

prev = os.path.join(root, "_preview")
if os.path.isdir(prev):
    shutil.rmtree(prev, ignore_errors=True)
    removed.append("_preview/")

left = sorted(os.listdir(root))
open(os.path.join(root, "tools", "_cleanup.log"), "w", encoding="utf-8").write(
    "removed %d items\nremaining:\n%s" % (len(removed), "\n".join(left)))
print("removed", len(removed))
print("\n".join(left))
