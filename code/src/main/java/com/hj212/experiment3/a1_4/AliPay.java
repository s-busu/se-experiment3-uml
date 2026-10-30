package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;

/**
 * AliPay —— 支付宝支付（A1-4）。
 *
 * <p>具有卡号（支付宝账号）number 属性。
 */
public class AliPay extends Payment {

    /** 卡号 / 支付宝账号。 */
    private String number;

    public AliPay() {
    }

    public AliPay(String number, BigDecimal amount) {
        super(amount);
        this.number = number;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    @Override
    public String getPaymentType() {
        return "支付宝";
    }
}
