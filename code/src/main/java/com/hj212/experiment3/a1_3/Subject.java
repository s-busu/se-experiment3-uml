package com.hj212.experiment3.a1_3;

/**
 * Subject —— 课程（A1-3）。
 *
 * <p>说明：需求中"系提供的课程 Subject"与"学生参加的课程"指向同一实体，
 * 指导教师教授、学生选修的都是 Subject。
 */
public class Subject {

    /** 课程名称。 */
    private String name;

    /** 学分。 */
    private int credit;

    /** 聚合关系的另一端：提供本课程的系。 */
    private Department department;

    public Subject() {
    }

    public Subject(String name, int credit) {
        this.name = name;
        this.credit = credit;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getCredit() {
        return credit;
    }

    public void setCredit(int credit) {
        this.credit = credit;
    }

    public Department getDepartment() {
        return department;
    }

    void setDepartment(Department department) {
        this.department = department;
    }

    @Override
    public String toString() {
        return "Subject{name='" + name + "', credit=" + credit + "}";
    }
}
