package com.hj212.experiment3.a1_2;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * College —— 学院（A1-2）。
 *
 * <p>UML 模型对应：
 * <ul>
 *   <li>聚合（空心菱形）：College 聚合若干 Building，建筑构成学院，
 *       但 Building 可以脱离学院独立存在。</li>
 *   <li>组合（实心菱形）：College 组合若干 Course，课程是学院不可分割的组成部分，
 *       生命周期依附于学院。</li>
 * </ul>
 */
public class College {

    /** 学院名称。 */
    private String name;

    /** 聚合关系：建筑构成学院。 */
    private final List<Building> buildings = new ArrayList<Building>();

    /** 组合关系：课程是学院不可分割的组成部分。 */
    private final List<Course> courses = new ArrayList<Course>();

    public College() {
    }

    public College(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    /**
     * 聚合：向学院中加入一栋建筑。
     *
     * @param building 建筑对象
     */
    public void addBuilding(Building building) {
        if (building != null && !buildings.contains(building)) {
            buildings.add(building);
        }
    }

    /**
     * 组合：向学院开设一门课程。课程归属该学院，销毁学院即销毁其课程。
     *
     * @param course 课程对象
     */
    public void addCourse(Course course) {
        if (course != null && !courses.contains(course)) {
            courses.add(course);
            course.setCollege(this);
        }
    }

    public List<Building> getBuildings() {
        return Collections.unmodifiableList(buildings);
    }

    public List<Course> getCourses() {
        return Collections.unmodifiableList(courses);
    }

    /**
     * 组合关系的外键维护：移除课程时同步解除其所属学院。
     *
     * @param course 待移除的课程
     */
    public void removeCourse(Course course) {
        if (courses.remove(course)) {
            course.setCollege(null);
        }
    }

    @Override
    public String toString() {
        return "College{name='" + name + "', buildings=" + buildings.size()
                + ", courses=" + courses.size() + "}";
    }
}
