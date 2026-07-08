import numpy as np
import timeit
# ### **NumPy 高级应用与金融数据分析实战**
# **目标**：通过矩阵运算和性能优化技术解决实际问题，结合金融数据分析场景强化实战能力。
# ---
# ## **练习 1：矩阵运算与性能优化**
# ### **任务**
# 1. **矩阵乘法优化**
#    - 生成两个大型随机矩阵 `A(1000, 2000)` 和 `B(2000, 3000)`，比较以下方法的计算时间：
#      - 普通 `np.dot(A, B)`
#      - 使用 `@` 运算符
#      - 使用 `np.matmul`
#    - 用 `%timeit` 测量性能差异。

np.random.seed(50)

arrA=np.random.rand(1000,2000)
arrB=np.random.rand(2000,3000)

print("result1:",timeit.timeit(lambda:np.dot(arrA,arrB),number=10))
print("result2:",timeit.timeit(lambda:arrA@arrB,number=10))
print("result3:",timeit.timeit(lambda:np.matmul(arrA,arrB),number=10))


# 2. **内存布局影响**
#    - 创建一个 `(1000, 1000)` 的数组，分别以 C 顺序（行优先）和 F 顺序（列优先）存储。
#    - 对两种布局的数组按行/列求和，比较速度差异。

arr2=np.random.rand(1000,1000)
arr2_C=np.array(arr2,order="C")
arr2_F=np.array(arr2,order="F")
sumL_c=arr2_C.sum(axis=1)#C顺序列求和
sumH_c=arr2_C.sum(axis=0)#C顺序行求和
sumL_f=arr2_F.sum(axis=1)#F顺序列求和
sumH_f=arr2_F.sum(axis=0)#F顺序行求和
print(timeit.timeit(lambda:sumH_c,number=10))
print(timeit.timeit(lambda:sumL_c,number=10))
print(timeit.timeit(lambda:sumH_f,number=10))
print(timeit.timeit(lambda:sumL_f,number=10))



# 3. **避免临时内存分配**
#    - 计算 `A^2 + 2*A + 1`，使用 `np.add(np.multiply(A, A), np.multiply(2, A), 1)` 避免中间变量。
#
# #### **关键知识点**
# - `np.matmul` vs `dot` vs `@`
# - `order='C'`（行优先） vs `order='F'`（列优先）
# - 使用 `out` 参数减少内存分配（如 `np.multiply(A, A, out=result)`）

A=np.random.randint(1,10,size=(3,4))
result=np.add(np.multiply(A,A),np.multiply(A,2))+1
print(result)





# ---
# ## **练习 2：金融数据分析实战**
# ### **任务**
# 1. **股票收益率计算**
#    - 给定股价数组 `prices = [100, 102, 105, 103, 107]`，计算每日对数收益率：
#      \[
#      \text{returns} = \log(\frac{prices_{t}}{prices_{t-1}})
#      \]
#    - 使用 `np.diff` 和 `np.log` 向量化实现。

price=np.array([100,102,105,103,107])
log_result=np.diff(np.log(price))
print(log_result)


#
# 2. **移动平均线**
#    - 生成包含 100 个交易日的随机股价数据，计算 5 日、20 日移动平均线（MA）。
#    - 使用 `np.convolve` 或 `np.cumsum` 优化计算。np.random.seed(42)


price = 100 + np.cumsum(np.random.randn(100) * 3)

price = np.abs(price)

print(f"生成的股价数据前5天: {price[:5]}")


ma5_convolve = np.convolve(price, np.ones(5)/5, mode='valid')
ma20_convolve = np.convolve(price, np.ones(20)/20, mode='valid')











# 3. **风险分析**
#    - 生成 1000 支股票 1 年的收益率数据（形状 `(1000, 252)`），计算：
#      - 每支股票的年化波动率（标准差 × √252）
#      - 股票间的相关系数矩阵（`np.corrcoef`）
#
# #### **示例代码**
# ```python
# # 对数收益率
# prices = np.array([100, 102, 105, 103, 107])
# returns = np.log(prices[1:] / prices[:-1])
#
# # 5日移动平均线
# window = 5
# ma5 = np.convolve(prices, np.ones(window)/window, mode='valid')
# ```
#
# ---
# #### **关键函数**
# - `numba.njit`
# - `arr.flags.owndata`
# - `keepdims=True` 保持维度广播
#
# ---
#
# ## **提交要求**
# 1. **代码**：每个任务的完整实现，附性能对比结果。
# 2. **分析**：
#    - 解释矩阵乘法不同方法的性能差异原因。
#    - 说明金融数据分析中向量化的重要性。
# 3. **扩展思考**：
#    - 如何用 NumPy 实现蒙特卡洛模拟股票价格？
#    - 什么情况下该用 `order='F'` 的内存布局？
