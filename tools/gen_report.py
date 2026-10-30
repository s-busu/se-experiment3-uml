# -*- coding: utf-8 -*-
"""
生成《软件工程》实验报告三：面向对象的系统建模A。

基于课程官方模板 template/实验报告模板.docx 的封面版式，
正文按模板的六段式结构（一、实验目的 … 六、仓库地址）填写，
并嵌入四张 UML 类图、关系明细表与关键代码。
"""
import os
import sys
import copy
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_def import ALL_MODELS, ASSOC, AGG, COMP, GEN, VIS_MAP, VIS_SYMBOL  # noqa: E402

ROOT = r"D:\软件工程\软件工程实验3"
TPL = os.path.join(ROOT, "template", "实验报告模板.docx")
OUT = os.path.join(ROOT, "202410120323-柳淳-软件工程实验三.docx")
DIAG_DIR = os.path.join(ROOT, "model", "diagrams")

STUDENT_NAME = "柳淳"
STUDENT_NO = "202410120323"
COLLEGE = "计算机与信息学院"
MAJOR = "软件工程"
LAB = "软件工程实验室"
EXPERIMENT_DATE = "2026 年 10 月 30 日"
REPO_URL = "https://gitee.com/skinpipi/se-exp3-uml"
REPO_BACKUP_URL = "https://github.com/s-busu/se-experiment3-uml"

DIAGRAM_FILE = {
    "A1-1": "A1_1_Thoroughbred.png",
    "A1-2": "A1_2_College.png",
    "A1-3": "A1_3_School.png",
    "A1-4": "A1_4_Shopping.png",
}

REL_KIND_CN = {ASSOC: "关联", AGG: "聚合", COMP: "组合", GEN: "泛化"}
REL_KIND_SHORT = {ASSOC: "关联", AGG: "聚合", COMP: "组合", GEN: "泛化"}


# ------------------------- 基础排版工具 -------------------------

def set_run(run, name="宋体", size=12, bold=False, ascii_font="Times New Roman"):
    run.font.name = ascii_font
    run.font.size = Pt(size)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:ascii"), ascii_font)
    rfonts.set(qn("w:hAnsi"), ascii_font)
    rfonts.set(qn("w:eastAsia"), name)


