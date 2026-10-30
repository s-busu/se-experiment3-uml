# -*- coding: utf-8 -*-
"""
由 tools/model_def.py 生成 UML 2.1 XMI 文件。

Rational Rose 2007 / Visual Paradigm / Enterprise Architect 等主流 UML 工具
均支持导入 UML 2.1 XMI，从而可以直接打开本实验构建的类图模型
并在 Rose 中继续编辑、导出 .md 工程文件。

实现说明：采用字符串直接拼装 XML，避免 ElementTree 对前缀/默认命名空间的
处理差异，确保输出的 XMI 严格符合 UML 2.1 XMI 结构。
"""
import os
import sys
from xml.sax.saxutils import escape, quoteattr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_def import ALL_MODELS, ASSOC, AGG, COMP, GEN  # noqa: E402

XMI_NS = "http://schema.omg.org/spec/XMI/2.1"
UML_NS = "http://schema.omg.org/spec/UML/2.1"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

VIS_MAP = {"public": "public", "private": "private",
           "protected": "protected", "package": "package"}

OUT_DIR = r"D:\软件工程\软件工程实验3\model"

_counter = [0]


def xid(prefix):
    _counter[0] += 1
    return "%s_%04d" % (prefix, _counter[0])


def att(name, value):
    if value is None:
        return ""
    return " %s=%s" % (name, quoteattr(str(value)))


def el(name, attrs=None, children=None, text=None, indent=0):
    """生成一个 XML 元素字符串。"""
    pad = "  " * indent
    head = "<%s%s" % (name, "".join(att(k, v) for k, v in (attrs or [])))
    if text is not None:
        return "%s%s>%s</%s>\n" % (pad, head, escape(text), name)
    if not children:
        return "%s%s/>\n" % (pad, head)
    inner = "".join(children)
    return "%s%s>\n%s%s</%s>\n" % (pad, head, inner, pad, name)


def comment(text, indent):
    return el("uml:ownedComment", [
        ("xmi:id", xid("cmt")),
    ], children=[
        el("uml:body", [], text=text, indent=indent + 1),
    ], indent=indent)


def primitive_type(type_name, indent):
    return el("uml:type", [], children=[
        el("uml:PrimitiveType", [("xmi:id", xid("pt")), ("name", type_name)],
           indent=indent + 1),
    ], indent=indent)


def build_class(c, indent=2):
    attrs = [("xmi:id", xid("cls")), ("name", c.name), ("visibility", "public")]
    if c.abstract:
        attrs.append(("isAbstract", "true"))
    if c.stereotype:
        attrs.append(("xmi.stereotype", c.stereotype))

    children = []
    if c.note:
        children.append(comment(c.note, indent + 1))

    for a in c.attrs:
        aattrs = [("xmi:id", xid("attr")), ("name", a.name),
                  ("visibility", VIS_MAP[a.visibility]), ("isReadOnly", "false")]
        if a.multiplicity:
            aattrs.append(("multiplicity", a.multiplicity))
        achildren = []
        if a.type:
            achildren.append(primitive_type(a.type, indent + 2))
        if a.note:
            achildren.append(comment(a.note, indent + 2))
        children.append(el("uml:ownedAttribute", aattrs,
                           children=achildren, indent=indent + 1))

    for o in c.ops:
        oattrs = [("xmi:id", xid("op")), ("name", o.name),
                  ("visibility", VIS_MAP[o.visibility]), ("isQuery", "false")]
        ochildren = []
        for pname, ptype, pvis in o.params:
            ochildren.append(el("uml:ownedParameter", [
                ("xmi:id", xid("param")), ("name", pname),
                ("visibility", VIS_MAP[pvis]), ("kind", "in"),
            ], children=[primitive_type(ptype, indent + 3)], indent=indent + 2))
        if o.return_type and o.return_type != "void":
            ochildren.append(primitive_type(o.return_type, indent + 2))
        if o.note:
            ochildren.append(comment(o.note, indent + 2))
        children.append(el("uml:ownedOperation", oattrs,
                           children=ochildren, indent=indent + 1))

    return el("uml:packagedElement", attrs, children=children, indent=indent)


def build_rel(r, indent=2):
    if r.kind == GEN:
        attrs = [("xmi:type", "uml:Generalization"), ("xmi:id", xid("rel")),
                 ("name", r.name or "")]
        children = [
            el("uml:generalChild", [("xmi:id", xid("gen")), ("name", r.source)],
               indent=indent + 1),
            el("uml:generalParent", [("xmi:id", xid("gen")), ("name", r.target)],
               indent=indent + 1),
        ]
        return el("uml:ownedRelationship", attrs, children=children, indent=indent)

    attrs = [("xmi:type", "uml:Association"), ("xmi:id", xid("rel")),
             ("name", r.name or ""), ("visibility", "public")]
    if r.kind == AGG:
        attrs.append(("isAggregate", "true"))
    elif r.kind == COMP:
        attrs.append(("isComposite", "true"))

    children = []
    for role, cls_name, mult in (
        (r.source_role, r.source, r.source_mult),
        (r.target_role, r.target, r.target_mult),
    ):
        end_children = [
            el("uml:type", [], children=[
                el("uml:Class", [("xmi:id", xid("clsref")), ("name", cls_name)],
                   indent=indent + 3),
            ], indent=indent + 2),
        ]
        children.append(el("uml:ownedEnd", [
            ("xmi:id", xid("end")), ("name", role or ""),
            ("visibility", "public"), ("isNavigable", "true"),
            ("multiplicity", mult),
        ], children=end_children, indent=indent + 1))

    if r.note:
        children.append(comment(r.note, indent + 1))

    return el("uml:ownedRelationship", attrs, children=children, indent=indent)


def build_xmi(m):
    _counter[0] = 0
    head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<xmi:XMI xmlns:xmi="%s" xmlns:uml="%s" xmlns:xsi="%s"\n'
            '    xmi:version="2.1"\n'
            '    xsi:schemaLocation="%s http://schema.omg.org/spec/UML/20110401/UML.xmi">\n'
            % (XMI_NS, UML_NS, XSI_NS, XMI_NS))

    pkg_children = []
    for c in m.classes:
        pkg_children.append(build_class(c, indent=2))
    for r in m.rels:
        pkg_children.append(build_rel(r, indent=2))

    pkg = el("uml:packagedElement", [
        ("xmi:id", xid("pkg")), ("name", m.title), ("visibility", "public"),
    ], children=pkg_children, indent=1)

    model = el("uml:Model", [
        ("xmi:id", xid("model")), ("name", "软件工程实验三-%s" % m.key),
    ], children=[pkg], indent=0)

    return head + model + "</xmi:XMI>\n"


def main():
    for m in ALL_MODELS:
        xml = build_xmi(m)
        fname = "%s-model.xmi" % m.key.lower()
        path = os.path.join(OUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(xml)
        # 校验 XML 合法性
        import xml.etree.ElementTree as ET
        ET.parse(path)
        print("wrote %s (%d bytes) - XML valid" % (path, len(xml.encode("utf-8"))))


if __name__ == "__main__":
    main()
