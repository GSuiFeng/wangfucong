# ============================================================
# Pandas 课堂作业：电商订单经营分析挑战
# 作者：王福聪  学号：2025113927
# ============================================================

import numpy as np
import pandas as pd

# 显示设置：显示所有列，金额保留两位小数
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

# ---------- 数据准备 ----------
orders = pd.DataFrame({
    'order_id': [f'O{number}' for number in range(1001, 1019)],
    'region': ['华东','华北','华南','华东','西南','华北','华南','华东','西南','华北','华东','华南','西南','华东','华北','华南','华东','西南'],
    'product': ['机械键盘','无线鼠标','显示器','扩展坞','机械键盘','显示器','无线鼠标','显示器','扩展坞','机械键盘','无线鼠标','扩展坞','显示器','机械键盘','扩展坞','显示器','无线鼠标','机械键盘'],
    'category': ['外设','外设','显示设备','配件','外设','显示设备','外设','显示设备','配件','外设','外设','配件','显示设备','外设','配件','显示设备','外设','外设'],
    'quantity': [2,3,1,4,5,2,6,1,3,2,8,2,1,3,5,2,4,6],
    'unit_price': [289,129,1299,399,289,1299,129,1299,399,289,129,399,1299,289,399,1299,129,289],
    'member_level': ['金卡','普通','银卡','金卡','银卡','普通','金卡','银卡','普通','金卡','银卡','金卡','普通','银卡','金卡','金卡','普通','银卡'],
    'coupon_rate': [0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.00,0.08,0.10,0.05,0.00,0.12,0.05,0.08,0.00,0.10],
    'salesperson': ['小林','小周','小陈','小林','小赵','小周','小陈','小林','小赵','小周','小林','小陈','小赵','小林','小周','小陈','小林','小赵']
})


# ============================================================
# 任务 1：快速理解数据
# ============================================================
print("=" * 60)
print("任务 1：快速理解数据")
print("=" * 60)

# 1.1 行数、列数、列名
print("\n--- 1.1 基本信息 ---")
print(f"行数: {orders.shape[0]}")          # shape[0] = 行数
print(f"列数: {orders.shape[1]}")          # shape[1] = 列数
print(f"列名: {list(orders.columns)}")     # columns 返回所有列名
# 解释：订单表共 18 行 9 列，列名涵盖订单号、地区、商品等信息。

# 1.2 取单列和多列
print("\n--- 1.2 取列 ---")
region_col = orders['region']               # 取单列 -> Series
print(f"单列类型: {type(region_col)}")      # <class 'pandas.core.series.Series'>

subset = orders[['order_id', 'product', 'quantity']]  # 双括号取多列 -> DataFrame
print(f"三列类型: {type(subset)}")          # <class 'pandas.core.frame.DataFrame'>
print(subset)
# 解释：单列是 Series（一维），多列是 DataFrame（二维表格）。

# 1.3 iloc：按位置取
print("\n--- 1.3 iloc：第 4~8 行、前 4 列 ---")
# iloc[起始行:结束行, 起始列:结束列]
# 位置 4~8 是第 5~9 行（索引从 0 开始），iloc 不包含结束位置，所以用 4:9
print(orders.iloc[4:9, 0:4])
# 解释：iloc 按数字位置切片，取出第 5 到第 9 行的前 4 列字段。

# 1.4 loc：按条件取
print("\n--- 1.4 loc：华东订单 ---")
# loc 可以用布尔条件筛选
huadong = orders.loc[orders['region'] == '华东', ['order_id', 'product', 'member_level']]
print(huadong)
# 解释：loc 通过"华东"标签筛选出行，并只保留三列关键信息。

# 1.5 loc 为什么更推荐？
print("\n--- 1.5 loc 优势 ---")
print("""
loc 更推荐的原因：
1. 稳定：loc 基于标签名，即使表增删行列，只要列名不变，代码依然正确；
   iloc 基于数字位置，插入或删除行/列后位置会变，代码容易出错。
2. 可读：loc[orders['region']=='华东', 'order_id'] 一看就懂，
   iloc[0:8, 3] 完全不知道取了啥。
3. 灵活：loc 支持布尔条件、标签切片、标签列表，iloc 只能按数字。
""")


# ============================================================
# 任务 2：构造订单结算指标
# ============================================================
print("\n" + "=" * 60)
print("任务 2：构造订单结算指标")
print("=" * 60)

# 用 assign 一次性新增 5 列，全部向量化计算
analysis = orders.assign(
    # ① 毛金额 = 数量 × 单价（向量化：整列直接相乘）
    gross_amount = orders['quantity'] * orders['unit_price'],

    # ② 会员折扣：np.where 嵌套判断（金卡10%、银卡5%、普通0%）
    member_discount = np.where(
        orders['member_level'] == '金卡', 0.10,
        np.where(orders['member_level'] == '银卡', 0.05, 0.00)
    ),

    # ③ 应付金额 = 毛金额 × (1-会员折扣) × (1-优惠券折扣)
    payable_amount = (
        orders['quantity'] * orders['unit_price']
        * (1 - np.where(orders['member_level'] == '金卡', 0.10,
                        np.where(orders['member_level'] == '银卡', 0.05, 0.00)))
        * (1 - orders['coupon_rate'])
    ),

    # ④ 运费：payable_amount >= 1000 免运费，否则 20
    shipping_fee = np.where(
        (orders['quantity'] * orders['unit_price']
         * (1 - np.where(orders['member_level'] == '金卡', 0.10,
                         np.where(orders['member_level'] == '银卡', 0.05, 0.00)))
         * (1 - orders['coupon_rate'])) >= 1000,
        0, 20
    )
)

