

import numpy as np

scores={}
while True:
    select=int(input(
        """
        ===================================
                     成绩分析系统
        ====================================

                    1. 输入成绩数据
                    2. 查看成绩统计
                    3. 查看成绩排名
                    4. 查看成绩分布
                    5. 查询学生成绩
                    6. 退出系统
                    请输入要使用的功能：
        """))



    if select==1:
        while True:
            name=input("请输入学生名字：")

            try:
                score = float(input("请输入学生成绩："))
                if 0<=score<=100:
                    if name in scores:
                        print("该学生已存在")
                    else:
                        scores[name]=score
                else:
                    print("请输入正确的成绩")
            except ValueError:
                print("请输入数字")
            if input("请选择是否继续录入（yes/no）；")=="no":
                break

    elif select==2:
        if not scores:
            print("暂无成绩数据")
        else:
            arr=np.array(list(scores.values()))
            print(f"最高分:{np.max(arr)}")
            print(f"最低分:{np.min(arr)}")
            print(f"平均分:{np.mean(arr)}")
            print(f"标准差:{np.std(arr)}")

    elif select==3:
        if not scores:
            print("暂无成绩数据")
        else:
            print("\n===== 成绩排名 =====")
            rank = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            for i, (name, score) in enumerate(rank, start=1):
                print(f"第{i}名  {name}  {score}分")

    elif select==4:
        if not scores:
            print("暂无成绩数据")
        else:
            a=b=c=d=f=0
            for score in scores.values():
                if 90<=score<=100:
                    a+=1
                elif 80<=score<90:
                    b+=1
                elif 70<=score<80:
                    c+=1
                elif 60<=score<70:
                    d+=1
                else:
                    f+=1
        print(f"优秀{a}良好{b}中等{c}及格{d}不及格{f}")


    elif select==5:
        name_LK=input("请输入要查询的学生名字：")
        if name_LK in scores.keys():
            print(f"该学生的成绩为{scores[name_LK]}")
        else:
            print("找不到该学生")





    elif select==6:
        print("退出系统")
        break


# 成绩分析命令行工具（Score Analyzer CLI）
# 一、项目背景
#
# 学校需要一个简单的成绩分析工具，教师可以通过命令行输入学生成绩数据，程序能够自动完成成绩统计、排名分析、成绩分布分析等功能。
#
# 学生需要使用 Python 编写一个命令行程序，并结合 NumPy 完成部分数据计算。
# 二、项目目标
#
# 完成一个命令行成绩分析系统，实现：
#
# 成绩数据录入
# 成绩统计分析
# 学生成绩排名
# 成绩等级划分
# 分析结果输出
#
# 要求：
#
# 使用 Python 完成程序开发
# 使用 NumPy 完成部分数组计算
# 程序具有清晰的菜单交互
# 代码结构合理
#
# 三、功能需求
# 功能1：输入学生成绩
#
# 程序启动后显示菜单：
#
# ============================
#      成绩分析系统
# ============================
#
# 1. 输入成绩数据
# 2. 查看成绩统计
# 3. 查看成绩排名
# 4. 查看成绩分布
# 5. 查询学生成绩
# 6. 退出系统
#
# 请选择：
#
# 用户可以输入学生信息：
#
# 例如：
#
# 请输入学生人数：5
#
# 请输入第1个学生姓名：张三
# 请输入成绩：85
#
# 请输入第2个学生姓名：李四
# 请输入成绩：92
#
# 请输入第3个学生姓名：王五
# 请输入成绩：76
