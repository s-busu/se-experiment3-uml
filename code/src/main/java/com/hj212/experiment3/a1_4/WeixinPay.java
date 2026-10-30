package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;

/**
 * WeixinPay —— 微信支付（A1-4）。
 *
 * <p>具有卡号属性。
 */
public class WeixinPay extends Payment {

    /** 卡号。 */
    private String number;

    public WeixinPay() {
    }

    public WeixinPay(String number, BigDecimal amount) {
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
        return "微信支付";
    }
}
