import numpy as np
import matplotlib.pyplot as plt
# 1
# NumPy数组基础操作
# 任务描述：
# 创建不同维度的数组（1D、2D、3D）
# 实现数组的索引、切片、形状变换操作
# 编写函数实现矩阵的基本运算（加法、乘法、转置）
# 使用NumPy生成随机数据并进行统计分析
# 要求：展示数组创建、索引切片、形状操作的熟练掌握

#创建数组
arr1=np.array([1,2])#一维
arr2=np.array([[1,2,3],[3,4,5]])#二维
arr3=np.array([[[1,2],[3,4]],[[5,6],[7,8]]])#三维
#索引、切片、形状改变
print(arr1[0])#索引
print(arr2[0,:])
print(arr3[0,:,0])#切片

print(np.shape(arr2))
print(np.reshape(arr2,(3,2)))#改变形状

np.random.seed(10)
arrA=np.random.randint(0,10,size=(2,3))
arrB=np.random.randint(0,10,size=(2,3))
print(np.add(arrA,arrB))#加法
print(arrA*arrB)#乘法
print(arrA@arrB.T)#矩阵乘法
arr_A=arrA.T# arr_A=arrA.T#转置

sumH_A=np.sum(arrA,axis=1)#行求和
print(sumH_A)
sumL_A=np.sum(arrA,axis=0)#列求和


# 2
# 金融数据分析实战
# 任务描述：
# 分析股票价格数据，计算收益率、波动率等指标
# 使用NumPy实现移动平均线计算
# 进行投资组合风险分析（方差、协方差计算）
# 可视化展示分析结果
# 数据来源：Yahoo Finance公开股票数据 或 使用NumPy生成模拟股票价格数据

price = 100 * np.exp(np.cumsum(np.random.normal(0.0005, 0.02, 100)))
price = price / price[0] * 100

returns = np.diff(np.log(price))
volatility = np.std(returns) * np.sqrt(252)
print(f"模拟股价数据形状: {price.shape}")
print(f"对数收益率 (前5个): {returns[:5]}")
print(f"年化波动率: {volatility:.4f}")

def calculate_ma_convolve(p, window):
    """使用 np.convolve 计算均线"""
    weights = np.ones(window) / window
    return np.convolve(p, weights, mode='valid')

def calculate_ma_cumsum(p, window):
    """使用 np.cumsum 计算均线"""
    cum_sum = np.cumsum(np.concatenate(([0], p)))
    return (cum_sum[window:] - cum_sum[:-window]) / window

# 计算 5日 和 20日 均线
ma5_conv = calculate_ma_convolve(price, 5)
ma20_conv = calculate_ma_convolve(price, 20)

# 对齐原始数据长度 (可选，为了画图好看)
ma5_full = np.concatenate((np.full(4, np.nan), ma5_conv))
ma20_full = np.concatenate((np.full(19, np.nan), ma20_conv))

# ==========================================
# 4. 投资组合风险分析 (假设有两只股票)
# ==========================================
# 生成第二只股票的模拟数据
price2 = 100 * np.exp(np.cumsum(np.random.normal(0.0006, 0.015, 100)))

# 计算两只股票的收益率
ret1 = np.diff(np.log(price))
ret2 = np.diff(np.log(price2))

# 合并收益率以便计算协方差
returns_matrix = np.vstack([ret1, ret2])

# 计算均值 (期望收益率)
mean_ret = np.mean(returns_matrix, axis=1)
# 计算协方差矩阵
cov_matrix = np.cov(returns_matrix)

print(f"资产1平均日收益率: {mean_ret[0]:.6f}")
print(f"资产2平均日收益率: {mean_ret[1]:.6f}")
print(f"协方差矩阵:{cov_matrix}")
plt.figure(figsize=(14, 10))

# 图1：价格与均线
plt.subplot(2, 1, 1)
plt.plot(price, label='Stock Price', color='black', alpha=0.7)
plt.plot(ma5_full, label='MA5 (Convolve)', color='blue', linestyle='--')
plt.plot(ma20_full, label='MA20 (Convolve)', color='red', linestyle='-.')
plt.title('Stock Price and Moving Averages')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

# 图2：收益率分布直方图
plt.subplot(2, 1, 2)
plt.hist(returns, bins=20, color='green', alpha=0.6, edgecolor='black')
plt.axvline(x=np.mean(returns), color='red', linestyle='--', label=f'Mean: {np.mean(returns):.4f}')
plt.title('Log Returns Distribution')
plt.xlabel('Returns')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.show()