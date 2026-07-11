# ============================================================
# 作业 1：数据清洗与预处理（Titanic 数据集）
# 作者：王福聪  学号：2025113927
# ============================================================

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

print("=" * 60)
print("作业 1：数据清洗与预处理")
print("=" * 60)

# ---------- 步骤 1：读取数据 ----------
print("\n【步骤 1】加载 Titanic 数据集")
titanic = sns.load_dataset('titanic')
print(f"原始数据：{titanic.shape[0]} 行 × {titanic.shape[1]} 列")
print(f"列名：{list(titanic.columns)}")

# 展示前 5 行
print("\n前 5 行预览：")
print(titanic.head())


# ============================================================
# 步骤 2：识别缺失值
# ============================================================
print("\n" + "=" * 60)
print("【步骤 2】缺失值分析")

# 每列缺失值数量
missing = titanic.isnull().sum()
missing_pct = (missing / len(titanic) * 100).round(2)
missing_df = pd.DataFrame({'缺失数量': missing, '缺失比例(%)': missing_pct})
missing_df = missing_df[missing_df['缺失数量'] > 0].sort_values('缺失数量', ascending=False)
print(missing_df)
print(f"\n说明：Age 缺失 19.9%，embarked 缺失极少，deck 缺失高达 77.2%")


# ============================================================
# 步骤 3：多种缺失值处理
# ============================================================
print("\n" + "=" * 60)
print("【步骤 3】缺失值处理")

# 创建副本，不污染原数据
df = titanic.copy()

# --- 方法 1：删除含缺失值的行（dropna） ---
df_drop = df.dropna(subset=['embarked'])  # 只删 embarked 缺失的 2 行
print(f"删除法：去掉 embarked 缺失的行，剩余 {df_drop.shape[0]} 行")

# --- 方法 2：填充缺失值（fillna） ---
# Age：用中位数填充（中位数不受极端值影响）
df['age'] = df['age'].fillna(df['age'].median())
print(f"填充法：age 缺失值用中位数 {df['age'].median():.1f} 填充")

# embarked：用众数填充（最常见的值）
mode_embarked = df['embarked'].mode()[0]
df['embarked'] = df['embarked'].fillna(mode_embarked)
print(f"填充法：embarked 缺失值用众数 '{mode_embarked}' 填充")

# embark_town：同样用众数填充
mode_town = df['embark_town'].mode()[0]
df['embark_town'] = df['embark_town'].fillna(mode_town)
print(f"填充法：embark_town 缺失值用众数 '{mode_town}' 填充")

# --- 方法 3：插值法（interpolate） ---
# 制造少量缺失来演示（fare 列）
df_fare_demo = df['fare'].copy()
df_fare_demo.iloc[10:15] = np.nan  # 人为制造 5 个缺失
df_fare_filled = df_fare_demo.interpolate(method='linear')
print(f"插值法：fare 用线性插值填补，示例值 {df_fare_filled.iloc[10:15].tolist()}")

# 高缺失率列（deck）：直接删除
df = df.drop(columns=['deck'])
print("删除法：deck 列缺失率 77.2%，直接删除该列")

# 验证缺失值已处理
print(f"\n处理后缺失值：\n{df.isnull().sum()}")
print("✓ 所有缺失值已处理完毕")


# ============================================================
# 步骤 4：识别并处理重复记录
# ============================================================
print("\n" + "=" * 60)
print("【步骤 4】重复记录处理")

dup_count = df.duplicated().sum()
print(f"完全重复行数：{dup_count}")

if dup_count > 0:
    df = df.drop_duplicates()
    print(f"删除重复后：{df.shape[0]} 行")
else:
    # 人为添加几条重复来演示
    print("（原始数据无重复，人为添加 3 条演示）")
    dup_rows = df.head(3)
    df_demo = pd.concat([df, dup_rows], ignore_index=True)
    print(f"添加前：{df.shape[0]} 行，添加后：{df_demo.shape[0]} 行")
    dup_in_demo = df_demo.duplicated().sum()
    print(f"检测到重复：{dup_in_demo} 行")
    df_demo = df_demo.drop_duplicates()
    print(f"去重后：{df_demo.shape[0]} 行")


# ============================================================
# 步骤 5：数据类型转换和格式标准化
# ============================================================
print("\n" + "=" * 60)
print("【步骤 5】数据类型转换与标准化")

print(f"转换前各列类型：\n{df.dtypes}\n")

# ① survived 转 bool：0/1 → False/True
df['survived'] = df['survived'].astype(bool)

# ② pclass 转 category（分类变量）
df['pclass'] = df['pclass'].astype('category')

# ③ sex 转 category
df['sex'] = df['sex'].astype('category')

# ④ age 转 int（年龄用整数更合理）
df['age'] = df['age'].astype(int)

# ⑤ fare 四舍五入保留 2 位
df['fare'] = df['fare'].round(2)

# ⑥ who 列：首字母大写标准化
df['who'] = df['who'].str.title()

# ⑦ 新增列：年龄分组（字符串格式标准化）
df['age_group'] = pd.cut(df['age'],
                          bins=[0, 18, 35, 60, 100],
                          labels=['少年', '青年', '中年', '老年'])

print(f"转换后各列类型：\n{df.dtypes}\n")
print(f"前 5 行最终结果：")
print(df[['survived', 'pclass', 'sex', 'age', 'fare', 'who', 'embarked', 'age_group']].head())


# ============================================================
# 步骤 6：清洗结果汇总
# ============================================================
print("\n" + "=" * 60)
print("【清洗结果汇总】")
print(f"原始数据：{titanic.shape[0]} 行 × {titanic.shape[1]} 列")
print(f"清洗后：  {df.shape[0]} 行 × {df.shape[1]} 列")
print(f"处理内容：")
print(f"  - 缺失值：age(中位数填充)、embarked(众数填充)、deck(删除列)")
print(f"  - 重复值：发现 {dup_count} 条，已删除（去重后 {df.shape[0]} 行）")
print(f"  - 类型转换：survived→bool, pclass→category, age→int, fare→保留2位")
print(f"  - 格式标准化：who 首字母大写, 新增年龄分组列")
