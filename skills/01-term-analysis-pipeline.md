# Term Entropy Analysis Pipeline

## 适用场景
- 输入：`term-entropy.csv`，格式为 TERM | Entropy | 2002 | 2003 | ... | 2026 | Subtotal
- 每行一个术语，25 列逐年频次 + 熵值
- 输出需求：过滤去噪 → 分类 → 热点分析 → 突发检测 → 演化趋势

## Step 1: 数据清洗
- 去除检索词/主题词：taVNS 全称、缩写、同义词、变体（taVNS, tVNS, aVNS, ta-VNS, transcutaneous auricular vagus nerve stimulation 等，含拼写变体）
- 去除功能词/虚词/介词（如 "a b s t r a c t", "in fl ammatory biomarkers" 等）
- 大小写不敏感匹配
- 输出：`term-entropy-filtered.csv`

## Step 2: 基础 vs 临床分类
- 用关键词规则将每个术语归入 basic / clinical / both
- 基础关键词：分子、细胞、通路、受体、基因、蛋白、动物模型、脑区、神经解剖、电生理、信号通路、突触、神经递质、离子通道、酶、氧化应激、炎症因子、免疫细胞、胶质细胞、microRNA、Western blot、免疫组化、PCR、ELISA、神经元、轴突、树突、突触可塑性、LTP、LTD、脑片、膜片钳、钙成像、光遗传、化学遗传、病毒示踪、顺行/逆行追踪、EEG频段、局部场电位、单细胞测序、转录组、蛋白组、代谢组、生物信息学、计算模型等
- 临床关键词：patient, trial, sham, randomized, clinical, outcome, adverse event, postoperative, surgery, depression, anxiety, epilepsy, stroke, pain, rehabilitation, scale, score, questionnaire, diagnosis, treatment, therapy, dose, efficacy, safety, tolerability, follow-up, hospitalization, mortality, quality of life, 各类量表名等
- 交叉（both）：同时满足基础+临床关键词
- 未匹配的默认归入基础研究（baseline 假设）
- 输出：`terms-classified.csv`（新增 Category 列）

## Step 3: 三类分析
### 3a. 2025-2026 热点
- 按 Total_2025_2026 降序排列
- 分别输出基础 Top N 和临床 Top N

### 3b. 突发术语（Burst Terms）
- 条件：2002-2024 年所有列频次之和 = 0，且 2025+2026 > 0
- 按总频次降序排列
- 输出：`burst-terms-full.csv`

### 3c. 2022-2026 演化
- 逐年活跃术语数统计
- 增长最快：Δ = mean(2025,2026) − mean(2022,2023,2024)
- 衰退最快：负 Δ 最大
- 按子类分别统计

## 关键 Python 模式
```python
import pandas as pd
df = pd.read_csv('term-entropy.csv')
years = [str(y) for y in range(2002, 2027)]
# 过滤
mask_remove = df['TERM'].str.lower().apply(lambda x: any(pattern in x for pattern in remove_patterns))
df_filtered = df[~mask_remove]
# 突发检测
df_filtered['pre_2025_sum'] = df_filtered[[str(y) for y in range(2002, 2025)]].sum(axis=1)
burst = df_filtered[(df_filtered['pre_2025_sum'] == 0) & (df_filtered[['2025','2026']].sum(axis=1) > 0)]
```
