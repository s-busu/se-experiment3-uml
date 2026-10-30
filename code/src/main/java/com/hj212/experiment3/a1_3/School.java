package com.hj212.experiment3.a1_3;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * School —— 学院（A1-3）。
 *
 * <p>UML 模型对应：
 * <ul>
 *   <li>School 由 1 到多个系 Department 构成（组合，实心菱形）</li>
 *   <li>School 拥有 0 到多名学生 Student（聚合，空心菱形）</li>
 * </ul>
 */
public class School {

    /** 学院名称。 */
    private String name;

    /** 组合关系：学院由若干系构成，至少 1 个。 */
    private final List<Department> departments = new ArrayList<Department>();

    /** 聚合关系：学院拥有 0 到多名学生。 */
    private final List<Student> students = new ArrayList<Student>();

    public School() {
    }

    public School(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    /**
     * 组合关系：向学院增设一个系。
     *
     * @param department 系
     */
    public void addDepartment(Department department) {
        if (department != null && !departments.contains(department)) {
            departments.add(department);
            department.setSchool(this);
        }
    }

    /**
     * 聚合关系：学院招收一名学生（可从 0 名开始）。
     *
     * @param student 学生
     */
    public void addStudent(Student student) {
        if (student != null && !students.contains(student)) {
            students.add(student);
            student.setSchool(this);
        }
    }

    public List<Department> getDepartments() {
        return Collections.unmodifiableList(departments);
    }

    public List<Student> getStudents() {
        return Collections.unmodifiableList(students);
    }

    @Override
    public String toString() {
        return "School{name='" + name + "', departments=" + departments.size()
                + ", students=" + students.size() + "}";
    }
}
