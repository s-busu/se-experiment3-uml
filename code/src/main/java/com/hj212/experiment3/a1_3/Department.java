package com.hj212.experiment3.a1_3;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Department —— 系（A1-3）。
 *
 * <p>约束：
 * <ul>
 *   <li>{每个系至少拥有 1 位指导教师}</li>
 *   <li>{每个系至少提供 1 门课程}</li>
 * </ul>
 */
public class Department {

    /** 系名称。 */
    private String name;

    /** 组合关系的另一端：所属学院。 */
    private School school;

    /** 聚合关系：本系拥有的指导教师，至少 1 位。 */
    private final List<Instructor> instructors = new ArrayList<Instructor>();

    /** 聚合关系：本系提供的课程，至少 1 门。 */
    private final List<Subject> subjects = new ArrayList<Subject>();

    public Department() {
    }

    public Department(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public School getSchool() {
        return school;
    }

    void setSchool(School school) {
        this.school = school;
    }

    /**
     * 聚合关系：系拥有指导教师。
     *
     * @param instructor 指导教师
     */
    public void addInstructor(Instructor instructor) {
        if (instructor != null && !instructors.contains(instructor)) {
            instructors.add(instructor);
            instructor.addDepartment(this);
        }
    }

    /**
     * 聚合关系：系提供课程。
     *
     * @param subject 课程
     */
    public void addSubject(Subject subject) {
        if (subject != null && !subjects.contains(subject)) {
            subjects.add(subject);
            subject.setDepartment(this);
        }
    }

    public List<Instructor> getInstructors() {
        return Collections.unmodifiableList(instructors);
    }

    public List<Subject> getSubjects() {
        return Collections.unmodifiableList(subjects);
    }

    @Override
    public String toString() {
        return "Department{name='" + name + "', instructors=" + instructors.size()
                + ", subjects=" + subjects.size() + "}";
    }
}
