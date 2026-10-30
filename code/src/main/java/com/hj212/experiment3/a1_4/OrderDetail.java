package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;

/**
 * OrderDetail —— 订单详情（A1-4）。
 *
 * <p>具有数量 quantity 属性，并具有 calculateSubTotal()、
 * calculateWeight() 方法。
 */
public class OrderDetail {

    /** 数量。 */
    private Integer quantity;

    /** 对应的商品项。 */
    private Product product;

    public OrderDetail() {
    }

    public OrderDetail(Product product, Integer quantity) {
        this.product = product;
        this.quantity = quantity;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        if (quantity != null && quantity < 0) {
            throw new IllegalArgumentException("数量不可为负数");
        }
        this.quantity = quantity;
    }

    public Product getProduct() {
        return product;
    }

    public void setProduct(Product product) {
        this.product = product;
    }

    /**
     * 计算小计金额。
     *
     * @return 该明细行的商品总价，取自 Product.getPriceForQuantity()
     */
    public BigDecimal calculateSubTotal() {
        if (product == null) {
            return BigDecimal.ZERO;
        }
        return product.getPriceForQuantity(quantity);
    }

    /**
     * 计算该明细行的总重量。
     *
     * @return 商品重量乘以数量
     */
    public Double calculateWeight() {
        if (product == null || product.getWeight() == null || quantity == null) {
            return 0.0D;
        }
        return product.getWeight() * quantity;
    }

    @Override
    public String toString() {
        return "OrderDetail{product=" + (product == null ? "null" : product.getTitle())
                + ", quantity=" + quantity + ", subTotal=" + calculateSubTotal() + "}";
    }
}
