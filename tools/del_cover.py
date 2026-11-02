# -*- coding: utf-8 -*-
"""
删除实验报告的封面页（第一页）。

封面 = 结构里的段落 1..20（其中第 20 段是模板遗留的分页符段落），
第 21 段起是正文「一、实验目的」。

按 doc.md 要求：删除多段必须从后往前逐次调用，并重新查 idx。
本脚本从段落 20 倒序删到段落 1，每删一段后重新拉结构，
用段落文本校验目标正确后再删下一段。
"""
import json
import os
import subprocess
import time

SKILL = r"D:\WorkBuddy\resources\app.asar.unpacked\resources\plugins\workbuddy-builtin\skills\workbuddy-local-office-edit"
PY = r"C:\Users\22581\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
FILE_ID = r"D:\软件工程\软件工程实验3\202410120323-柳淳-软件工程实验三.docx"
ARGS = r"D:\软件工程\软件工程实验3\tools\_args_call.json"
LOG = r"D:\软件工程\软件工程实验3\tools\_del_cover_%s.log" % time.strftime("%H%M%S")

lines = []


def log(m):
    print(m)
    lines.append(str(m))


def call(tool, args):
    with open(ARGS, "w", encoding="utf-8") as f:
        json.dump(args, f, ensure_ascii=False)
    p = subprocess.run([PY, "edsdk.py", "call", tool, "--json-file", ARGS],
                       capture_output=True, cwd=SKILL, timeout=180)
    out = p.stdout.decode("utf-8", "replace")
    i = out.find("{")
    if i < 0:
        raise RuntimeError("no json: %s | %s" % (out[:400],
                                                 p.stderr.decode("utf-8", "replace")[:400]))
    data = json.loads(out[i:])
    if data.get("ok") is False:
        raise RuntimeError("tool %s failed: %s" % (tool, data))
    return data


def nodes(limit=40, offset=0):
    res = call("doc_resolve_document_structure", {
        "file_id": FILE_ID, "mode": "compact",
        "text_preview_length": 60, "limit": limit, "offset": offset})
    return res.get("nodes", [])


def main():
    # 1. 记录删除前的结构
    before = nodes(30, 0)
    log("=== BEFORE ===")
    for n in before[:22]:
        log("  P%-3s [%s,%s] %s" % (n.get("paragraph_index"), n.get("start_index"),
                                   n.get("end_index"),
                                   (n.get("text_preview") or "")[:50]))

    # 2. 确认第 21 段是「一、实验目的」（正文的真正起点）
    target = None
    for n in before:
        if n.get("paragraph_index") == 21:
            target = n
    if not target or "一、实验目的" not in (target.get("text_preview") or ""):
        log("!! 第21段不是「一、实验目的」，中止")
        return 1
    log("确认：P21 = %r，正文从 idx=%s 开始" % (target.get("text_preview"),
                                          target.get("start_index")))

    # 3. 从后往前删除段落 20..1
    #    倒序删除时，前面的段落 start_index 不受影响，但每轮仍重新取结构校验
    for pindex in range(20, 0, -1):
        cur = nodes(30, 0)
        node = None
        for n in cur:
            if n.get("paragraph_index") == pindex:
                node = n
                break
        if node is None:
            log("  P%d 已不存在，跳过" % pindex)
            continue
        idx = node["start_index"]
        preview = (node.get("text_preview") or "")[:40]
        try:
            call("doc_delete_paragraph", {"file_id": FILE_ID, "idx": idx})
            log("  已删除 P%-3d idx=%-5s %r" % (pindex, idx, preview))
        except Exception as e:
            log("  !! 删除 P%d (idx=%s) 失败: %s" % (pindex, idx, e))
            raise

    # 4. 删除后的结构
    after = nodes(10, 0)
    log("=== AFTER ===")
    for n in after:
        log("  P%-3s [%s,%s] %s" % (n.get("paragraph_index"), n.get("start_index"),
                                   n.get("end_index"),
                                   (n.get("text_preview") or "")[:50]))

    with open(LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
