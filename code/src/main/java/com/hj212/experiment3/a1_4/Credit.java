package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;
import java.util.Date;

/**
 * Credit —— 信用卡支付（A1-4）。
 *
 * <p>具有卡号 number、类型 type 和过期日期 expireDate 属性。
 */
public class Credit extends Payment {

    /** 卡号。 */
    private String number;

    /** 卡类型。 */
    private String type;

    /** 过期日期。 */
    private Date expireDate;

    public Credit() {
    }

    public Credit(String number, String type, Date expireDate, BigDecimal amount) {
        super(amount);
        this.number = number;
        this.type = type;
        this.expireDate = expireDate;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public Date getExpireDate() {
        return expireDate;
    }

    public void setExpireDate(Date expireDate) {
        this.expireDate = expireDate;
    }

    @Override
    public String getPaymentType() {
        return "信用卡";
    }
}
