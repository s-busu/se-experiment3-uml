package com.hj212.experiment3.a1_2;

/**
 * Course —— 课程（A1-2）。
 *
 * <p>约束性注释：{@code {Course 一定在某个 Building 中进行}}。
 * <p>即每个 Course 必须且仅能关联一个 Building（Building 端多重性为 "1"），
 * 一栋 Building 可以开设多门 Course（Course 端多重性为 "*"）。
 */
public class Course {

    /** 课程名称。 */
    private String name;

    /** 约束：Course 一定在某个 Building 中进行 —— 关联的 Building 不可为空。 */
    private Building building;

    /** 组合关系的另一端：所属学院。 */
    private College college;

    public Course() {
    }

    public Course(String name, Building building) {
        this.name = name;
        setBuilding(building);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    /**
     * @return 本课程所在的建筑；由约束保证非空
     */
    public Building getBuilding() {
        return building;
    }

    /**
     * 建立课程与建筑之间的关联，维护约束 {@code {Course 一定在某个 Building 中进行}}。
     *
     * @param building 课程所在建筑，不可为 null
     * @throws IllegalArgumentException 当 building 为 null 时抛出，违反约束性注释
     */
    public void setBuilding(Building building) {
        if (building == null) {
            throw new IllegalArgumentException(
                    "违反约束：{Course 一定在某个 Building 中进行}，building 不可为 null");
        }
        this.building = building;
    }

    public College getCollege() {
        return college;
    }

    void setCollege(College college) {
        this.college = college;
    }

    @Override
    public String toString() {
        return "Course{name='" + name + "', building=" + (building == null ? "null" : building.getName()) + "}";
    }
}
