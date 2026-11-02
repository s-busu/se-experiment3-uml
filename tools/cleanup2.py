# -*- coding: utf-8 -*-
"""清理目检用的临时文件。"""
import os
import shutil

ROOT = r"D:\软件工程\软件工程实验3"
for name in ["_check.pdf", "_chk_p1.png", "_chk_p2.png"]:
    p = os.path.join(ROOT, name)
    if os.path.isfile(p):
        try:
            os.remove(p)
            print("removed", name)
        except Exception as e:
            print("skip", name, e)
print("root:", ", ".join(sorted(os.listdir(ROOT))))
