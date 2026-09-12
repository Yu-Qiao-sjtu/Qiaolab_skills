---
name: ai-insider-research
description: 基于已收录的 AI 研究访谈方法论，分析训练研究的问题定义、消融和组织实践。用于解读该访谈或将其方法迁移到给定研究问题，不用于查询最新模型规格、公司人事或行情。
compatibility: Wisp Science 1.11.0 author-declared; requires supplied material and text reasoning. Optional file or vision tools depend on the task.
wisp:
  schema_version: 1
  domains: ["general"]
  research_stages: ["analysis", "hypothesis", "validation"]
  roles: ["analyst", "planner"]
  evidence_types: ["literature", "computational"]
  outputs: ["research-design", "validation-plan"]
  side_effects: project_write
---

# AI 研究访谈方法论

## 职责
把访谈中的研究经验转成适用于当前问题的判断维度，并保留来源与时代边界。

## 何时使用
- 正例：用姚顺宇访谈里的问题定义与消融思路，审视我这个模型实验计划。
- 反例：现在最新模型的价格和上下文长度是多少？

## 输入
访谈解读问题，或用户的研究问题和约束；可选：新的原始材料。

## 交付物
与问题相关的方法、来源定位、适用条件和可检验的下一步。 默认在对话中交付；只有用户要求文件时，才写入其指定的项目路径，未指定文件名时使用项目内清晰命名的 Markdown 文件并报告路径。

## 不适用范围
不把访谈观点当作当前行业事实；不自行训练模型、配置 GPU、联网调用 API 或承诺研究效果。

## 依赖与能力边界
必需：能理解中文的文本模型，以及可读取的输入材料。材料在文件中时需要 Wisp 可用的 `read` 或等效读取工具。无必需 MCP、Python/R 包、CLI、网络或特定操作系统。

可选：用户要求文件时使用可用的 `write` 工具；否则在对话中交付。缺少必需材料或工具时说明具体缺项并暂停依赖它的步骤，其余可独立完成的部分可继续。

## 工作流程
1. 根据问题读取 [方法模块](references/methods.md)，需要来源背景时读取 [材料概览](references/BOOK_OVERVIEW.md)。
2. 选取直接相关的研究原则，区分受访者观点、已有例子和本次迁移推断。
3. 列出适用前提、最小验证实验与可能失败的条件；未提供数据时只设计验证，不虚构执行结果。

## 权限与完成检查
技能加载只提供说明，不自动执行脚本、安装依赖或授权操作。默认只读取任务相关材料；文件写入遵循用户当前请求与宿主审批。已有明确授权不重复询问；未回答的问题不是授权。不联网检索、上传、发送消息或调用外部服务来补齐证据。

如果生成文件，确认文件真实存在、可读取、内容完整，再报告路径。分别说明材料核对、格式检查、图像判读和实际计算哪些完成、哪些未做；不得把格式通过或访谈类比当作科学有效性证明。安装整个目录并按包内相对路径读取参考材料；没有运行时侧载脚本。

来源、许可与兼容状态见 [来源说明](references/provenance.md)。
