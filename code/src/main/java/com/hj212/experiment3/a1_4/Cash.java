package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;

/**
 * Cash —— 现金支付（A1-4）。
 *
 * <p>具有支付金额 cashTendered 属性（顾客交付的现金总额，
 * 可大于应付金额，差额即为找零）。
 */
public class Cash extends Payment {

    /** 顾客交付的现金金额。 */
    private BigDecimal cashTendered;

    public Cash() {
    }

    public Cash(BigDecimal cashTendered, BigDecimal amount) {
        super(amount);
        this.cashTendered = cashTendered;
    }

    public BigDecimal getCashTendered() {
        return cashTendered;
    }

    public void setCashTendered(BigDecimal cashTendered) {
        this.cashTendered = cashTendered;
    }

    /**
     * 计算应找零金额。
     *
     * @return 现金交付额减应付金额；不为负
     */
    public BigDecimal getChange() {
        if (cashTendered == null || getAmount() == null) {
            return BigDecimal.ZERO;
        }
        BigDecimal change = cashTendered.subtract(getAmount());
        return change.max(BigDecimal.ZERO);
    }

    @Override
    public String getPaymentType() {
        return "现金";
    }
}
