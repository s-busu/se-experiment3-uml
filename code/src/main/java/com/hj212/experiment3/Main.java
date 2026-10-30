package com.hj212.experiment3;

import com.hj212.experiment3.a1_1.Thoroughbred;
import com.hj212.experiment3.a1_2.Building;
import com.hj212.experiment3.a1_2.College;
import com.hj212.experiment3.a1_2.Course;
import com.hj212.experiment3.a1_3.Department;
import com.hj212.experiment3.a1_3.Instructor;
import com.hj212.experiment3.a1_3.School;
import com.hj212.experiment3.a1_3.Student;
import com.hj212.experiment3.a1_3.Subject;
import com.hj212.experiment3.a1_4.AliPay;
import com.hj212.experiment3.a1_4.Cash;
import com.hj212.experiment3.a1_4.Credit;
import com.hj212.experiment3.a1_4.Customer;
import com.hj212.experiment3.a1_4.Order;
import com.hj212.experiment3.a1_4.OrderDetail;
import com.hj212.experiment3.a1_4.OrderStatus;
import com.hj212.experiment3.a1_4.Payment;
import com.hj212.experiment3.a1_4.Product;
import com.hj212.experiment3.a1_4.WeixinPay;
import com.hj212.experiment3.a1_4.WireTransfer;

import java.math.BigDecimal;
import java.time.Year;
import java.util.Calendar;
import java.util.Date;

/**
 * 实验三 面向对象系统建模 —— 演示程序。
 *
 * <p>依次演示 A1-1 ~ A1-4 四个模型的运行效果，
 * 验证类图所定义的结构、关系、多重性与约束在代码中均得到落实。
 */
public final class Main {

    private Main() {
    }

    public static void main(String[] args) {
        System.out.println("========== 软件工程实验三：面向对象的系统建模 A ==========");

        demoA11();
        demoA12();
        demoA13();
        demoA14();

        System.out.println("========== 全部演示结束 ==========");
    }

    /** A1-1 Thoroughbred 模型演示。 */
    private static void demoA11() {
        System.out.println();
        System.out.println("---------- A1-1 Thoroughbred（优良品质的马）----------");
        Thoroughbred stallion = new Thoroughbred(null, null, Year.now().getValue() - 6);
        Thoroughbred mare = new Thoroughbred(null, null, Year.now().getValue() - 8);
        stallion.setMother(mare);
        stallion.setFather(new Thoroughbred(null, null, Year.now().getValue() - 10));

        System.out.println("公马出生年份 : " + stallion.getBirthyear());
        System.out.println("公马当前年龄 : " + stallion.getCurrentAge() + " 岁");
        System.out.println("公马母马     : " + stallion.getMother());
        System.out.println("公马父马     : " + stallion.getFather());
    }

    /** A1-2 College 聚合 / 组合模型演示。 */
    private static void demoA12() {
        System.out.println();
        System.out.println("---------- A1-2 College（聚合 / 组合 / 约束）----------");
        College college = new College("河海大学");
        Building building = new Building("致用楼", "西康路 1 号");

        college.addBuilding(building);
        Course course = new Course("面向对象分析与设计", building);
        college.addCourse(course);

        System.out.println("学院       : " + college.getName());
        System.out.println("聚合的建筑 : " + college.getBuildings().get(0).getName());
        System.out.println("组合的课程 : " + college.getCourses().get(0).getName());
        System.out.println("课程所在建筑（约束 {Course 一定在某个 Building 中进行}）: "
                + course.getBuilding().getName());

        try {
            new Course("非法课程", null);
        } catch (IllegalArgumentException e) {
            System.out.println("约束校验生效 : " + e.getMessage());
        }
    }

    /** A1-3 School 领域模型演示。 */
    private static void demoA13() {
        System.out.println();
        System.out.println("---------- A1-3 School（学院 / 系 / 教师 / 课程 / 学生）----------");
        School school = new School("计算机与信息学院");
        Department cs = new Department("软件工程系");
        Department se = new Department("信息工程系");
        school.addDepartment(cs);
        school.addDepartment(se);

        Instructor instructor = new Instructor("张老师", "T1001");
        cs.addInstructor(instructor);
        se.addInstructor(instructor);

        Subject oop = new Subject("面向对象分析与设计", 3);
        Subject seCourse = new Subject("软件工程", 3);
        cs.addSubject(oop);
        se.addSubject(seCourse);
        instructor.teach(oop);
        instructor.teach(seCourse);

        Student student = new Student("柳淳", "202410120323");
        school.addStudent(student);
        student.attend(oop);
        student.attend(seCourse);

        System.out.println("学院       : " + school.getName()
                + "，系 " + school.getDepartments().size() + " 个，学生 "
                + school.getStudents().size() + " 名");
        System.out.println("软件工程系 : 指导教师 " + cs.getInstructors().size()
                + " 位，课程 " + cs.getSubjects().size() + " 门");
        System.out.println("张老师所属系: " + instructor.getDepartments().size()
                + " 个，教授课程 " + instructor.getTaughtSubjects().size() + " 门");
        System.out.println("柳淳参加课程: " + student.getSubjects().size() + " 门");

        try {
            instructor.teach(new Subject("第 4 门课程", 2));
        } catch (IllegalStateException e) {
            System.out.println("多重性校验生效 : " + e.getMessage());
        }
    }

