# -*- coding: utf-8 -*-
"""
实验三 UML 模型的单一事实来源（Single Source of Truth）。

四个子模型（A1-1 ~ A1-4）的类、属性、操作、关系、多重性、角色名
在此集中定义，供以下三者共同使用，保证完全一致：
  1) model/*.puml         —— PlantUML 渲染源（图形）
  2) model/*.xmi          —— UML 2.1 XMI（可导入 Rational Rose / Visual Paradigm）
  3) 报告中的关系表与说明文字
"""

# 可见性
PUB = "public"
PROT = "protected"
PACK = "package"
PRIV = "private"

# 可见性符号（UML 记号）与中文描述
VIS_MAP = {"public": "public", "private": "private",
           "protected": "protected", "package": "package"}
VIS_SYMBOL = {"public": "+", "private": "-", "protected": "#", "package": "~"}
VIS_CN = {"public": "公有", "private": "私有",
          "protected": "受保护", "package": "包"}

# 关系类型
ASSOC = "association"
AGG = "aggregation"
COMP = "composition"
GEN = "generalization"


class Attr:
    def __init__(self, name, type_, visibility=PRIV, multiplicity=None, note=None):
        self.name = name
        self.type = type_
        self.visibility = visibility
        self.multiplicity = multiplicity
        self.note = note


class Op:
    def __init__(self, name, return_type="void", visibility=PUB, params=None, note=None):
        self.name = name
        self.return_type = return_type
        self.visibility = visibility
        # params: list of (name, type, visibility)
        self.params = params or []
        self.note = note


class Cls:
    def __init__(self, name, attrs=None, ops=None, abstract=False, stereotype=None, note=None):
        self.name = name
        self.attrs = attrs or []
        self.ops = ops or []
        self.abstract = abstract
        self.stereotype = stereotype
        self.note = note


class Rel:
    def __init__(self, kind, source, target, source_role=None, source_mult=None,
                 target_role=None, target_mult=None, name=None, note=None,
                 generalization_of=None):
        self.kind = kind
        self.source = source
        self.target = target
        self.source_role = source_role
        self.source_mult = source_mult
        self.target_role = target_role
        self.target_mult = target_mult
        self.name = name
        self.note = note
        # 泛化：generalization_of 表示 child extends parent
        self.generalization_of = generalization_of


class Model:
    def __init__(self, key, title, classes, rels, notes=None):
        self.key = key
        self.title = title
        self.classes = classes
        self.rels = rels
        self.notes = notes or []


# ============================== A1-1 Thoroughbred ==============================

A1_1 = Model(
    key="A1-1",
    title="Thoroughbred 类模型",
    classes=[
        Cls("Thoroughbred", attrs=[
            Attr("mother", "Thoroughbred", PRIV),
            Attr("father", "Thoroughbred", PRIV),
            Attr("birthyear", "Integer", PRIV),
        ], ops=[
            Op("getCurrentAge", "Integer", PUB),
            Op("getFather", "Thoroughbred", PUB),
            Op("getMother", "Thoroughbred", PUB),
        ], note="母马与父马同为 Thoroughbred，构成自关联（递归关联）。"),
    ],
    rels=[],
    notes=[
        "三个属性均为私有可见性 (-)；类型置于名字之后并以冒号分隔。",
        "三个操作均为公有可见性 (+)，无参，标注返回类型。",
    ],
)

# ============================== A1-2 College ==============================

