package com.hj212.experiment3.a1_3;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Student —— 学生（A1-3）。
 *
 * <p>约束：{@code {学院拥有 0 到多名学生；每名学生参加 1-5 门课程学习}}。
 */
public class Student {

    /** 姓名。 */
    private String name;

    /** 学号。 */
    private String studentNo;

    /** 聚合关系的另一端：所属学院。 */
    private School school;

    /** 参加学习的课程，1-5 门。 */
    private final List<Subject> subjects = new ArrayList<Subject>();

    /** 约束上限：最多参加 5 门课程。 */
    private static final int MAX_SUBJECTS = 5;

    public Student() {
    }

    public Student(String name, String studentNo) {
        this.name = name;
        this.studentNo = studentNo;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getStudentNo() {
        return studentNo;
    }

    public void setStudentNo(String studentNo) {
        this.studentNo = studentNo;
    }

    public School getSchool() {
        return school;
    }

    void setSchool(School school) {
        this.school = school;
    }

    /**
     * 关联：学生参加一门课程学习。
     *
     * @param subject 课程
     * @throws IllegalStateException 当参加课程数超过 5 时抛出，违反多重性 1..5
     */
    public void attend(Subject subject) {
        if (subject == null) {
            throw new IllegalArgumentException("课程不可为 null");
        }
        if (subjects.contains(subject)) {
            return;
        }
        if (subjects.size() >= MAX_SUBJECTS) {
            throw new IllegalStateException(
                    "违反多重性约束：每名学生最多参加 " + MAX_SUBJECTS + " 门课程");
        }
        subjects.add(subject);
    }

    public List<Subject> getSubjects() {
        return Collections.unmodifiableList(subjects);
    }

    @Override
    public String toString() {
        return "Student{name='" + name + "', studentNo='" + studentNo
                + "', subjects=" + subjects.size() + "}";
    }
}
