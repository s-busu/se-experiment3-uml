# -*- coding: utf-8 -*-
"""
调用 editor_sdk 的 doc_resolve_document_structure，把节点解析成紧凑表格，
便于精确定位封面页的段落范围。
"""
import json
import os
import subprocess
import sys
import time

SKILL = r"D:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\workbuddy-local-office-edit"
PY = r"C:\Users\22581\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
FILE_ID = r"D:\软件工程\软件工程实验3\202410120323-柳淳-软件工程实验三.docx"
ARGS = r"D:\软件工程\软件工程实验3\tools\_args_call.json"
OUT = r"D:\软件工程\软件工程实验3\tools\_struct_table.txt"


def call(tool, args):
    with open(ARGS, "w", encoding="utf-8") as f:
        json.dump(args, f, ensure_ascii=False)
    p = subprocess.run([PY, "edsdk.py", "call", tool, "--json-file", ARGS],
                       capture_output=True, cwd=SKILL, timeout=180)
    out = p.stdout.decode("utf-8", "replace")
    # 输出可能前面带说明行，取第一个 { 开头的 JSON 块
    i = out.find("{")
    if i < 0:
        raise RuntimeError("no json in output: %s | %s" % (out[:300],
                                                           p.stderr.decode("utf-8", "replace")[:300]))
    return json.loads(out[i:])


def main():
    offset = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 40

    res = call("doc_resolve_document_structure", {
        "file_id": FILE_ID, "mode": "compact",
        "text_preview_length": 60, "limit": limit, "offset": offset})

    nodes = res.get("nodes", [])
    lines = []
    lines.append("total nodes returned: %d (offset=%d)" % (len(nodes), offset))
    lines.append("%-4s %-6s %-6s %-10s %s" % ("idx", "start", "end", "type", "preview"))
    lines.append("-" * 100)
    for n in nodes:
        lines.append("%-4s %-6s %-6s %-10s %s" % (
            n.get("paragraph_index"), n.get("start_index"), n.get("end_index"),
            n.get("type"), (n.get("text_preview") or "").replace("\n", "\\n")))

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", OUT, "nodes:", len(nodes))


if __name__ == "__main__":
    main()
