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
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.time.Year;
import java.util.Calendar;
import java.util.Date;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * 实验三 面向对象系统建模 —— 单元测试。
 *
 * <p>覆盖四个模型的关键结构、关系、多重性与约束。
 */
class Experiment3ModelTest {

    // ==================== A1-1 Thoroughbred ====================

    @Test
    void thoroughbredShouldExposePrivatesAndPublicOperations() {
        Thoroughbred horse = new Thoroughbred(null, null, Year.now().getValue() - 5);
        assertEquals(5, horse.getCurrentAge());
        assertNull(horse.getFather());
        assertNull(horse.getMother());
    }

    @Test
    void thoroughbredShouldSupportSelfAssociation() {
        Thoroughbred father = new Thoroughbred(null, null, 2010);
        Thoroughbred mother = new Thoroughbred(null, null, 2012);
        Thoroughbred child = new Thoroughbred(mother, father, 2020);

        assertSame(mother, child.getMother());
        assertSame(father, child.getFather());
    }

    // ==================== A1-2 College ====================

    @Test
    void collegeShouldAggregateBuildingsAndComposeCourses() {
        College college = new College("河海大学");
        Building building = new Building("致用楼", "西康路 1 号");
        college.addBuilding(building);
        college.addCourse(new Course("面向对象", building));

        assertEquals(1, college.getBuildings().size());
        assertEquals(1, college.getCourses().size());
        assertSame(building, college.getBuildings().get(0));
    }

    @Test
    void courseMustAlwaysBeInSomeBuilding() {
        assertThrows(IllegalArgumentException.class, () -> new Course("非法课程", null));
    }

    @Test
    void removingCourseShouldClearCompositionLink() {
        College college = new College("河海大学");
        Course course = new Course("面向对象", new Building("致用楼", "西康路 1 号"));
        college.addCourse(course);
        assertSame(college, course.getCollege());

        college.removeCourse(course);
        assertNull(course.getCollege());
        assertTrue(college.getCourses().isEmpty());
    }

    // ==================== A1-3 School ====================

    @Test
    void schoolShouldComposeDepartmentsAndAggregateStudents() {
        School school = new School("计算机与信息学院");
        Department cs = new Department("软件工程系");
        school.addDepartment(cs);
        school.addStudent(new Student("柳淳", "202410120323"));

        assertEquals(1, school.getDepartments().size());
        assertEquals(1, school.getStudents().size());
        assertSame(school, cs.getSchool());
    }

    @Test
    void instructorShouldBelongToAtLeastOneDepartment() {
        Department cs = new Department("软件工程系");
        Department se = new Department("信息工程系");
        Instructor instructor = new Instructor("张老师", "T1001");
        cs.addInstructor(instructor);
        se.addInstructor(instructor);

        assertEquals(2, instructor.getDepartments().size());
        assertEquals(1, cs.getInstructors().size());
    }

    @Test
    void instructorShouldTeachAtMostThreeSubjects() {
        Instructor instructor = new Instructor("张老师", "T1001");
        instructor.teach(new Subject("课1", 3));
        instructor.teach(new Subject("课2", 3));
        instructor.teach(new Subject("课3", 3));
        assertEquals(3, instructor.getTaughtSubjects().size());

        assertThrows(IllegalStateException.class, () -> instructor.teach(new Subject("课4", 3)));
    }

    @Test
    void studentShouldAttendAtMostFiveSubjects() {
        Student student = new Student("柳淳", "202410120323");
        for (int i = 1; i <= 5; i++) {
            student.attend(new Subject("课程" + i, 3));
        }
        assertEquals(5, student.getSubjects().size());

        assertThrows(IllegalStateException.class, () -> student.attend(new Subject("课程6", 3)));
    }

    @Test
    void departmentShouldProvideAtLeastOneSubject() {
        Department cs = new Department("软件工程系");
        Subject subject = new Subject("面向对象", 3);
        cs.addSubject(subject);
        assertEquals(1, cs.getSubjects().size());
        assertSame(cs, subject.getDepartment());
    }

    // ==================== A1-4 网上购物系统 ====================

    @Test
    void customerShouldExposeFourAttributes() {
        Customer customer = new Customer("柳淳", "13800000000", "南京市西康路 1 号", true);
        assertEquals("柳淳", customer.getName());
        assertEquals("13800000000", customer.getContact());
        assertEquals("南京市西康路 1 号", customer.getDeliveryAddress());
        assertTrue(customer.isActive());
    }

    @Test
    void inactiveCustomerShouldNotPlaceOrder() {
        Customer customer = new Customer("张三", "13900000000", "某地", false);
        assertThrows(IllegalStateException.class, () -> customer.placeOrder(new Order(customer)));
    }

    @Test
    void orderShouldComposeOneToManyDetails() {
        Customer customer = new Customer("柳淳", "13800000000", "南京市", true);
        Order order = new Order(customer);
        order.addDetail(new OrderDetail(
                new Product("《软件工程》", 0.75D, "教材", new BigDecimal("59.00")), 2));
        order.addDetail(new OrderDetail(
                new Product("笔", 0.05D, "文具", new BigDecimal("5.00")), 3));
        customer.placeOrder(order);

        assertEquals(2, order.getDetails().size());
        assertEquals(1, customer.getOrders().size());
        assertSame(customer, order.getCustomer());
    }

    @Test
    void orderDetailShouldCalculateSubTotalAndWeight() {
        Product product = new Product("《软件工程》", 0.75D, "教材", new BigDecimal("59.00"));
        OrderDetail detail = new OrderDetail(product, 3);

        assertEquals(new BigDecimal("177.00"), detail.calculateSubTotal());
        assertEquals(2.25D, detail.calculateWeight(), 1e-9);
        assertEquals(new BigDecimal("177.00"), product.getPriceForQuantity(3));
    }

