"""
====================================
学生成绩管理系统
数据类型与控制结构综合练习
====================================
"""

def show_menu():
    """显示操作菜单"""
    print("\n" + "=" * 30)
    print("   学生成绩管理系统")
    print("=" * 30)
    print("1. 录入学生成绩")
    print("2. 查询学生成绩")
    print("3. 显示所有学生")
    print("4. 统计信息（平均分/最高分/最低分）")
    print("5. 退出系统")
    print("=" * 30)


def add_student(students):
    """录入学生信息"""
    print("\n--- 录入学生成绩 ---")

    # 输入学号，检查是否已存在
    stu_id = input("请输入学号：").strip()
    if stu_id in students:
        print(f"学号 {stu_id} 已存在，无法重复录入！")
        return

    # 输入姓名
    name = input("请输入姓名：").strip()
    if name == "":
        print("姓名不能为空！")
        return

    # 输入各科成绩
    scores = {}  # 用字典存储各科成绩
    subjects = ["语文", "数学", "英语"]
    for subject in subjects:
        while True:
            try:
                score = float(input(f"请输入{subject}成绩："))
                if 0 <= score <= 100:
                    scores[subject] = score
                    break
                else:
                    print("成绩应在 0~100 之间，请重新输入。")
            except ValueError:
                print("请输入有效的数字！")

    # 存入学生字典
    students[stu_id] = {
        "姓名": name,
        "成绩": scores
    }
    print(f"学生 {name}（学号：{stu_id}）录入成功！")


def search_student(students):
    """查询学生成绩"""
    print("\n--- 查询学生成绩 ---")
    stu_id = input("请输入要查询的学号：").strip()

    if stu_id not in students:
        print(f"未找到学号为 {stu_id} 的学生。")
        return

    info = students[stu_id]
    print(f"\n学号：{stu_id}")
    print(f"姓名：{info['姓名']}")
    print("各科成绩：")
    for subject, score in info["成绩"].items():
        print(f"  {subject}：{score}")


def show_all(students):
    """显示所有学生信息"""
    print("\n--- 所有学生信息 ---")
    if len(students) == 0:
        print("暂无学生记录。")
        return

    for stu_id, info in students.items():
        print(f"\n学号：{stu_id}  姓名：{info['姓名']}")
        for subject, score in info["成绩"].items():
            print(f"  {subject}：{score}")


def show_stats(students):
    """统计各科平均分、最高分、最低分"""
    print("\n--- 成绩统计 ---")
    if len(students) == 0:
        print("暂无学生记录，无法统计。")
        return

    subjects = ["语文", "数学", "英语"]

    for subject in subjects:
        # 收集所有学生该科的成绩
        score_list = []
        for info in students.values():
            score_list.append(info["成绩"][subject])

        # 计算统计值
        avg = sum(score_list) / len(score_list)
        max_score = max(score_list)
        min_score = min(score_list)

        print(f"\n{subject}：")
        print(f"  平均分：{avg:.1f}")
        print(f"  最高分：{max_score}")
        print(f"  最低分：{min_score}")


def main():
    """主函数：菜单循环"""
    students = {}  # 用字典存储所有学生，键=学号，值=学生信息

    while True:
        show_menu()
        choice = input("请选择操作（1-5）：").strip()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            search_student(students)

        elif choice == "3":
            show_all(students)

        elif choice == "4":
            show_stats(students)

        elif choice == "5":
            print("谢谢使用，再见！")
            break

        else:
            print("无效选择，请输入 1-5 之间的数字。")


# 运行程序
if __name__ == "__main__":
    main()
