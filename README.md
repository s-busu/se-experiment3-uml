# 软件工程实验三：面向对象的系统建模 A

> 课程：软件工程　　学号：202410120323　　姓名：柳淳

本仓库为「软件工程实验三：面向对象的系统建模 A」的完整实现，包含 A1-1 ~ A1-4
四个子任务的 **UML 类图模型**、**Java 代码实现** 与 **单元测试**。

---

## 一、实验内容与产物对照

| 子任务 | 内容 | 模型文件 | 类图 | 代码包 |
|---|---|---|---|---|
| A1-1 | Thoroughbred（优良品质的马）属性与操作的规范表达 | `model/a1-1-thoroughbred.puml`、`model/a1-1-model.xmi` | `model/diagrams/A1_1_Thoroughbred.png` | `code/src/main/java/com/hj212/experiment3/a1_1/` |
| A1-2 | College / Building / Course 的聚合、组合与约束性注释 | `model/a1-2-college.puml`、`model/a1-2-model.xmi` | `model/diagrams/A1_2_College.png` | `code/src/main/java/com/hj212/experiment3/a1_2/` |
| A1-3 | School / Department / Instructor / Subject / Student 领域模型 | `model/a1-3-school.puml`、`model/a1-3-model.xmi` | `model/diagrams/A1_3_School.png` | `code/src/main/java/com/hj212/experiment3/a1_3/` |
| A1-4 | 简化网上购物系统类模型（类之间关系含多重性） | `model/a1-4-shopping.puml`、`model/a1-4-model.xmi` | `model/diagrams/A1_4_Shopping.png` | `code/src/main/java/com/hj212/experiment3/a1_4/` |

---

## 二、目录结构

```
.
├── model/                                  # UML 模型
│   ├── a1-1-thoroughbred.puml               # PlantUML 源文件（类图定义）
│   ├── a1-2-college.puml
│   ├── a1-3-school.puml
│   ├── a1-4-shopping.puml
│   ├── a1-1-model.xmi ~ a1-4-model.xmi     # UML 2.1 XMI，可导入 Rose / Visual Paradigm
│   └── diagrams/                           # 渲染出的类图 PNG
│
├── code/                                   # Java 实现与单元测试
│   ├── build.gradle                        # Gradle 构建脚本（UTF-8 编码，JUnit 5）
│   ├── settings.gradle
│   └── src/
│       ├── main/java/com/hj212/experiment3/
│       │   ├── Main.java                   # 演示程序：依次运行四个模型
│       │   ├── a1_1/Thoroughbred.java
│       │   ├── a1_2/College.java, Building.java, Course.java
│       │   ├── a1_3/School.java, Department.java, Instructor.java,
│       │   │       Subject.java, Student.java
│       │   └── a1_4/Customer.java, Order.java, OrderDetail.java, Product.java,
│       │           Payment.java, Credit.java, Cash.java, WireTransfer.java,
│       │           AliPay.java, WeixinPay.java, OrderStatus.java
│       └── test/java/com/hj212/experiment3/Experiment3ModelTest.java
│
├── tools/                                  # 模型与报告生成脚本
│   ├── model_def.py                        # 模型的单一事实来源（类/属性/操作/关系/多重性）
│   ├── gen_xmi.py                          # 由模型定义生成 UML 2.1 XMI
│   ├── gen_report.py                       # 生成实验报告 docx
│   └── pdf_preview.py                      # 报告 PDF 分页渲染（目检用）
│
└── 202410120323-柳淳-软件工程实验三.docx      # 实验报告
```

---

## 三、建模说明

### UML 元素规范

* **属性**：`可见性符号 名字 : 类型`，可见性符号 `-` 私有、`#` 受保护、
  `~` 包、`+` 公有。
* **操作**：`可见性符号 名字(参数名 : 参数类型) : 返回类型`。
* **关系**：区分关联、聚合（空心菱形）、组合（实心菱形）与泛化（实线空心三角）。
* **多重性**：标注在关联端，表示「一个本端对象对应多少个另一端对象」，
  取值如 `1`、`0..*`、`1..*`、`1..3`、`1..5`。
* **角色名**：标注在关联端，用于区分同一对类之间的不同语义
  （如 A1-3 中 Department 与 Instructor 之间的「拥有指导教师」与「属于」）。
* **约束性注释**：用 UML 的 `{ }` 记号标注在关联上，如
  `{Course 一定在某个 Building 中进行}`。

### 四个子模型的要点

**A1-1 Thoroughbred**
三个属性 `mother`、`father`、`birthyear` 全部为私有可见性；
三个操作 `getCurrentAge()`、`getFather()`、`getMother()` 全部为公有可见性并标注返回类型。
`mother` / `father` 的类型同为 Thoroughbred，构成自关联。

