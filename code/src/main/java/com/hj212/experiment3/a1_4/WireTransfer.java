package com.hj212.experiment3.a1_4;

import java.math.BigDecimal;

/**
 * WireTransfer —— 在线转账（A1-4）。
 *
 * <p>具有银行 ID bankID 和银行名称 bankName 属性。
 */
public class WireTransfer extends Payment {

    /** 银行 ID。 */
    private String bankID;

    /** 银行名称。 */
    private String bankName;

    public WireTransfer() {
    }

    public WireTransfer(String bankID, String bankName, BigDecimal amount) {
        super(amount);
        this.bankID = bankID;
        this.bankName = bankName;
    }

    public String getBankID() {
        return bankID;
    }

    public void setBankID(String bankID) {
        this.bankID = bankID;
    }

    public String getBankName() {
        return bankName;
    }

    public void setBankName(String bankName) {
        this.bankName = bankName;
    }

    @Override
    public String getPaymentType() {
        return "在线转账";
    }
}
