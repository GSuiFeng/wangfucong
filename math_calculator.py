"""
====================================
数学计算器
函数与文件操作实践
====================================
"""

import math

HISTORY_FILE = "calc_history.txt"  # 历史记录文件


# ========== 5 个自定义计算函数 ==========

def add(a, b):
    """加法"""
    return a + b


def subtract(a, b):
    """减法"""
    return a - b


def multiply(a, b):
    """乘法"""
    return a * b


def divide(a, b):
    """除法（含除零检查）"""
    if b == 0:
        raise ZeroDivisionError("错误：除数不能为零！")
    return a / b


def power(a, b):
    """幂运算：a 的 b 次方"""
    return a ** b


def sqrt(a):
    """开平方根"""
    if a < 0:
        raise ValueError("错误：不能对负数开平方根！")
    return math.sqrt(a)


# ========== 历史记录管理 ==========

def save_history(expression, result):
    """将一条计算记录追加到文件"""
    record = f"{expression} = {result}"
    # 以追加模式写入文件
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(record + "\n")


def read_history():
    """从文件读取全部历史记录，返回列表"""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [line.strip() for line in lines]
    except FileNotFoundError:
        return []  # 文件不存在则返回空列表


def show_history():
    """显示历史记录"""
    print("\n--- 计算历史记录 ---")
    records = read_history()
    if len(records) == 0:
        print("暂无历史记录。")
        return
    for i, record in enumerate(records, 1):
        print(f"  {i}. {record}")


# ========== 菜单与主逻辑 ==========

def show_menu():
    """显示操作菜单"""
    print("\n" + "=" * 30)
    print("     数学计算器")
    print("=" * 30)
    print("1. 加法（两个数）")
    print("2. 减法（两个数）")
    print("3. 乘法（两个数）")
    print("4. 除法（两个数）")
    print("5. 幂运算（底数 ^ 指数）")
    print("6. 开平方根（一个数）")
    print("7. 查看历史记录")
    print("8. 退出")
    print("=" * 30)


def get_two_numbers():
    """获取用户输入的两个数，带异常处理"""
    try:
        a = float(input("请输入第一个数："))
        b = float(input("请输入第二个数："))
        return a, b
    except ValueError:
        print("输入无效，请输入数字！")
        return None, None


def get_one_number():
    """获取用户输入的一个数"""
    try:
        a = float(input("请输入一个数："))
        return a
    except ValueError:
        print("输入无效，请输入数字！")
        return None


def main():
    """主函数：菜单循环"""
    while True:
        show_menu()
        choice = input("请选择操作（1-8）：").strip()

        # 加法
        if choice == "1":
            a, b = get_two_numbers()
            if a is not None:
                result = add(a, b)
                expr = f"{a} + {b}"
                print(f"结果：{result}")
                save_history(expr, result)

        # 减法
        elif choice == "2":
            a, b = get_two_numbers()
            if a is not None:
                result = subtract(a, b)
                expr = f"{a} - {b}"
                print(f"结果：{result}")
                save_history(expr, result)

        # 乘法
        elif choice == "3":
            a, b = get_two_numbers()
            if a is not None:
                result = multiply(a, b)
                expr = f"{a} * {b}"
                print(f"结果：{result}")
                save_history(expr, result)

        # 除法
        elif choice == "4":
            a, b = get_two_numbers()
            if a is not None:
                try:
                    result = divide(a, b)
                    expr = f"{a} / {b}"
                    print(f"结果：{result}")
                    save_history(expr, result)
                except ZeroDivisionError as e:
                    print(e)

        # 幂运算
        elif choice == "5":
            a, b = get_two_numbers()
            if a is not None:
                result = power(a, b)
                expr = f"{a} ^ {b}"
                print(f"结果：{result}")
                save_history(expr, result)

        # 开平方根
        elif choice == "6":
            a = get_one_number()
            if a is not None:
                try:
                    result = sqrt(a)
                    expr = f"sqrt({a})"
                    print(f"结果：{result}")
                    save_history(expr, result)
                except ValueError as e:
                    print(e)

        # 查看历史记录
        elif choice == "7":
            show_history()

        # 退出
        elif choice == "8":
            print("谢谢使用，再见！")
            break

        # 无效选择
        else:
            print("无效选择，请输入 1-8 之间的数字。")


# 运行程序
if __name__ == "__main__":
    main()
