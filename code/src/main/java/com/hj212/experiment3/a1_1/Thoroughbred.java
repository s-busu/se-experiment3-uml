package com.hj212.experiment3.a1_1;

import java.time.Year;

/**
 * Thoroughbred —— 优良品质的马（A1-1）。
 *
 * <p>UML 模型对应：
 * <ul>
 *   <li>属性 mother、father、birthyear：均为私有可见性 (-)</li>
 *   <li>操作 getCurrentAge()、getFather()、getMother()：均为公有可见性 (+)</li>
 * </ul>
 *
 * <p>mother 与 father 的类型同为 Thoroughbred，构成自关联（递归关联）：
 * 父马与母马本身也都是 Thoroughbred。
 */
public class Thoroughbred {

    /** 母马。 */
    private Thoroughbred mother;

    /** 父马。 */
    private Thoroughbred father;

    /** 出生年份。 */
    private int birthyear;

    public Thoroughbred() {
        this(null, null, Year.now().getValue());
    }

    public Thoroughbred(Thoroughbred mother, Thoroughbred father, int birthyear) {
        this.mother = mother;
        this.father = father;
        this.birthyear = birthyear;
    }

    /**
     * 计算当前年龄（周岁）：当前年份 - 出生年份。
     *
     * @return 以周岁计的年龄
     */
    public int getCurrentAge() {
        return Year.now().getValue() - birthyear;
    }

    /**
     * @return 父马对象，若未设置则为 null
     */
    public Thoroughbred getFather() {
        return father;
    }

    /**
     * @return 母马对象，若未设置则为 null
     */
    public Thoroughbred getMother() {
        return mother;
    }

    public int getBirthyear() {
        return birthyear;
    }

    public void setMother(Thoroughbred mother) {
        this.mother = mother;
    }

    public void setFather(Thoroughbred father) {
        this.father = father;
    }

    public void setBirthyear(int birthyear) {
        this.birthyear = birthyear;
    }

    @Override
    public String toString() {
        return "Thoroughbred{birthyear=" + birthyear + ", age=" + getCurrentAge() + "}";
    }
}