**A1-2 College**
`College` 聚合 `Building`（空心菱形，建筑可独立存在）；
`College` 组合 `Course`（实心菱形，课程生命周期依附于学院）；
`Course` 关联 `Building`，并带约束 `{Course 一定在某个 Building 中进行}`，
即 Building 端多重性为 `1`、Course 端为 `*`。

**A1-3 School**

| 关系 | 多重性 | 含义 |
|---|---|---|
| School → Department | 1 / 1..* | 学院由 1 到多个系构成（组合） |
| Department → Instructor | 1 / 1..* | 每个系至少拥有 1 位指导教师 |
| Instructor → Department | * / 1..* | 每位指导教师至少属于某个系 |
| Department → Subject | 1 / 1..* | 每个系至少提供 1 门课程 |
| Instructor → Subject | 1 / 1..3 | 每位指导教师教授 1-3 门课程 |
| School → Student | 1 / 0..* | 学院拥有 0 到多名学生 |
| Student → Subject | 1 / 1..5 | 每名学生参加 1-5 门课程学习 |

需求中「系提供的课程 Subject」与「学生参加的课程」指向同一实体，即 `Subject`。

**A1-4 网上购物系统**

`Payment` 为抽象类，`Credit`、`Cash`、`WireTransfer`、`AliPay`、`WeixinPay`
通过泛化继承，各自带有题目要求的属性。
`OrderStatus` 为枚举，取值 `CREATE / PAID / SHIPPING / DELIVERED / CANCEL`。

| 关系 | 源端（角色/多重性） | 目标端（角色/多重性） | 说明 |
|---|---|---|---|
| 关联 | 客户 / 1 | 订单 / 0..* | 一个客户下 0 到多个订单 |
| 组合 | 订单 / 1 | 订单明细 / 1..* | 订单包含 1 到多条明细 |
| 关联 | 订单明细 / 0..* | 商品项 / 1 | 每条明细对应一个商品项 |
| 关联 | 订单 / 1 | 支付方式 / 0..1 | 一个订单最多一种支付方式 |

`Product` 额外引入 `unitPrice` 属性，以支持 `getPriceForQuantity(qty)` 的计算。

---

## 四、模型与代码的一致性

类图不是画完就完的文档，而是可执行的契约。类图中的结构在代码中一一落实：

| 类图中的约束 | 代码中的落实方式 |
|---|---|
| 多重性上限 `1..3`（指导教师教授课程） | `Instructor.teach()` 检查集合规模，超限抛 `IllegalStateException` |
| 多重性上限 `1..5`（学生参加课程） | `Student.attend()` 检查集合规模 |
| 约束 `{Course 一定在某个 Building 中进行}` | `Course.setBuilding()` 拒绝 null，抛 `IllegalArgumentException` |
| 组合关系（订单包含明细） | `Order` 维护明细集合，`addDetail()` 保证不重复 |
| 聚合关系（学院拥有建筑） | `College.addBuilding()` 仅登记引用，不转移所有权 |
| 泛化关系（五种支付方式） | `Payment` 抽象类 + 五个子类 `extends Payment` |
| `OrderStatus` 枚举与状态流转 | `OrderStatus.canTransitionTo()` 定义合法流转，`Order` 各操作前置校验 |

---

## 五、运行方式

### 环境

* JDK 1.8.0_131（`JAVA_HOME` 指向 `C:\Program Files\Java\jdk1.8.0_131`）
* Gradle 7.6.4
* JUnit 5.8.2

### 构建与测试

```bash
cd code
gradle test          # 运行单元测试
gradle run           # 运行演示程序，输出四个模型的运行效果
```

### 重新生成 UML 类图

需要 PlantUML（`plantuml.jar`）与 Graphviz：

```bash
java -jar tools/plantuml.jar -charset UTF-8 -DPLANTUML_LIMIT_SIZE=8192 \
     -tpng -o model/diagrams model/*.puml
```

### 重新生成 UML 2.1 XMI

```bash
python tools/gen_xmi.py
```

生成的 `model/a1-*-model.xmi` 符合 UML 2.1 XMI 结构，
可直接用 **Rational Rose 2007**、**Visual Paradigm**、**Enterprise Architect**
导入，从而在 Rose 中得到与 PNG 图示完全等价的类图模型。

### 重新生成实验报告

```bash
python tools/gen_report.py
```

---

## 六、测试结果

`Experiment3ModelTest` 共 25 个用例，覆盖四个模型的结构、关系、多重性与约束：

```
BUILD SUCCESSFUL
25 tests completed, 0 failed
```