    @Test
    void orderStatusShouldContainFiveValues() {
        assertEquals(5, OrderStatus.values().length);
        assertEquals(OrderStatus.CREATE, OrderStatus.valueOf("CREATE"));
        assertNotNull(OrderStatus.valueOf("PAID"));
        assertNotNull(OrderStatus.valueOf("SHIPPING"));
        assertNotNull(OrderStatus.valueOf("DELIVERED"));
        assertNotNull(OrderStatus.valueOf("CANCEL"));
    }

    @Test
    void orderShouldFollowStatusStateMachine() {
        Order order = new Order(new Customer("柳淳", "138", "南京", true));
        order.addDetail(new OrderDetail(
                new Product("笔", 0.05D, "文具", new BigDecimal("5.00")), 1));
        assertEquals(OrderStatus.CREATE, order.getStatus());

        order.pay(new Cash(new BigDecimal("10.00"), order.calculateTotal()));
        assertEquals(OrderStatus.PAID, order.getStatus());

        order.ship();
        assertEquals(OrderStatus.SHIPPING, order.getStatus());

        order.deliver();
        assertEquals(OrderStatus.DELIVERED, order.getStatus());

        assertThrows(IllegalStateException.class, order::cancel);
    }

    @Test
    void shippingShouldPreventPaying() {
        Order order = new Order(new Customer("柳淳", "138", "南京", true));
        order.addDetail(new OrderDetail(
                new Product("笔", 0.05D, "文具", new BigDecimal("5.00")), 1));
        order.pay(new Cash(new BigDecimal("10.00"), order.calculateTotal()));
        order.ship();
        assertEquals(OrderStatus.SHIPPING, order.getStatus());

        // 已发货的订单不允许再次支付
        assertThrows(IllegalStateException.class,
                () -> order.pay(new Cash(new BigDecimal("10.00"), order.calculateTotal())));
    }

    @Test
    void shippingShouldRequirePaidStatus() {
        Order order = new Order(new Customer("柳淳", "138", "南京", true));
        order.addDetail(new OrderDetail(
                new Product("笔", 0.05D, "文具", new BigDecimal("5.00")), 1));
        // 未支付的订单不允许直接发货
        assertThrows(IllegalStateException.class, order::ship);
    }

    @Test
    void allFivePaymentKindsShouldExtendPayment() {
        Payment[] payments = new Payment[] {
                new Credit("6222021234567890", "VISA", new Date(), new BigDecimal("59.00")),
                new Cash(new BigDecimal("100.00"), new BigDecimal("59.00")),
                new WireTransfer("10230001", "中国工商银行", new BigDecimal("59.00")),
                new AliPay("liuchun@alipay.com", new BigDecimal("59.00")),
                new WeixinPay("wx_202410120323", new BigDecimal("59.00"))
        };
        for (Payment payment : payments) {
            assertTrue(payment instanceof Payment);
            assertEquals(new BigDecimal("59.00"), payment.getAmount());
        }
        assertEquals("信用卡", payments[0].getPaymentType());
        assertEquals("现金", payments[1].getPaymentType());
        assertEquals("在线转账", payments[2].getPaymentType());
        assertEquals("支付宝", payments[3].getPaymentType());
        assertEquals("微信支付", payments[4].getPaymentType());
    }

    @Test
    void cashShouldComputeChange() {
        Cash cash = new Cash(new BigDecimal("100.00"), new BigDecimal("59.00"));
        assertEquals(new BigDecimal("41.00"), cash.getChange());
    }

    @Test
    void creditShouldExposeNumberTypeAndExpireDate() {
        Calendar calendar = Calendar.getInstance();
        calendar.set(2030, Calendar.DECEMBER, 31);
        Credit credit = new Credit("6222021234567890", "VISA", calendar.getTime(),
                new BigDecimal("59.00"));

        assertEquals("6222021234567890", credit.getNumber());
        assertEquals("VISA", credit.getType());
        assertNotNull(credit.getExpireDate());
    }

    @Test
    void wireTransferShouldExposeBankIdAndBankName() {
        WireTransfer transfer = new WireTransfer("10230001", "中国工商银行", new BigDecimal("59.00"));
        assertEquals("10230001", transfer.getBankID());
        assertEquals("中国工商银行", transfer.getBankName());
    }

    @Test
    void aliPayAndWeixinPayShouldExposeNumber() {
        assertEquals("liuchun@alipay.com", new AliPay("liuchun@alipay.com", BigDecimal.TEN).getNumber());
        assertEquals("wx_202410120323", new WeixinPay("wx_202410120323", BigDecimal.TEN).getNumber());
    }

    @Test
    void orderShouldAggregateAtMostOnePayment() {
        Order order = new Order(new Customer("柳淳", "138", "南京", true));
        order.addDetail(new OrderDetail(
                new Product("笔", 0.05D, "文具", new BigDecimal("5.00")), 1));
        assertNull(order.getPayment());

        order.pay(new AliPay("liuchun@alipay.com", order.calculateTotal()));
        assertNotNull(order.getPayment());
        assertEquals(new BigDecimal("5.00"), order.getPayment().getAmount());
    }

    @Test
    void studentDuplicateSubjectShouldNotBeAddedTwice() {
        Student student = new Student("柳淳", "202410120323");
        Subject subject = new Subject("面向对象", 3);
        student.attend(subject);
        student.attend(subject);
        assertEquals(1, student.getSubjects().size());
        assertFalse(student.getSubjects().isEmpty());
    }
}