# ⑤ 最终金额 = 应付金额 + 运费（在 analysis 基础上再 assign）
analysis = analysis.assign(
    final_amount = analysis['payable_amount'] + analysis['shipping_fee']
)

# 金额保留两位小数
money_cols = ['gross_amount', 'payable_amount', 'shipping_fee', 'final_amount', 'member_discount']
analysis[money_cols] = analysis[money_cols].round(2)

# 展示前 8 行相关字段
print("\n前 8 行结算指标：")
display_cols = ['order_id', 'region', 'product', 'quantity', 'unit_price',
                'member_level', 'coupon_rate', 'member_discount',
                'gross_amount', 'payable_amount', 'shipping_fee', 'final_amount']
print(analysis[display_cols].head(8))
# 解释：向量化计算一次性算出所有订单的结算金额，会员折扣通过 np.where 根据等级赋值。


# ============================================================
# 任务 3：复杂条件筛选
# ============================================================
print("\n" + "=" * 60)
print("任务 3：复杂条件筛选")
print("=" * 60)

# 分别定义 3 个布尔条件（每个都是 True/False 的 Series）
cond1 = analysis['region'].isin(['华东', '华南'])   # 地区为华东或华南
cond2 = analysis['final_amount'] >= 700              # final_amount 不低于 700
cond3 = (analysis['quantity'] >= 2) | (analysis['member_level'] == '金卡')  # 数量≥2 或 金卡会员

# 组合掩码：3 个条件全部满足
mask = cond1 & cond2 & cond3

# 筛选 + 选列 + 排序
key_orders = analysis.loc[mask, ['order_id', 'region', 'product',
                                  'quantity', 'member_level', 'final_amount']]
key_orders = key_orders.sort_values('final_amount', ascending=False)

print(key_orders)
# 解释：筛选出华东/华南地区中 final_amount ≥ 700 且满足数量或会员条件的高价值订单。

print("""
---
关于 & 和 | 两侧加括号的原因：

Python 中运算符优先级：比较运算符（> < ==） > 按位运算符（& |）

如果不加括号：
  orders['quantity'] >= 2 | orders['member_level'] == '金卡'
Python 会先算 2 | orders['member_level']，导致类型错误。

加了括号：
  (orders['quantity'] >= 2) | (orders['member_level'] == '金卡')
先算两个布尔条件得到 True/False Series，再用 | 做按位或运算。
所以括号是为了确保条件先求值，再组合。
""")


# ============================================================
# 任务 4：封装可复用处理函数
# ============================================================
print("=" * 60)
print("任务 4：封装可复用处理函数")
print("=" * 60)

def add_order_level(df):
    """根据 final_amount 新增 order_level 列，不修改传入表"""
    return df.assign(
        order_level=np.where(
            df['final_amount'] >= 2000,
            '战略订单',
            np.where(
                df['final_amount'] >= 1000,
                '重点订单',
                '普通订单'
            )
        )
    )

# 用 pipe 调用
leveled_orders = analysis.pipe(add_order_level)

# 输出各等级订单数
print("\n各等级订单数：")
print(leveled_orders['order_level'].value_counts())
# 解释：嵌套 np.where 实现三级判断，pipe 将表传入函数，返回带 order_level 的新表。


# ============================================================
# 任务 5：一条链完成经营汇总
# ============================================================
print("\n" + "=" * 60)
print("任务 5：一条链完成经营汇总")
print("=" * 60)

region_report = (
    analysis
    .pipe(add_order_level)                           # ① 添加订单等级
    .query('final_amount >= 500')                    # ② 只保留 final_amount >= 500
    .groupby(['region', 'order_level'])              # ③ 按地区和订单等级分组
    .agg(                                             # ④ 计算 4 个指标
        order_count=('order_id', 'count'),            # 订单数
        quantity_sum=('quantity', 'sum'),             # 商品件数合计
        revenue_sum=('final_amount', 'sum'),          # 金额合计
        revenue_mean=('final_amount', 'mean')         # 平均金额
    )
    .sort_values('revenue_sum', ascending=False)      # ⑤ 按金额合计降序
)

print(region_report)
# 解释：一条方法链从原始表到分组汇总报告，不创建中间 DataFrame，代码清晰可读。


# ============================================================
# 任务 6：经营诊断与表达
# ============================================================
print("\n" + "=" * 60)
print("任务 6：经营诊断与表达")
print("=" * 60)

# 6.1 哪位销售人员最终成交金额最高？
sales_rank = analysis.groupby('salesperson')['final_amount'].sum().sort_values(ascending=False)
top_salesperson = sales_rank.index[0]          # 第一名姓名
top_total = round(sales_rank.iloc[0], 2)       # 第一名总金额

print(f"\n6.1 成交金额最高: {top_salesperson}，总成交 {top_total:.2f} 元")

# 6.2 该销售人员成交金额最高的地区
top_person_data = analysis[analysis['salesperson'] == top_salesperson]
region_rank = top_person_data.groupby('region')['final_amount'].sum().sort_values(ascending=False)
top_region = region_rank.index[0]
top_region_amount = round(region_rank.iloc[0], 2)

print(f"6.2 核心地区: {top_region}，该地区成交 {top_region_amount:.2f} 元")

# 6.3 该地区金额占比
region_ratio = (top_region_amount / top_total) * 100

print(f"6.3 地区贡献率: {region_ratio:.1f}%")

# 一句话业务结论
print(f"\n业务结论：{top_salesperson}以{top_total:.2f}元位居销冠，"
      f"其中{top_region}占比{region_ratio:.1f}%，是该销售人员的核心战场，"
      f"建议继续深耕{top_region}市场并复制成功经验至其他区域。")
