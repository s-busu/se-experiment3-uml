# -*- coding: utf-8 -*-
"""渲染保存后的报告首页，目检封面是否已删除。"""
import os
import fitz

PDF = r"D:\软件工程\软件工程实验3\_check.pdf"
DOCX = r"D:\软件工程\软件工程实验3\202410120323-柳淳-软件工程实验三.docx"

# 若 PDF 未生成（Word COM 不可用），用 docx2pdf 不可得时退而检查 docx 段落
if os.path.isfile(PDF):
    doc = fitz.open(PDF)
    print("pages:", len(doc))
    for i in range(min(2, len(doc))):
        p = os.path.join(r"D:\软件工程\软件工程实验3", "_chk_p%d.png" % (i + 1))
        doc[i].get_pixmap(dpi=100).save(p)
        print("saved", p)
    print("--- page1 text ---")
    print(doc[0].get_text()[:600])
else:
    print("no pdf")
