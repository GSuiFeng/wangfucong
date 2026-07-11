# ============================================================
# 作业 2：空气质量数据分析与可视化（Beijing PM2.5 数据集）
# 作者：王福聪  学号：2025113927
# 注意：本环境 pandas resample 有兼容问题，用 groupby 替代
# ============================================================

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互后端
import matplotlib.pyplot as plt

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
pd.set_option('display.max_columns', None)

print("=" * 60)
print("作业 2：空气质量数据分析与可视化")
print("=" * 60)

# ---------- 步骤 1：加载和初步清洗 ----------
print("\n【步骤 1】加载数据")
df = pd.read_csv('PM2_5.csv')

# 列名统一为英文小写
df.columns = ['no', 'year', 'month', 'day', 'hour', 'pm2_5', 'dew_point',
              'temperature', 'pressure', 'wind_dir', 'wind_speed',
              'snow_hours', 'rain_hours']
df = df.drop(columns=['no'])  # 移除无用的行号列

print(f"数据规模：{df.shape[0]} 行 × {df.shape[1]} 列")
print(f"时间范围：{df['year'].min()}-{df['year'].max()}")

# 取最后 2 年数据，减少数据量同时保持分析完整
df = df[df['year'] >= 2013].copy()
print(f"取 2013-2014 子集后：{df.shape[0]} 行")

# 处理 pm2_5 缺失值（向前填充：用上一个有效值填充）
df['pm2_5'] = df['pm2_5'].ffill()
print(f"缺失值处理完毕，前 5 行预览：")
print(df.head())


# ============================================================
# 步骤 2：统计指标计算
# ============================================================
print("\n" + "=" * 60)
print("【步骤 2】污染物统计指标")

stats = df['pm2_5'].describe()
print(f"PM2.5 统计指标：")
print(f"  均值={stats['mean']:.2f}  中位数={df['pm2_5'].median():.2f}")
print(f"  标准差={stats['std']:.2f}")
print(f"  最小值={stats['min']:.2f}  最大值={stats['max']:.2f}")

# 各污染物相关性
pollutants = ['pm2_5', 'temperature', 'dew_point', 'pressure', 'wind_speed']
corr_matrix = df[pollutants].corr()
print(f"\n污染物相关性矩阵：\n{corr_matrix.round(2)}")

top_corr = corr_matrix['pm2_5'].drop('pm2_5').abs().sort_values(ascending=False)
print(f"\nPM2.5 与其他因子相关性（绝对值排名）：")
for col in top_corr.index:
    print(f"  {col}: {corr_matrix.loc['pm2_5', col]:.2f}")


# ============================================================
# 步骤 3：时间序列分析（用 groupby 替代 resample）
# ============================================================
print("\n" + "=" * 60)
print("【步骤 3】时间序列分析")

# 按日平均：用 groupby 替代 resample('D').mean()
daily = df.groupby(['year', 'month', 'day'])['pm2_5'].mean()
print(f"日平均数据：{len(daily)} 天")

# 近年统计
yearly_mean = df.groupby('year')['pm2_5'].mean()
yearly_max = df.groupby('year')['pm2_5'].max()
yearly_min = df.groupby('year')['pm2_5'].min()
yearly = pd.DataFrame({'年均值': yearly_mean, '年最大值': yearly_max, '年最小值': yearly_min})
print(f"\n逐年 PM2.5 统计：\n{yearly.round(2)}")

# 按月统计（所有年份合并）
monthly_all = df.groupby('month')['pm2_5'].mean()
print(f"\n各月平均 PM2.5（全年）：")
for m, val in monthly_all.items():
    print(f"  {m}月: {val:.2f}")


# ============================================================
# 步骤 4：创建多种图表
# ============================================================
print("\n" + "=" * 60)
print("【步骤 4】创建可视化图表")

# 取最后 90 天的日均值
recent = daily.tail(90)

# ---------- 图 1：PM2.5 日变化折线图 ----------
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(range(len(recent)), recent.values, color='#d9534f', linewidth=1)
ax1.set_title('PM2.5 日变化趋势（近 90 天）', fontsize=13)
ax1.set_ylabel('PM2.5 (μg/m³)')
ax1.set_xlabel('天数（从第 1 天到第 90 天）')
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('pm25_line.png', dpi=150)
plt.close(fig1)
print("✓ 图 1：折线图已保存 → pm25_line.png")

# ---------- 图 2：逐年 PM2.5 均值柱状图 ----------
fig2, ax2 = plt.subplots(figsize=(10, 5))
years = [str(y) for y in yearly.index]
bars = ax2.bar(years, yearly['年均值'],
               color=['#5bc0de', '#337ab7'])
