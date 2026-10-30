package com.hj212.experiment3.a1_4;

/**
 * OrderStatus —— 订单状态（A1-4）。
 *
 * <p>订单状态包括 CREATE、PAID、SHIPPING、DELIVERED、CANCEL 五种。
 */
public enum OrderStatus {

    /** 已创建，尚未支付。 */
    CREATE,

    /** 已支付。 */
    PAID,

    /** 已发货。 */
    SHIPPING,

    /** 已送达。 */
    DELIVERED,

    /** 已取消。 */
    CANCEL;

    /**
     * 判断能否从当前状态流转到目标状态。
     *
     * @param target 目标状态
     * @return 允许流转返回 true
     */
    public boolean canTransitionTo(OrderStatus target) {
        if (target == null) {
            return false;
        }
        switch (this) {
            case CREATE:
                return target == PAID || target == CANCEL;
            case PAID:
                return target == SHIPPING || target == CANCEL;
            case SHIPPING:
                return target == DELIVERED;
            case DELIVERED:
            case CANCEL:
            default:
                return false;
        }
    }
}