A1_2 = Model(
    key="A1-2",
    title="College 聚合 / 组合模型",
    classes=[
        Cls("College", attrs=[
            Attr("name", "String", PRIV),
        ], ops=[
            Op("addBuilding", "void", PUB, [("b", "Building", PUB)]),
            Op("addCourse", "void", PUB, [("c", "Course", PUB)]),
            Op("getBuildings", "Building[]", PUB),
            Op("getCourses", "Course[]", PUB),
        ]),
        Cls("Building", attrs=[
            Attr("name", "String", PRIV),
            Attr("address", "String", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getAddress", "String", PUB),
        ]),
        Cls("Course", attrs=[
            Attr("name", "String", PRIV),
            Attr("building", "Building", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getBuilding", "Building", PUB),
        ]),
    ],
    rels=[
        Rel(AGG, "College", "Building",
            source_role="学院", source_mult="1",
            target_role="建筑", target_mult="0..*",
            name="包含",
            note="空心菱形：建筑构成学院，建筑可脱离学院独立存在。"),
        Rel(COMP, "College", "Course",
            source_role="学院", source_mult="1",
            target_role="课程", target_mult="1..*",
            name="开设",
            note="实心菱形：课程是学院不可分割的组成部分，生命周期依附于学院。"),
        Rel(ASSOC, "Course", "Building",
            source_role="课程", source_mult="*",
            target_role="建筑", target_mult="1",
            name="开设于",
            note="约束性注释：{Course 一定在某个 Building 中进行}。"
                 "Building 端多重性为 1，Course 端为 *。"),
    ],
    notes=[
        "聚合（空心菱形 o--）与组合（实心菱形 *--）的区别体现为被拥有对象能否独立存在。",
        "约束性注释 {Course 一定在某个 Building 中进行} 用 UML 的 { } 约束记号标注在关联上。",
    ],
)

# ============================== A1-3 School ==============================

A1_3 = Model(
    key="A1-3",
    title="学校领域模型（School / Department / Instructor / Subject / Student）",
    classes=[
        Cls("School", attrs=[
            Attr("name", "String", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getDepartments", "Department[]", PUB),
            Op("getStudents", "Student[]", PUB),
            Op("addDepartment", "void", PUB, [("d", "Department", PUB)]),
            Op("addStudent", "void", PUB, [("s", "Student", PUB)]),
        ]),
        Cls("Department", attrs=[
            Attr("name", "String", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getInstructors", "Instructor[]", PUB),
            Op("getSubjects", "Subject[]", PUB),
            Op("addInstructor", "void", PUB, [("i", "Instructor", PUB)]),
            Op("addSubject", "void", PUB, [("s", "Subject", PUB)]),
        ]),
        Cls("Instructor", attrs=[
            Attr("name", "String", PRIV),
            Attr("employeeNo", "String", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getDepartments", "Department[]", PUB),
            Op("getTaughtSubjects", "Subject[]", PUB),
            Op("teach", "void", PUB, [("s", "Subject", PUB)]),
        ]),
        Cls("Subject", attrs=[
            Attr("name", "String", PRIV),
            Attr("credit", "Integer", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getCredit", "Integer", PUB),
            Op("getDepartment", "Department", PUB),
        ]),
        Cls("Student", attrs=[
            Attr("name", "String", PRIV),
            Attr("studentNo", "String", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getSubjects", "Subject[]", PUB),
            Op("attend", "void", PUB, [("s", "Subject", PUB)]),
        ]),
    ],
    rels=[
        Rel(COMP, "School", "Department",
            source_role="学院", source_mult="1",
            target_role="系", target_mult="1..*",
            name="设有",
            note="实心菱形：一个学院由 1 到多个系构成。"),
        Rel(AGG, "Department", "Instructor",
            source_role="系", source_mult="1",
            target_role="指导教师", target_mult="1..*",
            name="拥有指导教师",
            note="空心菱形：每个系至少拥有 1 位指导教师。"),
        Rel(ASSOC, "Instructor", "Department",
            source_role="指导教师", source_mult="*",
            target_role="系", target_mult="1..*",
            name="属于",
            note="每个指导教师至少属于某个系，故 Instructor 端多重性为 *。"),
        Rel(AGG, "Department", "Subject",
            source_role="系", source_mult="1",
            target_role="课程", target_mult="1..*",
            name="提供课程",
            note="每个系至少提供 1 门课程。"),
        Rel(ASSOC, "Instructor", "Subject",
            source_role="指导教师", source_mult="1",
            target_role="课程", target_mult="1..3",
            name="教授",
            note="每位指导教师教授 1-3 门课程。"),
        Rel(AGG, "School", "Student",
            source_role="学院", source_mult="1",
            target_role="学生", target_mult="0..*",
            name="拥有学生",
            note="学院拥有 0 到多名学生。"),
        Rel(ASSOC, "Student", "Subject",
            source_role="学生", source_mult="1",
            target_role="课程", target_mult="1..5",
            name="参加学习",
            note="每名学生参加 1-5 门课程学习。"),
    ],
    notes=[
        "题目中“系提供的课程 Subject”与“学生参加的课程”指向同一实体，即 Subject。",
        "多重性 1..* / 1..3 / 1..5 / 0..* 直接约束了代码中的集合规模上限。",
    ],
)

# ============================== A1-4 网上购物系统 ==============================

A1_4 = Model(
    key="A1-4",
    title="网上购物系统类模型（类之间关系含多重性）",
    classes=[
        Cls("Customer", attrs=[
            Attr("name", "String", PRIV),
            Attr("contact", "String", PRIV),
            Attr("deliveryAddress", "String", PRIV),
            Attr("active", "Boolean", PRIV),
        ], ops=[
            Op("getName", "String", PUB),
            Op("getContact", "String", PUB),
            Op("getDeliveryAddress", "String", PUB),
            Op("isActive", "Boolean", PUB),
            Op("placeOrder", "void", PUB, [("o", "Order", PUB)]),
            Op("getOrders", "Order[]", PUB),
        ]),
        Cls("Order", attrs=[
            Attr("createDate", "Date", PRIV),
            Attr("status", "OrderStatus", PRIV),
        ], ops=[
            Op("getCreateDate", "Date", PUB),
            Op("getStatus", "OrderStatus", PUB),
            Op("addDetail", "void", PUB, [("d", "OrderDetail", PUB)]),
            Op("getDetails", "OrderDetail[]", PUB),
            Op("getPayment", "Payment", PUB),
            Op("pay", "void", PUB, [("p", "Payment", PUB)]),
            Op("ship", "void", PUB),
            Op("deliver", "void", PUB),
            Op("cancel", "void", PUB),
        ]),
        Cls("OrderDetail", attrs=[
            Attr("quantity", "Integer", PRIV),
        ], ops=[
            Op("getQuantity", "Integer", PUB),
            Op("calculateSubTotal", "BigDecimal", PUB),
            Op("calculateWeight", "Double", PUB),
        ]),
        Cls("Product", attrs=[
            Attr("title", "String", PRIV),
            Attr("weight", "Double", PRIV),
            Attr("description", "String", PRIV),
            Attr("unitPrice", "BigDecimal", PRIV),
        ], ops=[
            Op("getTitle", "String", PUB),
            Op("getWeight", "Double", PUB),
            Op("getDescription", "String", PUB),
            Op("getUnitPrice", "BigDecimal", PUB),
            Op("getPriceForQuantity", "BigDecimal", PUB, [("qty", "Integer", PUB)]),
        ]),
        Cls("Payment", attrs=[
            Attr("amount", "BigDecimal", PRIV),
        ], ops=[
            Op("getAmount", "BigDecimal", PUB),
            Op("setAmount", "void", PUB, [("a", "BigDecimal", PUB)]),
        ], abstract=True, note="抽象支付方式，amount 为支付金额。"),
        Cls("Credit", attrs=[
            Attr("number", "String", PRIV),
            Attr("type", "String", PRIV),
            Attr("expireDate", "Date", PRIV),
        ], ops=[
            Op("getNumber", "String", PUB),
            Op("getType", "String", PUB),
            Op("getExpireDate", "Date", PUB),
        ]),
        Cls("Cash", attrs=[
            Attr("cashTendered", "BigDecimal", PRIV),
        ], ops=[
            Op("getCashTendered", "BigDecimal", PUB),
        ]),
        Cls("WireTransfer", attrs=[
            Attr("bankID", "String", PRIV),
            Attr("bankName", "String", PRIV),
        ], ops=[
            Op("getBankID", "String", PUB),
            Op("getBankName", "String", PUB),
        ]),
        Cls("AliPay", attrs=[
            Attr("number", "String", PRIV),
        ], ops=[
            Op("getNumber", "String", PUB),
        ]),
        Cls("WeixinPay", attrs=[
            Attr("number", "String", PRIV),
        ], ops=[
            Op("getNumber", "String", PUB),
        ]),
        Cls("OrderStatus", stereotype="enumeration", note=(
            "订单状态枚举，包含 CREATE、PAID、SHIPPING、DELIVERED、CANCEL 五种状态。"), attrs=[
            Attr("CREATE", None, PUB),
            Attr("PAID", None, PUB),
            Attr("SHIPPING", None, PUB),
            Attr("DELIVERED", None, PUB),
            Attr("CANCEL", None, PUB),
        ]),
    ],
    rels=[
        Rel(ASSOC, "Customer", "Order",
            source_role="客户", source_mult="1",
            target_role="订单", target_mult="0..*",
            name="下单",
            note="一个客户可以下 0 到多个订单，每个订单属于且仅属于一个客户。"),
        Rel(COMP, "Order", "OrderDetail",
            source_role="订单", source_mult="1",
            target_role="订单明细", target_mult="1..*",
            name="包含明细",
            note="实心菱形：订单包含 1 到多条订单明细，明细生命周期依附于订单。"),
        Rel(ASSOC, "OrderDetail", "Product",
            source_role="订单明细", source_mult="0..*",
            target_role="商品项", target_mult="1",
            name="对应商品",
            note="每条订单明细对应且仅对应一个商品项；同一商品可出现在多条明细中。"),
        Rel(ASSOC, "Order", "Payment",
            source_role="订单", source_mult="1",
            target_role="支付方式", target_mult="0..1",
            name="采用支付",
            note="一个订单最多对应一种支付方式；支付前 payment 为空。"),
        Rel(GEN, "Credit", "Payment", generalization_of="Payment"),
        Rel(GEN, "Cash", "Payment", generalization_of="Payment"),
        Rel(GEN, "WireTransfer", "Payment", generalization_of="Payment"),
        Rel(GEN, "AliPay", "Payment", generalization_of="Payment"),
        Rel(GEN, "WeixinPay", "Payment", generalization_of="Payment"),
    ],
    notes=[
        "Payment 为抽象类，五种具体支付方式 Credit / Cash / WireTransfer / AliPay / WeixinPay 通过泛化继承。",
        "OrderStatus 为枚举类，order 的 status 属性取值为 CREATE / PAID / SHIPPING / DELIVERED / CANCEL。",
        "Product 的 unitPrice 属性为实现 getPriceForQuantity() 所需的补充属性。",
    ],
)

ALL_MODELS = [A1_1, A1_2, A1_3, A1_4]