for bar, val in zip(bars, yearly['年均值']):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val:.1f}', ha='center', fontsize=10)
ax2.set_title('逐年 PM2.5 年均值对比', fontsize=13)
ax2.set_ylabel('PM2.5 (μg/m³)')
ax2.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('pm25_bar.png', dpi=150)
plt.close(fig2)
print("✓ 图 2：柱状图已保存 → pm25_bar.png")

# ---------- 图 3：温度与 PM2.5 散点图 ----------
fig3, ax3 = plt.subplots(figsize=(8, 6))
sample = df.sample(n=min(500, len(df)), random_state=42)
scatter = ax3.scatter(sample['temperature'], sample['pm2_5'],
                       c=sample['wind_speed'], cmap='coolwarm',
                       alpha=0.6, s=20)
ax3.set_title('温度与 PM2.5 关系（颜色=风速）', fontsize=13)
ax3.set_xlabel('温度 (°C)')
ax3.set_ylabel('PM2.5 (μg/m³)')
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('风速 (m/s)')
plt.tight_layout()
plt.savefig('pm25_scatter.png', dpi=150)
plt.close(fig3)
print("✓ 图 3：散点图已保存 → pm25_scatter.png")

# ---------- 图 4：污染物相关性热力图 ----------
fig4, ax4 = plt.subplots(figsize=(8, 6))
im = ax4.imshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')

for i in range(len(corr_matrix)):
    for j in range(len(corr_matrix)):
        ax4.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                 ha='center', va='center',
                 color='white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black',
                 fontsize=11)

short_names = ['PM2.5', '温度', '露点', '气压', '风速']
ax4.set_xticks(range(len(short_names)))
ax4.set_xticklabels(short_names, rotation=45, ha='right')
ax4.set_yticks(range(len(short_names)))
ax4.set_yticklabels(short_names)
ax4.set_title('污染物相关性热力图', fontsize=13)
plt.colorbar(im, ax=ax4, label='相关系数')
plt.tight_layout()
plt.savefig('pm25_heatmap.png', dpi=150)
plt.close(fig4)
print("✓ 图 4：热力图已保存 → pm25_heatmap.png")

# ---------- 图 5：PM2.5 月均值季节性变化 ----------
fig5, ax5 = plt.subplots(figsize=(10, 5))
months = ['1月','2月','3月','4月','5月','6月',
          '7月','8月','9月','10月','11月','12月']
month_vals = monthly_all.values
ax5.plot(months, month_vals, marker='o', color='#d9534f',
         linewidth=2, markersize=8)
ax5.fill_between(range(12), month_vals, alpha=0.15, color='#d9534f')
ax5.set_title('PM2.5 月均值——季节性变化规律', fontsize=13)
ax5.set_ylabel('PM2.5 (μg/m³)')
ax5.grid(True, alpha=0.3)

# 标注最高最低月
max_m = monthly_all.idxmax()
min_m = monthly_all.idxmin()
ax5.annotate(f'{max_m}月最高\n{monthly_all[max_m]:.1f}',
             xy=(max_m-1, monthly_all[max_m]),
             xytext=(max_m-1.5, monthly_all[max_m]+10),
             arrowprops=dict(arrowstyle='->', color='red'), fontsize=9)
ax5.annotate(f'{min_m}月最低\n{monthly_all[min_m]:.1f}',
             xy=(min_m-1, monthly_all[min_m]),
             xytext=(min_m+0.5, monthly_all[min_m]+15),
             arrowprops=dict(arrowstyle='->', color='green'), fontsize=9)

plt.tight_layout()
plt.savefig('pm25_seasonal.png', dpi=150)
plt.close(fig5)
print("✓ 图 5：季节性变化图已保存 → pm25_seasonal.png")

print("\n所有图表已保存到当前目录。")


# ============================================================
# 步骤 5：季节性分析结论
# ============================================================
print("\n" + "=" * 60)
print("【步骤 5】季节性变化规律分析")

y2013 = yearly.loc[2013, '年均值']
y2014 = yearly.loc[2014, '年均值']
trend = '呈下降趋势，空气质量改善' if y2014 < y2013 else '需持续关注'

print(f"""
分析结论：
1. PM2.5 整体趋势：{y2013:.1f} → {y2014:.1f}，{trend}

2. 季节性特征：
   - 高污染月：{max_m}月（均值 {monthly_all[max_m]:.1f}），冬季采暖+静稳天气导致
   - 低污染月：{min_m}月（均值 {monthly_all[min_m]:.1f}），夏季扩散条件好

3. 相关因子：
   - 温度与 PM2.5 相关系数 {corr_matrix.loc['pm2_5', 'temperature']:.2f}（负相关）
   - 气压与 PM2.5 相关系数 {corr_matrix.loc['pm2_5', 'pressure']:.2f}（正相关）
   - 说明：低温+高压天气更容易出现 PM2.5 污染

4. 建议：冬季应加强减排措施，夏季是空气质量最好的时期。
""")
