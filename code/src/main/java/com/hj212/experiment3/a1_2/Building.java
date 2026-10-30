package com.hj212.experiment3.a1_2;

/**
 * Building —— 建筑（A1-2）。
 *
 * <p>Building 被 College 以聚合方式拥有：建筑构成学院，
 * 但建筑对象可以脱离学院而独立存在。
 */
public class Building {

    /** 建筑名称。 */
    private String name;

    /** 建筑地址。 */
    private String address;

    public Building() {
    }

    public Building(String name, String address) {
        this.name = name;
        this.address = address;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    @Override
    public String toString() {
        return "Building{name='" + name + "', address='" + address + "'}";
    }
}
