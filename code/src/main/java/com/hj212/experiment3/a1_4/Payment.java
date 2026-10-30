package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;

/**
 * Payment —— 支付方式（A1-4，抽象类）。
 *
 * <p>具有支付金额 amount 属性。抽象出五种具体支付方式：
 * Credit（信用卡）、Cash（现金）、WireTransfer（在线转账）、
 * AliPay（支付宝）、WeixinPay（微信支付）。
 */
public abstract class Payment {

    /** 支付金额。 */
    private BigDecimal amount;

    protected Payment() {
    }

    protected Payment(BigDecimal amount) {
        this.amount = amount;
    }

    public BigDecimal getAmount() {
        return amount;
    }

    public void setAmount(BigDecimal amount) {
        this.amount = amount;
    }

    /**
     * 支付方式名称，用于日志与展示。
     *
     * @return 支付方式名称
     */
    public abstract String getPaymentType();
}
