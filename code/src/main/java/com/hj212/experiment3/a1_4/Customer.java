package com.hj212.experiment3.a1_4;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Customer —— 客户（A1-4）。
 *
 * <p>具有四个属性：姓名 name、联系电话 contact、
 * 邮寄地址 deliveryAddress 和是否激活状态 active。
 */
public class Customer {

    /** 姓名。 */
    private String name;

    /** 联系电话。 */
    private String contact;

    /** 邮寄地址。 */
    private String deliveryAddress;

    /** 是否激活状态。 */
    private boolean active;

    /** 关联关系：客户下的订单，0 到多个。 */
    private final List<Order> orders = new ArrayList<Order>();

    public Customer() {
    }

    public Customer(String name, String contact, String deliveryAddress, boolean active) {
        this.name = name;
        this.contact = contact;
        this.deliveryAddress = deliveryAddress;
        this.active = active;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getContact() {
        return contact;
    }

    public void setContact(String contact) {
        this.contact = contact;
    }

    public String getDeliveryAddress() {
        return deliveryAddress;
    }

    public void setDeliveryAddress(String deliveryAddress) {
        this.deliveryAddress = deliveryAddress;
    }

    /**
     * @return 是否激活
     */
    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    /**
     * 下单：创建订单并与该客户关联。
     *
     * @param order 待创建的订单
     * @throws IllegalStateException 当客户未激活时抛出
     */
    public void placeOrder(Order order) {
        if (!active) {
            throw new IllegalStateException("客户 " + name + " 未激活，不允许下单");
        }
        if (order == null) {
            throw new IllegalArgumentException("订单不可为 null");
        }
        order.setCustomer(this);
        if (!orders.contains(order)) {
            orders.add(order);
        }
    }

    public List<Order> getOrders() {
        return Collections.unmodifiableList(orders);
    }

    @Override
    public String toString() {
        return "Customer{name='" + name + "', contact='" + contact
                + "', deliveryAddress='" + deliveryAddress
                + "', active=" + active + ", orders=" + orders.size() + "}";
    }
}
