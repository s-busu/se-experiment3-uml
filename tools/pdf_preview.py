# -*- coding: utf-8 -*-
"""把 PDF 渲染为分页 PNG，用于目检报告排版。"""
import fitz
import os

pdf = r"D:\软件工程\软件工程实验3\report_preview.pdf"
outdir = r"D:\软件工程\软件工程实验3\_preview"
os.makedirs(outdir, exist_ok=True)

doc = fitz.open(pdf)
lines = []
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=110)
    p = os.path.join(outdir, "page%02d.png" % (i + 1))
    pix.save(p)
    lines.append("page %d -> %s (%dx%d)" % (i + 1, p, pix.width, pix.height))

open(r"D:\软件工程\软件工程实验3\_preview.txt", "w", encoding="utf-8").write("\n".join(lines))
print("pages:", len(doc))