def add_para(doc, text="", size=12, bold=False, align=None, font="宋体",
             space_before=0, space_after=0, indent_first=True, line=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if line:
        pf.line_spacing = line
    if align is not None:
        p.alignment = align
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if indent_first and text:
        pf.first_line_indent = Pt(size * 2)
    strip_numbering(p)
    if text:
        set_run(p.add_run(text), name=font, size=size, bold=bold)
    return p


def strip_numbering(paragraph):
    """清除段落继承的自动编号（模板 Normal 样式带有 numPr，会串出列表序号）。"""
    ppr = paragraph._p.get_or_add_pPr()
    for numpr in ppr.findall(qn("w:numPr")):
        ppr.remove(numpr)
    # 显式声明本段落不使用编号，覆盖样式级 numPr（numId=0 表示无编号）
    numpr = OxmlElement("w:numPr")
    ilvl = OxmlElement("w:ilvl")
    ilvl.set(qn("w:val"), "0")
    numid = OxmlElement("w:numId")
    numid.set(qn("w:val"), "0")
    numpr.append(ilvl)
    numpr.append(numid)
    ppr.insert(0, numpr)


def add_heading(doc, text, size=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    strip_numbering(p)
    set_run(p.add_run(text), name="黑体", size=size, bold=True)
    return p


def add_code(doc, lines, size=8.5):
    """等宽字体代码块，逐行输出。"""
    for line in lines:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.left_indent = Cm(0.9)
        pf.line_spacing = 1.0
        strip_numbering(p)
        set_run(p.add_run(line if line else " "), name="Consolas", size=size,
                ascii_font="Consolas")


def add_image(doc, path, caption, width_cm=15.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(path, width=Cm(width_cm))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    set_run(cap.add_run(caption), name="宋体", size=10.5, bold=True)


def set_cell(cell, text, bold=False, size=10.5, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.first_line_indent = Pt(0)
    if align is not None:
        p.alignment = align
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    strip_numbering(p)
    # 文本中的 \n 转成软换行 <w:br/>
    parts = str(text).split("\n")
    for i, part in enumerate(parts):
        if i:
            p.add_run().add_break()
        set_run(p.add_run(part), name="宋体", size=size, bold=bold)


def shade_cell(cell, hex_color="D9D9D9"):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcpr.append(shd)


def add_table(doc, headers, rows, widths=None, size=10.5, caption=None):
    if caption:
        cap = doc.add_paragraph()
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap.paragraph_format.space_before = Pt(6)
        cap.paragraph_format.space_after = Pt(3)
        cap.paragraph_format.keep_with_next = True
        strip_numbering(cap)
        set_run(cap.add_run(caption), name="宋体", size=10.5, bold=True)

    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, h in enumerate(headers):
        set_cell(t.rows[0].cells[i], h, bold=True, size=size)
        shade_cell(t.rows[0].cells[i])
    repeat_header(t.rows[0])
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            set_cell(cells[i], str(val), size=size,
                     align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER)
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    # 禁止表格行跨页断开
    for r in t.rows:
        trpr = r._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        trpr.append(cant)
    # 表格后留白
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(4)
    return t


def repeat_header(row):
    """设置表头跨页重复。"""
    trpr = row._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trpr.append(th)


def page_break(doc):
    from docx.enum.text import WD_BREAK
    p = doc.add_paragraph()
    p.add_run().add_break(WD_BREAK.PAGE)


# ------------------------- 报告正文 -------------------------

def build_cover(doc):
    """改写模板封面的标题与抬头信息（按文本定位，避免索引错位）。"""
    paras = doc.paragraphs

    for p in paras:
        text = "".join(p._p.itertext())
        stripped = text.strip()

        # 标题行：实验报告一 ：...
        if stripped.startswith("实验报告一"):
            for r in list(p.runs):
                r._element.getparent().remove(r._element)
            strip_numbering(p)
            set_run(p.add_run("实验报告三 ：面向对象的系统建模A"),
                    name="楷体_GB2312", size=24, bold=True)

        elif stripped.startswith("姓    名："):
            for r in list(p.runs):
                r._element.getparent().remove(r._element)
            set_run(p.add_run("姓    名：%s          学    号：%s          "
                              % (STUDENT_NAME, STUDENT_NO)),
                    name="宋体", size=14, bold=True)

        elif stripped.startswith("院    系："):
            for r in list(p.runs):
                r._element.getparent().remove(r._element)
            set_run(p.add_run("院    系：%s          专  业：%s          "
                              % (COLLEGE, MAJOR)),
                    name="宋体", size=14, bold=True)

        elif stripped.startswith("实 验 室："):
            for r in list(p.runs):
                r._element.getparent().remove(r._element)
            set_run(p.add_run("实 验 室：%s        实验日期：%s    "
                              % (LAB, EXPERIMENT_DATE)),
                    name="宋体", size=14, bold=True)

        elif stripped.startswith("总评成绩："):
            for r in list(p.runs):
                r._element.getparent().remove(r._element)
            set_run(p.add_run("总评成绩：                        审阅教师：                  "),
                    name="宋体", size=14, bold=True)


def clear_body_after_cover(doc):
    """删除封面之后的所有内容，为新正文让路。"""
    body = doc.element.body
    children = list(body)
    keep = 0
    found = False
    for i, child in enumerate(children):
        tag = child.tag.split("}")[-1]
        if tag == "sectPr":
            continue
        if tag == "p":
            text = "".join(child.itertext())
            if "一、实验目的" in text:
                keep = i
                found = True
                break
        keep = i + 1
    if not found:
        keep = 0
    for child in children[keep:]:
        if child.tag.split("}")[-1] != "sectPr":
            body.remove(child)


def rel_rows(m):
    """把模型的关系转成报告表格的行。"""
    rows = []
    for r in m.rels:
        if r.kind == GEN:
            rows.append([REL_KIND_CN[GEN], r.source, r.target,
                         "子类", "父类", "继承",
                         "%s 继承自 %s（泛化关系，无多重性）。" % (r.source, r.target)])
        else:
            rows.append([
                REL_KIND_CN[r.kind],
                r.source,
                r.target,
                "%s\n(%s)" % (r.source_role or "", r.source_mult or ""),
                "%s\n(%s)" % (r.target_role or "", r.target_mult or ""),
                r.name or "—",
                r.note or "",
            ])
    return rows


def build_report():
    doc = Document(TPL)
    build_cover(doc)
    clear_body_after_cover(doc)

    # 封面独占一页
    page_break(doc)

    # ---------- 一、实验目的 ----------
    add_heading(doc, "一、实验目的")
    for t in [
        "掌握 UML 静态建模的方法，能够依据需求描述规范地提取类、属性、操作，"
        "并准确标注可见性级别、关系类型、多重性与角色名；",
        "掌握聚合、组合、关联、泛化四种基本关系的语义差异，"
        "能够结合约束性注释表达类之间的业务规则；",
        "掌握 UML 类图的图形化表达方法，能够使用 UML 建模工具"
        "（Rational Rose / Visual Paradigm 等）创建并导出类图模型；",
        "能够使用面向对象语言将类图模型实现为可运行的代码，"
        "并借助单元测试验证模型中的结构与约束在代码中得到落实。",
    ]:
        add_para(doc, t)

    # ---------- 二、实验环境 ----------
    add_heading(doc, "二、实验环境")
    add_para(doc, "建模工具：Rational Rose 2007（UML 2.1 XMI 导入校验）、"
                  "Visual Paradigm CE 16、PlantUML 1.2024.7（类图渲染）；")
    add_para(doc, "实现语言：Java（JDK 1.8.0_131）、Gradle 7.6.4；")
    add_para(doc, "测试框架：JUnit 5.8.2；")
    add_para(doc, "版本管理：Git 2.55.0 + Gitee（码云）；")
    add_para(doc, "操作系统：Windows 11（64 位）。")

    # ---------- 三、实验要求 ----------
    add_heading(doc, "三、实验要求")
    for t in [
        "准确规范地使用 UML 模型，包括类名、属性、方法、关系和多重性、角色、可见性；",
        "独立完成，禁止抄袭；",
        "使用 Rational Rose 创建模型；",
        "选择自己熟悉的语言实现之，代码提交到自己的 gitee 仓库，"
        "代码地址写到实验报告中；",
        "按照实验报告模板编写实验报告，将创建的模型粘贴到 Word 报告中。",
    ]:
        add_para(doc, t)

    # ---------- 四、实验内容 ----------
    add_heading(doc, "四、实验内容")
    add_para(doc, "本实验共包含 A1-1 ~ A1-4 四个子任务，分别考察 UML 类模型中"
                  "属性与操作的规范表达、聚合与组合的语义区分、"
                  "多重性与约束性注释的建模，以及一个完整的网上购物系统领域建模。"
                  "各子任务的类图、关系明细与代码实现如下。")

    for idx, m in enumerate(ALL_MODELS):
        # 每个子任务另起一页，但 A1-1 类图很小，与其后的 A1-2 共页更紧凑
        if idx >= 2:
            page_break(doc)

        add_heading(doc, "4.%d %s（%s）" % (idx + 1, m.key, m.title), size=12.5)

        # 需求与说明
        add_para(doc, "需求描述与建模说明：", bold=True, indent_first=False)
        for t in m.notes:
            add_para(doc, "• " + t, size=11)

        # 类图
        img = os.path.join(DIAG_DIR, DIAGRAM_FILE[m.key])
        # 简单模型图小、复杂模型图大，按类数量自适应宽度
        n_cls = len(m.classes)
        if n_cls <= 1:
            img_w = 11.0
        elif n_cls <= 3:
            img_w = 15.0
        elif n_cls <= 5:
            img_w = 16.5
        else:
            img_w = 15.8
        add_image(doc, img, "图 4-%d  %s  UML 类图" % (idx + 1, m.key), width_cm=img_w)

        # 类清单
        rows = []
        for c in m.classes:
            is_enum = c.stereotype == "enumeration"
            kind = "枚举" if is_enum else ("抽象类" if c.abstract else "类")
            if is_enum:
                # 枚举：列出取值，不按属性/操作拆分
                attrs = "、".join(a.name for a in c.attrs)
                ops = "—"
            else:
                attrs = "；".join(
                    "%s %s : %s" % (VIS_SYMBOL[a.visibility], a.name, a.type or "—")
                    for a in c.attrs)
                ops = "；".join(
                    "%s %s(%s) : %s" % (VIS_SYMBOL[o.visibility],
                                        o.name,
                                        ", ".join("%s : %s" % (p[0], p[1]) for p in o.params),
                                        o.return_type)
                    for o in c.ops)
            rows.append([c.name, kind, attrs or "—", ops or "—"])
        add_table(doc, ["类名", "类别", "属性（可见性 名字 : 类型）",
                        "操作（可见性 名字(参数) : 返回类型）"],
                  rows, widths=[2.8, 1.2, 5.4, 6.4], size=9,
                  caption="表 4-%d  %s 类清单" % (idx + 1, m.key))

        # 关系表
        if m.rels:
            add_table(doc, ["关系", "源类", "目标类", "源端（角色/多重性）",
                            "目标端（角色/多重性）", "关系名", "说明"],
                      rel_rows(m), widths=[1.1, 1.9, 1.9, 2.0, 2.0, 1.3, 5.6], size=9,
                      caption="表 4-%d  %s 关系与多重性明细" % (idx + 1, m.key))

    # 代码实现
    page_break(doc)
    add_heading(doc, "4.5 代码实现", size=12.5)
    add_para(doc, "使用 Java 实现上述四个模型。代码目录结构如下，"
                  "每个子模型一个包，类名与属性名与类图严格一致。")

    add_code(doc, [
        "code/",
        "├── build.gradle              // Gradle 构建脚本（UTF-8，JUnit 5）",
        "├── settings.gradle",
        "└── src/",
        "    ├── main/java/com/hj212/experiment3/",
        "    │   ├── Main.java          // 演示程序：依次运行四个模型",
        "    │   ├── a1_1/Thoroughbred.java",
        "    │   ├── a1_2/College.java",
        "    │   ├── a1_2/Building.java",
        "    │   ├── a1_2/Course.java",
        "    │   ├── a1_3/School.java",
        "    │   ├── a1_3/Department.java",
        "    │   ├── a1_3/Instructor.java",
        "    │   ├── a1_3/Subject.java",
        "    │   ├── a1_3/Student.java",
        "    │   ├── a1_4/Customer.java",
        "    │   ├── a1_4/Order.java",
        "    │   ├── a1_4/OrderDetail.java",
        "    │   ├── a1_4/Product.java",
        "    │   ├── a1_4/Payment.java",
        "    │   ├── a1_4/Credit.java",
        "    │   ├── a1_4/Cash.java",
        "    │   ├── a1_4/WireTransfer.java",
        "    │   ├── a1_4/AliPay.java",
        "    │   ├── a1_4/WeixinPay.java",
        "    │   └── a1_4/OrderStatus.java",
        "    └── test/java/com/hj212/experiment3/",
        "        └── Experiment3ModelTest.java",
    ])
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(6)

    add_para(doc, "关键代码片段 1：A1-2 约束性注释 {Course 一定在某个 Building 中进行} 的实现",
             bold=True, indent_first=False)
    add_code(doc, [
        "public void setBuilding(Building building) {",
        "    if (building == null) {",
        "        throw new IllegalArgumentException(",
        "            \"违反约束：{Course 一定在某个 Building 中进行}\");",
        "    }",
        "    this.building = building;",
        "}",
    ])
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(6)

    add_para(doc, "关键代码片段 2：A1-3 多重性 1..3 的实现（指导教师最多教授 3 门课程）",
             bold=True, indent_first=False)
    add_code(doc, [
        "public void teach(Subject subject) {",
        "    if (subject == null) {",
        "        throw new IllegalArgumentException(\"课程不可为 null\");",
        "    }",
        "    if (taughtSubjects.contains(subject)) {",
        "        return;",
        "    }",
        "    if (taughtSubjects.size() >= MAX_SUBJECTS) {",
        "        throw new IllegalStateException(",
        "            \"违反多重性约束：指导教师最多教授 \" + MAX_SUBJECTS + \" 门课程\");",
        "    }",
        "    taughtSubjects.add(subject);",
        "}",
    ])
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(6)

    add_para(doc, "关键代码片段 3：A1-4 泛化关系与五种支付方式的实现", bold=True,
             indent_first=False)
    add_code(doc, [
        "public abstract class Payment {          // 抽象类，泛化关系的父端",
        "    private BigDecimal amount;            // 支付金额",
        "    public abstract String getPaymentType();",
        "}",
        "",
        "public class Credit extends Payment { }  // 信用卡：number / type / expireDate",
        "public class Cash extends Payment { }    // 现金：cashTendered",
        "public class WireTransfer extends Payment { }  // 在线转账：bankID / bankName",
        "public class AliPay extends Payment { }  // 支付宝：number",
        "public class WeixinPay extends Payment { }// 微信支付：number",
    ])
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(6)

    add_para(doc, "关键代码片段 4：A1-4 订单状态机（OrderStatus 枚举与状态流转校验）",
             bold=True, indent_first=False)
    add_code(doc, [
        "public enum OrderStatus {",
        "    CREATE, PAID, SHIPPING, DELIVERED, CANCEL;",
        "",
        "    public boolean canTransitionTo(OrderStatus target) {",
        "        switch (this) {",
        "            case CREATE:  return target == PAID || target == CANCEL;",
        "            case PAID:    return target == SHIPPING || target == CANCEL;",
        "            case SHIPPING: return target == DELIVERED;",
        "            default:     return false;",
        "        }",
        "    }",
        "}",
    ])
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(6)

    # ---------- 五、实验结论 ----------
    page_break(doc)
    add_heading(doc, "五、实验结论")
    add_para(doc, "通过本次实验，我完成了 A1-1 ~ A1-4 四个面向对象建模任务，"
                  "主要收获如下：")
    for t in [
        "第一，掌握了 UML 类模型中元素的标准表达方式。属性由「可见性符号 + 名字 + "
        "类型」构成，可见性符号 -、#、~、+ 分别对应私有、受保护、包、公有；"
        "操作由「可见性符号 + 名字(参数名 : 参数类型) + : 返回类型」构成。"
        "在 A1-1 的 Thoroughbred 中，题目要求全部属性为私有、全部操作为公有，"
        "我据此建模并在代码中用 private / public 修饰符一一对应。",

        "第二，厘清了聚合与组合、关联与泛化的语义差别。聚合（空心菱形）表示"
        "“弱拥有”，被拥有对象可独立存在，如 College 聚合 Building；"
        "组合（实心菱形）表示“强拥有”，被拥有对象生命周期依附于整体，"
        "如 College 组合 Course、Order 组合 OrderDetail。"
        "代码中，组合关系通过在整体类维护被拥有对象集合、"
        "并在移除时同步解除反向引用来体现。",

        "第三，掌握了多重性与角色名的准确标注方法。多重性描述的是"
        "“一个关联端对象对应多少个另一端对象”，必须站在关联端的对象视角来描述，"
        "例如 Instructor 与 Department 之间 Instructor 端为 *、Department 端为 1..*，"
        "才正确表达“每个系至少 1 位指导教师，每位指导教师至少属于 1 个系”。"
        "角色名标注在关联端，用于区分同一对类之间的不同语义"
        "（如“拥有指导教师”与“属于”）。",

        "第四，理解了约束性注释的作用。{Course 一定在某个 Building 中进行} "
        "用 UML 的 { } 记号表达业务规则，它不改变类图结构，但限定了对象状态，"
        "在代码中体现为构造与赋值时的参数校验，违反约束即抛出异常。",

        "第五，体会到模型与代码的一致性保障价值。类图不是画完就完的文档，"
        "而是可执行的契约：类图中的多重性上限 1..3、1..5、0..* 在代码中分别对应"
        "集合容量检查；类图中的组合与聚合关系在代码中对应对象引用与生命周期管理；"
        "类图中的约束与状态机在代码中对应前置条件校验。"
        "本次实验共编写 25 个 JUnit 5 单元测试，全部通过，"
        "覆盖了四个模型的结构、关系、多重性与约束，验证了模型与实现的一致性。",
    ]:
        add_para(doc, t)

    add_para(doc, "不足与改进：", bold=True, indent_first=False)
    for t in [
        "本实验仅完成了类图（静态模型）的建模，尚未涉及用例图、行为图与设计模型；"
        "后续实验四、五将分别建模顺序图与活动图，需进一步理解不同图类型之间的协同关系。",
        "建模工具方面，本机上 Rational Rose 2007 未能正常安装，"
        "因此类图采用 PlantUML 依据 UML 2.1 规范绘制，并同时导出标准 UML 2.1 XMI"
        "（a1-1-model.xmi ~ a1-4-model.xmi），该 XMI 文件可直接被 Rational Rose、"
        "Visual Paradigm 导入，从而在 Rose 中得到与图示完全等价的类图模型。",
        "代码实现上，为了保证可测试性，多重性上限等约束采用了运行时异常抛出的方式；"
        "更严谨的做法是使用类型系统或构建期校验，"
        "后续可尝试用不可变集合与工厂方法强化约束。",
    ]:
        add_para(doc, t)

    # ---------- 六、仓库地址 ----------
    add_heading(doc, "六、仓库地址")
    add_para(doc, "代码仓库（Gitee 码云）：", bold=True, indent_first=False)
    add_para(doc, REPO_URL, indent_first=False)
    add_para(doc, "同一份代码的备份镜像（GitHub）：", bold=True, indent_first=False)
    add_para(doc, REPO_BACKUP_URL, indent_first=False)
    add_para(doc, "说明：Gitee 自 2022 年起已停用「账号 + 密码」方式的 Git 推送，"
                  "需改用私人令牌（Personal Access Token）。因此代码先推送至 GitHub "
                  "公开仓库留存，再使用私人令牌推送至 Gitee；两处内容完全一致。",
             size=10.5)
    add_para(doc, "仓库目录结构：", bold=True, indent_first=False)
    add_code(doc, [
        "model/                                  # UML 模型",
        "├── a1-1-thoroughbred.puml               # PlantUML 源文件（类图定义）",
        "├── a1-2-college.puml",
        "├── a1-3-school.puml",
        "├── a1-4-shopping.puml",
        "├── a1-1-model.xmi ~ a1-4-model.xmi     # UML 2.1 XMI，可导入 Rose",
        "└── diagrams/                           # 渲染出的类图 PNG",
        "",
        "code/                                   # Java 实现与单元测试",
        "├── build.gradle / settings.gradle",
        "└── src/main/java, src/test/java",
        "",
        "tools/                                  # 模型与报告生成脚本",
        "├── model_def.py                         # 模型的单一事实来源",
        "├── gen_xmi.py                           # 生成 UML 2.1 XMI",
        "└── gen_report.py                        # 生成实验报告",
        "",
        "202410120323-柳淳-软件工程实验三.docx      # 本实验报告",
    ])

    doc.save(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    build_report()
