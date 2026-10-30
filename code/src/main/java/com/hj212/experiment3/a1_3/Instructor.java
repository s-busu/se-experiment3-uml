package com.hj212.experiment3.a1_3;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Instructor —— 指导教师（A1-3）。
 *
 * <p>约束：{@code {每个指导教师至少属于某个系，且教授 1-3 门课程}}。
 */
public class Instructor {

    /** 姓名。 */
    private String name;

    /** 工号。 */
    private String employeeNo;

    /** 聚合关系的另一端：所属的系，至少 1 个。 */
    private final List<Department> departments = new ArrayList<Department>();

    /** 教授的课程，1-3 门。 */
    private final List<Subject> taughtSubjects = new ArrayList<Subject>();

    /** 约束上限：最多教授 3 门课程。 */
    private static final int MAX_SUBJECTS = 3;

    public Instructor() {
    }

    public Instructor(String name, String employeeNo) {
        this.name = name;
        this.employeeNo = employeeNo;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmployeeNo() {
        return employeeNo;
    }

    public void setEmployeeNo(String employeeNo) {
        this.employeeNo = employeeNo;
    }

    /**
     * 关联关系的另一端维护：指导教师加入某系。
     *
     * @param department 系
     */
    void addDepartment(Department department) {
        if (department != null && !departments.contains(department)) {
            departments.add(department);
        }
    }

    /**
     * 关联：指导教师教授一门课程。
     *
     * @param subject 课程
     * @throws IllegalStateException 当已教授课程数超过 3 时抛出，违反多重性 1..3
     */
    public void teach(Subject subject) {
        if (subject == null) {
            throw new IllegalArgumentException("课程不可为 null");
        }
        if (taughtSubjects.contains(subject)) {
            return;
        }
        if (taughtSubjects.size() >= MAX_SUBJECTS) {
            throw new IllegalStateException(
                    "违反多重性约束：每位指导教师最多教授 " + MAX_SUBJECTS + " 门课程");
        }
        taughtSubjects.add(subject);
    }

    public List<Department> getDepartments() {
        return Collections.unmodifiableList(departments);
    }

    public List<Subject> getTaughtSubjects() {
        return Collections.unmodifiableList(taughtSubjects);
    }

    @Override
    public String toString() {
        return "Instructor{name='" + name + "', employeeNo='" + employeeNo
                + "', departments=" + departments.size()
                + ", taughtSubjects=" + taughtSubjects.size() + "}";
    }
}
