# Qiaolab Skills · Wisp Science

面向 Wisp Science 的科研技能集合，统一采用它的技能结构、触发边界、依赖声明和包资源要求。

| 技能 | 用途 |
| --- | --- |
| [ai4asking](skills/ai4asking/SKILL.md) | 有依据的追问 |
| [ai-insider-research](skills/ai-insider-research/SKILL.md) | AI 研究访谈方法论 |
| [ai-paradigm-shift](skills/ai-paradigm-shift/SKILL.md) | Agent 范式与系统设计思考 |
| [research-thinking-insights](skills/research-thinking-insights/SKILL.md) | 科研问题定义与排错 |
| [semiconductor-chip-insight](skills/semiconductor-chip-insight/SKILL.md) | 芯片架构与工程思维 |
| [yonghegong-wish](skills/yonghegong-wish/SKILL.md) | 目标与指令精确表达 |
| [paper-deconstruction](skills/paper-deconstruction/SKILL.md) | 论文证据与因果逻辑拆解 |

## 安装

在 Wisp Science **Settings → Skills** 中导入 [技能目录](https://github.com/Yu-Qiao-sjtu/Qiaolab_skills/tree/master/skills)，选择需要的技能。也可以克隆仓库后，把完整的 `skills/<name>/` 目录安装到研究项目的 `.wisp/skills/`。

```sh
python scripts/install_skill.py --skill paper-deconstruction --project /path/to/research-project
```

不能只复制 SKILL.md；参考材料与许可证必须随包保留。已有同名包不会被覆盖，更新前先备份本地修改。原 `AI4asking` 统一命名为 `ai4asking`。根目录其他平台规则文件为历史适配，Wisp 只使用技能包。

## 规范和验证

- [Wisp 规范与完整安装说明](docs/WISP-STANDARD.md)
- [开发规则](AGENTS.md)
- [兼容性验证记录](docs/VALIDATION.md)
- [目录元数据](community-skills/index.json)：符合上游目录结构，尚未提交到 Wisp 官方社区索引。
- [合并来源](MIGRATION.md)：Wisp_skills 的五个技能及 Pro.-Paper 分析方法已在此维护。

私有实验记录技能仍在原私有仓库，采用同一规范但不加入公开索引。目标兼容 Wisp Science 1.11.0；结构验证与真实模型任务验证分别报告。