    /** A1-4 网上购物系统模型演示。 */
    private static void demoA14() {
        System.out.println();
        System.out.println("---------- A1-4 网上购物系统（类之间关系含多重性）----------");
        Customer customer = new Customer("柳淳", "13800000000", "南京市西康路 1 号", true);

        Product book = new Product("《软件工程》", 0.75D, "教材", new BigDecimal("59.00"));
        Product laptop = new Product("笔记本电脑", 2.50D, "办公设备", new BigDecimal("6800.00"));

        Order order = new Order(customer);
        order.addDetail(new OrderDetail(book, 2));
        order.addDetail(new OrderDetail(laptop, 1));
        customer.placeOrder(order);

        System.out.println("客户       : " + customer.getName()
                + "，激活=" + customer.isActive() + "，订单 " + customer.getOrders().size() + " 个");
        System.out.println("订单状态   : " + order.getStatus());
        System.out.println("订单明细   : " + order.getDetails().size() + " 条");
        System.out.println("小计/重量  : " + order.getDetails().get(0).calculateSubTotal()
                + " / " + order.getDetails().get(0).calculateWeight());
        System.out.println("订单总额   : " + order.calculateTotal()
                + "，总重量 " + order.calculateTotalWeight());

        Credit credit = new Credit("6222021234567890", "VISA", new Date(),
                order.calculateTotal());
        order.pay(credit);
        System.out.println("支付后状态 : " + order.getStatus()
                + "，支付方式=" + order.getPayment().getPaymentType()
                + "，金额=" + order.getPayment().getAmount());
        order.ship();
        order.deliver();
        System.out.println("发货送达后 : " + order.getStatus());

        demonstratePaymentKinds();
        demonstrateInactiveCustomer();
    }

    /** 演示五种具体支付方式。 */
    private static void demonstratePaymentKinds() {
        System.out.println("  五种支付方式 :");
        Payment[] payments = new Payment[] {
                new Credit("6222021234567890", "VISA", new Date(), new BigDecimal("59.00")),
                new Cash(new BigDecimal("100.00"), new BigDecimal("59.00")),
                new WireTransfer("10230001", "中国工商银行", new BigDecimal("59.00")),
                new AliPay("liuchun@alipay.com", new BigDecimal("59.00")),
                new WeixinPay("wx_202410120323", new BigDecimal("59.00"))
        };
        for (Payment payment : payments) {
            String extra = "";
            if (payment instanceof Cash) {
                extra = "，交付现金 " + ((Cash) payment).getCashTendered()
                        + "，找零 " + ((Cash) payment).getChange();
            } else if (payment instanceof Credit) {
                extra = "，卡号 " + ((Credit) payment).getNumber()
                        + "，类型 " + ((Credit) payment).getType();
            } else if (payment instanceof WireTransfer) {
                extra = "，银行 " + ((WireTransfer) payment).getBankName()
                        + "(" + ((WireTransfer) payment).getBankID() + ")";
            } else if (payment instanceof AliPay) {
                extra = "，卡号 " + ((AliPay) payment).getNumber();
            } else if (payment instanceof WeixinPay) {
                extra = "，卡号 " + ((WeixinPay) payment).getNumber();
            }
            System.out.println("    - " + payment.getPaymentType()
                    + "，金额 " + payment.getAmount() + extra);
        }
    }

    /** 演示未激活客户不能下单，以及订单状态机约束。 */
    private static void demonstrateInactiveCustomer() {
        Customer inactive = new Customer("张三", "13900000000", "某地", false);
        try {
            inactive.placeOrder(new Order(inactive));
        } catch (IllegalStateException e) {
            System.out.println("  激活状态校验生效 : " + e.getMessage());
        }

        Order order = new Order(inactive);
        order.addDetail(new OrderDetail(
                new Product("笔", 0.05D, "文具", new BigDecimal("5.00")), 1));
        try {
            order.ship();
        } catch (IllegalStateException e) {
            System.out.println("  状态机校验生效   : " + e.getMessage());
        }
        order.pay(new Cash(new BigDecimal("10.00"), order.calculateTotal()));
        order.ship();
        System.out.println("  合法状态流转     : CREATE -> PAID -> SHIPPING -> DELIVERED 可行，"
                + "枚举定义 " + OrderStatus.values().length + " 种状态");
    }
}
