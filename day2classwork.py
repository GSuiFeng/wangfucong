import numpy as np


"""练习1"""
# ### **练习 1：数组创建与形状操作**
# #### **任务**
# 1. 创建一个形状为 `(3, 4)` 的二维随机整数数组（范围 0~9）。
# 2. 将该数组重塑为 `(4, 3)` 并转置。
# 3. 提取数组中所有大于 5 的元素，生成一个新数组。
#
# #### **要求**
# - 使用 `np.random.randint` 生成随机数组。
# - 用 `reshape` 和 `T` 完成形状变换。
# - 用布尔索引提取元素。
#
# #### **示例代码框架**
# ```python
# import numpy as np
# arr = np.random.randint(0, 10, size=(3, 4))  # 任务1
# reshaped_arr = arr.reshape(4, 3).T           # 任务2
#                   # 任务3
# ```filtered_arr = arr[arr > 5]
#
# ---



arr0 = np.random.randint(0, 10, size=(3, 4))
reshape_arr = arr0.reshape(4, 3).T
filtered_arr = arr0[arr0 > 5]




"""练习2"""
# ### **练习 2：索引与切片**
# #### **任务**
# 给定数组：
# ```python
# arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
# ```
# 1. 获取第 2 行的第 1~3 列（输出 `[5, 6, 7]`）。
# 2. 获取所有行的第 3 列（输出 `[3, 7, 11]`）。
# 3. 使用步长切片获取奇数行（第1、3行）。
#
# #### **要求**
# - 使用逗号分隔行列索引（如 `arr[1, 0:3]`）。
# - 对比 `arr[:, 2]` 和 `arr[::2, :]` 的用法。
#
# ---

arr_=np.array([[1,2,3,4],
             [5,6,7,8],
             [9,10,11,12]])

print(arr_[1,0:3])  #1

print(arr_[:,2]) #2

print(arr_[::2,:]) #3




"""练习3"""
# ### **练习 3：矢量化运算与聚合函数**
# #### **任务**
# 1. 计算两个随机数组 `A(2,3)` 和 `B(2,3)` 的逐元素乘法（`*`）和矩阵乘法（`@`）。
# 2. 对数组 `[[1, 2], [3, 4]]` 分别按行和列求和。
# 3. 计算数组 `[1.2, 3.5, 2.8]` 的均值、标准差和四舍五入结果。
#
# #### **要求**
# - 区分 `*` 和 `@` 的用途。
# - 使用 `np.sum(axis=0/1)` 指定轴向。
# - 调用 `np.mean()`, `np.std()`, `np.round()`。
#
# #### **示例输出**
# ```python
# A * B = [[ 5 12 21] [32 45 60]]  # 逐元素乘
# A @ B.T = [[ 38 83]]             # 矩阵乘
# 列求和: [4 6]                     # axis=0
# 四舍五入: [1. 4. 3.]             # np.round
# ```
#
# ---

np.random.seed(20)
"""任务一"""
arrA=np.random.randint(1,10,size=(2,3))
print(arrA)
arrB=np.random.randint(1,10,size=(2,3))
print(arrB)

arr1_1=arrA*arrB
print(arr1_1)

arr1_2=arrA @ arrB.T
print(arr1_2)

"""任务二"""

arr2=[[1,2],
     [3,4]]

arr2_1=np.sum(arr2,axis=0)
print(arr2_1) #列
arr2_2=np.sum(arr2,axis=1)
print(arr2_2) #行


arr3=[1.2,3.5,2.8]
mean_arr3=np.mean(arr3)
print(mean_arr3)  #平均值

std_arr3=np.std(arr3)
print(std_arr3)  #标准差

round_arr3=np.round(arr3)
print(round_arr3)  #四舍五入


 ### **练习 4：综合应用**
# #### **任务**
# 1. 生成一个长度为 10 的随机浮点数组（范围 0~1），将其归一化到 [0, 100] 区间。
# 2. 计算该数组的累计和（`cumsum`）和累计最大值（`cummax`）。
#
# #### **提示**
# - 归一化公式：`(arr - min) / (max - min) * 100`。
# - 使用 `np.cumsum()` 和 `np.maximum.accumulate()`。
#
# ---
#


np.random.seed(20)
_arr = np.random.rand(10)
normalized=(_arr-_arr.min())/(_arr.max()-_arr.min())*100
cum_sum=np.cumsum(normalized)
cum_max=np.maximum.accumulate(normalized)
print(np.round(normalized,2)) #归一化
print(np.round(cum_sum,2)) #数组累计
print(np.round(cum_max,2)) #累计最大值