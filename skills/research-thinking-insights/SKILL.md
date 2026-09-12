---
name: research-thinking-insights
description: 将跨领域访谈中的问题定义、系统排错和跨层思考方法用于用户给定的科研计划或失败结果。适用于课题审视与排错方案设计，不代替数据分析执行、文献检索或统计检验。
compatibility: Wisp Science 1.11.0 author-declared; requires supplied material and text reasoning. Optional file or vision tools depend on the task.
wisp:
  schema_version: 1
  domains: ["general", "scientific-literature"]
  research_stages: ["hypothesis", "validation"]
  roles: ["planner", "critic"]
  evidence_types: ["literature", "project-data", "experimental"]
  outputs: ["hypothesis-card", "validation-plan"]
  side_effects: project_write
---

# 科研问题定义与排错

## 职责
找出科研计划最关键的未知与可区分解释的下一步，帮助建立有反馈的研究迭代。

## 何时使用
- 正例：这个实验连续三次没效果，帮我按问题定义和系统排错梳理下一步。
- 反例：读取表达矩阵并实际运行差异表达分析。

## 输入
研究目标、已有证据或失败现象；可选：实验条件、资源和时间约束。

## 交付物
问题定义、证据与假设的区分、排错优先级和下一步验证计划。 默认在对话中交付；只有用户要求文件时，才写入其指定的项目路径，未指定文件名时使用项目内清晰命名的 Markdown 文件并报告路径。

## 不适用范围
不凭摘要式描述诊断实际实验根因；不编造对照结果，也不自动执行实验或计算。

## 依赖与能力边界
必需：能理解中文的文本模型，以及可读取的输入材料。材料在文件中时需要 Wisp 可用的 `read` 或等效读取工具。无必需 MCP、Python/R 包、CLI、网络或特定操作系统。

可选：用户要求文件时使用可用的 `write` 工具；否则在对话中交付。缺少必需材料或工具时说明具体缺项并暂停依赖它的步骤，其余可独立完成的部分可继续。

## 工作流程
1. 按当前问题读取 [科研方法模块](references/methods.md)；跨访谈出处见 [材料概览](references/BOOK_OVERVIEW.md)，无需安装其他技能。
2. 将观察、解释和待验证假设分开；确认研究目标可以用什么证据判断，而非只追随热门技术。
3. 优先选择能区分竞争解释且成本可控的检查；说明停止条件和结果如何改变下一步。

## 权限与完成检查
技能加载只提供说明，不自动执行脚本、安装依赖或授权操作。默认只读取任务相关材料；文件写入遵循用户当前请求与宿主审批。已有明确授权不重复询问；未回答的问题不是授权。不联网检索、上传、发送消息或调用外部服务来补齐证据。

如果生成文件，确认文件真实存在、可读取、内容完整，再报告路径。分别说明材料核对、格式检查、图像判读和实际计算哪些完成、哪些未做；不得把格式通过或访谈类比当作科学有效性证明。安装整个目录并按包内相对路径读取参考材料；没有运行时侧载脚本。

来源、许可与兼容状态见 [来源说明](references/provenance.md)。
