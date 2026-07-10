import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: f'{x:.2f}')

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

"""任务一"""
print(f"行数: {orders.shape[0]}")
print(f"列数: {orders.shape[1]}")

print(f"region列{orders['region']}")
subset = orders[["order_id","product","quantity"]]
print(subset)

print(orders.iloc[4:9,0:4])

print(orders.loc[orders["region"] == "华东",["order_id","product","member_level"]])


"""任务二"""


analysis = orders.assign(
    gross_amount = orders["quantity"] * orders["unit_price"],

    member_discount = np.where(orders["member_level"] == "金卡", 0.1 ,
                               np.where(orders["member_level"] == "银卡", 0.05,0)),
)

analysis = analysis.assign(
    payable_amount = analysis["gross_amount"] * (1-analysis["member_discount"]) * (1-analysis["coupon_rate"])
)

analysis = analysis.assign(
    shipping_fee = np.where(analysis["payable_amount"] >= 1000, 0 ,20),
)

analysis = analysis.assign(
    final_amount = analysis["shipping_fee"]+analysis["payable_amount"]
)

analysis["final_amount"] = analysis["final_amount"].round(2)

print(analysis.head(8))


"""任务三"""

request1 = (analysis["region"] == "华东") | (analysis["region"] == "华南")
request2 = analysis["final_amount"] >= 700
request3 = (analysis["quantity"] >= 2) | (analysis["member_level"] == "金卡")

request_all = request1 & request2 & request3

_analysis = analysis.loc[request_all,["order_id","region","product","quantity","member_level","final_amount"]]
_analysis = _analysis.sort_values("final_amount", ascending=False)

print(_analysis)
















"""任务四"""

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
