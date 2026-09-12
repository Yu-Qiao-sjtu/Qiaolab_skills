---
name: semiconductor-chip-insight
description: 用已收录的半导体访谈框架分析用户给定的软硬件协同、架构权衡和工程创新问题。用于方法学习与方案比较，不用于实时供应链调查、股票建议或芯片规格认证。
compatibility: Wisp Science 1.11.0 author-declared; requires supplied material and text reasoning. Optional file or vision tools depend on the task.
wisp:
  schema_version: 1
  domains: ["general"]
  research_stages: ["analysis", "validation"]
  roles: ["analyst", "critic"]
  evidence_types: ["literature", "computational"]
  outputs: ["risk-map", "validation-plan"]
  side_effects: project_write
---

# 芯片架构与工程思维

## 职责
围绕用户场景分析软硬件协同、分层约束和工程方案的权衡。

## 何时使用
- 正例：结合软硬件协同思路，比较这个加速器方案的几个设计取舍。
- 反例：推荐现在最值得买的半导体股票。

## 输入
具体工程问题、方案或访谈解读目标；可选：指标、预算、工艺与约束。

## 交付物
约束与权衡分析、访谈来源、条件性建议及待验证指标。 默认在对话中交付；只有用户要求文件时，才写入其指定的项目路径，未指定文件名时使用项目内清晰命名的 Markdown 文件并报告路径。

## 不适用范围
不提供未经查证的最新工艺、产品规格或商业预测；不把类比当作硬件测量或投资依据。

## 依赖与能力边界
必需：能理解中文的文本模型，以及可读取的输入材料。材料在文件中时需要 Wisp 可用的 `read` 或等效读取工具。无必需 MCP、Python/R 包、CLI、网络或特定操作系统。

可选：用户要求文件时使用可用的 `write` 工具；否则在对话中交付。缺少必需材料或工具时说明具体缺项并暂停依赖它的步骤，其余可独立完成的部分可继续。

## 工作流程
1. 读取 [工程方法模块](references/methods.md)，需要访谈背景时读取 [材料概览](references/BOOK_OVERVIEW.md)。
2. 明确优化目标和不可改变的约束，分开讨论算法、系统、架构和工艺层面。
3. 指出权衡依赖的测量、实验或规格；未提供数字时保持定性，不编造性能提升。

## 权限与完成检查
技能加载只提供说明，不自动执行脚本、安装依赖或授权操作。默认只读取任务相关材料；文件写入遵循用户当前请求与宿主审批。已有明确授权不重复询问；未回答的问题不是授权。不联网检索、上传、发送消息或调用外部服务来补齐证据。

如果生成文件，确认文件真实存在、可读取、内容完整，再报告路径。分别说明材料核对、格式检查、图像判读和实际计算哪些完成、哪些未做；不得把格式通过或访谈类比当作科学有效性证明。安装整个目录并按包内相对路径读取参考材料；没有运行时侧载脚本。

来源、许可与兼容状态见 [来源说明](references/provenance.md)。
