package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;

/**
 * Product —— 商品项（A1-4）。
 *
 * <p>具有名称 title、重量 weight 和描述 description 属性，
 * 并具有 getPriceForQuantity() 和 getWeight() 方法。
 *
 * <p>为使 getPriceForQuantity() 可计算，另引入单价属性 unitPrice。
 */
public class Product {

    /** 商品名称。 */
    private String title;

    /** 商品重量。 */
    private Double weight;

    /** 商品描述。 */
    private String description;

    /** 商品单价。 */
    private BigDecimal unitPrice;

    public Product() {
    }

    public Product(String title, Double weight, String description, BigDecimal unitPrice) {
        this.title = title;
        this.weight = weight;
        this.description = description;
        this.unitPrice = unitPrice;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    /**
     * @return 商品重量
     */
    public Double getWeight() {
        return weight;
    }

    public void setWeight(Double weight) {
        this.weight = weight;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public BigDecimal getUnitPrice() {
        return unitPrice;
    }

    public void setUnitPrice(BigDecimal unitPrice) {
        this.unitPrice = unitPrice;
    }

    /**
     * 计算指定数量商品的总价。
     *
     * @param qty 数量
     * @return 单价乘以数量后的金额；qty 为 null 或单价为 null 时返回 0
     */
    public BigDecimal getPriceForQuantity(Integer qty) {
        if (qty == null || unitPrice == null) {
            return BigDecimal.ZERO;
        }
        if (qty < 0) {
            throw new IllegalArgumentException("数量不可为负数");
        }
        return unitPrice.multiply(BigDecimal.valueOf(qty));
    }

    @Override
    public String toString() {
        return "Product{title='" + title + "', weight=" + weight
                + ", unitPrice=" + unitPrice + "}";
    }
}
