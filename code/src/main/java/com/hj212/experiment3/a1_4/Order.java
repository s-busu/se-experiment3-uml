package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;

/**
 * Order —— 订单（A1-4）。
 *
 * <p>具有创建日期 createDate 和订单状态 status
 * （CREATE、PAID、SHIPPING、DELIVERED、CANCEL）属性。
 *
 * <p>组合关系：一个订单包含 1 到多条订单明细 OrderDetail。
 */
public class Order {

    /** 创建日期。 */
    private Date createDate;

    /** 订单状态。 */
    private OrderStatus status;

    /** 组合关系：订单包含的明细，至少 1 条。 */
    private final List<OrderDetail> details = new ArrayList<OrderDetail>();

    /** 关联关系：订单采用的支付方式（支付前为 null）。 */
    private Payment payment;

    /** 关联关系：下单的客户。 */
    private Customer customer;

    public Order() {
        this.createDate = new Date();
        this.status = OrderStatus.CREATE;
    }

    public Order(Customer customer) {
        this();
        this.customer = customer;
    }

    public Date getCreateDate() {
        return createDate;
    }

    public void setCreateDate(Date createDate) {
        this.createDate = createDate;
    }

    public OrderStatus getStatus() {
        return status;
    }

    public void setStatus(OrderStatus status) {
        this.status = status;
    }

    /**
     * 组合关系：向订单添加一条明细。
     *
     * @param detail 订单明细
     */
    public void addDetail(OrderDetail detail) {
        if (detail != null && !details.contains(detail)) {
            details.add(detail);
        }
    }

    public List<OrderDetail> getDetails() {
        return Collections.unmodifiableList(details);
    }

    public Payment getPayment() {
        return payment;
    }

    public Customer getCustomer() {
        return customer;
    }

    void setCustomer(Customer customer) {
        this.customer = customer;
    }

    /**
     * 计算订单应付总额。
     *
     * @return 所有明细小计之和
     */
    public BigDecimal calculateTotal() {
        BigDecimal total = BigDecimal.ZERO;
        for (OrderDetail detail : details) {
            total = total.add(detail.calculateSubTotal());
        }
        return total;
    }

    /**
     * 计算订单总重量。
     *
     * @return 所有明细重量之和
     */
    public Double calculateTotalWeight() {
        double total = 0.0D;
        for (OrderDetail detail : details) {
            total += detail.calculateWeight();
        }
        return total;
    }

    /**
     * 支付订单：校验状态流转并记录支付方式。
     *
     * @param p 支付方式
     * @throws IllegalStateException 当状态不允许支付时抛出
     */
    public void pay(Payment p) {
        requireTransition(OrderStatus.PAID);
        if (p == null) {
            throw new IllegalArgumentException("支付方式不可为 null");
        }
        this.payment = p;
        p.setAmount(calculateTotal());
        this.status = OrderStatus.PAID;
    }

    /**
     * 发货。
     */
    public void ship() {
        requireTransition(OrderStatus.SHIPPING);
        this.status = OrderStatus.SHIPPING;
    }

    /**
     * 确认送达。
     */
    public void deliver() {
        requireTransition(OrderStatus.DELIVERED);
        this.status = OrderStatus.DELIVERED;
    }

    /**
     * 取消订单。
     */
    public void cancel() {
        requireTransition(OrderStatus.CANCEL);
        this.status = OrderStatus.CANCEL;
    }

    /**
     * 校验当前状态是否允许流转到目标状态。
     *
     * @param target 目标状态
     */
    private void requireTransition(OrderStatus target) {
        if (status == null || !status.canTransitionTo(target)) {
            throw new IllegalStateException(
                    "订单状态不允许由 " + status + " 流转到 " + target);
        }
    }

    @Override
    public String toString() {
        return "Order{createDate=" + createDate + ", status=" + status
                + ", details=" + details.size() + ", total=" + calculateTotal() + "}";
    }
}
