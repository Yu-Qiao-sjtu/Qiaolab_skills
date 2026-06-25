# Basic vs Clinical Classification for Biomedical Terms

## 方法论
用关键词规则将每个术语归入 basic / clinical / both：
- **基础关键词**：分子通路、神经递质、受体、离子通道、突触、脑区、动物模型、电生理、细胞因子、免疫细胞、基因表达、蛋白、氧化应激、胶质细胞、光遗传、膜片钳、钙成像、转录组、蛋白组、EEG 频段、局部场电位等
- **临床关键词**：patient, trial, sham, randomized, clinical, outcome, adverse event, postoperative, surgery, depression, epilepsy, stroke, scale, score, questionnaire, diagnosis, treatment, therapy, dose, efficacy, safety, follow-up, hospitalization, mortality, quality of life 等
- **交叉**：同时命中基础+临床
- **未匹配默认归入基础研究**（保守 baseline）

## 验证
- 对所有未匹配术语逐个分析原因
- 通用描述词（如 "significant difference""systematic review"）归入临床
- 纯方法学词需逐个判断
- 最终所有术语全部归入三类之一

## 项目组织规范
```
project/
├── README.md              # 完整项目文档（方法、发现、引用）
├── data/
│   ├── raw/               # 原始数据（不可修改）
│   ├── processed/         # 过滤后 + 分类数据
│   └── clustering/        # UMAP/HDBSCAN 结果
├── figures/               # 终稿论文图（PNG 1200dpi + PDF）
├── reports/               # 文字报告
├── scripts/
│   ├── pipeline/          # 核心分析步骤（按 1-6 编号）
│   ├── figures/           # 图表生成脚本
│   └── utils/             # 调试工具
└── archive/               # 废弃旧版图
```

## 关键决策
- 先去掉 taVNS 同义词再分类（避免检索词污染各类）
- 突发术语定义：此前 23 年（2002-2024）从未出现
- 上升信号：突发基础上还要求 2026 > 2025
