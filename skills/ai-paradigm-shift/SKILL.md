---
name: ai-paradigm-shift
description: 使用已收录的 Agent 访谈方法论，分析用户给定的 Chat 到 Agent 工作流、反馈回路和组织协作设计。用于方法比较与方案评审，不用于预测 AGI 日期、查询最新公司动态或直接部署 Agent。
compatibility: Wisp Science 1.11.0 author-declared; requires supplied material and text reasoning. Optional file or vision tools depend on the task.
wisp:
  schema_version: 1
  domains: ["general"]
  research_stages: ["analysis", "hypothesis", "validation"]
  roles: ["analyst", "planner"]
  evidence_types: ["literature", "computational"]
  outputs: ["research-design", "risk-map"]
  side_effects: project_write
---

# Agent 范式与系统设计思考

## 职责
帮助评估一个具体工作流何时需要 Agent、如何获得反馈、以及能力与环境之间的依赖。

## 何时使用
- 正例：这个客服流程应该保持 Chat，还是做成有工具的 Agent？按访谈方法分析。
- 反例：直接帮我在服务器部署一个多 Agent 服务。

## 输入
待评估工作流、方案或访谈问题；可选：工具权限、成本和失败案例。

## 交付物
工作流分析、关键假设、风险和小规模验证计划。 默认在对话中交付；只有用户要求文件时，才写入其指定的项目路径，未指定文件名时使用项目内清晰命名的 Markdown 文件并报告路径。

## 不适用范围
不把历史访谈观点包装成最新产品能力；不自动创建多 Agent、外部账号或部署服务。

## 依赖与能力边界
必需：能理解中文的文本模型，以及可读取的输入材料。材料在文件中时需要 Wisp 可用的 `read` 或等效读取工具。无必需 MCP、Python/R 包、CLI、网络或特定操作系统。

可选：用户要求文件时使用可用的 `write` 工具；否则在对话中交付。缺少必需材料或工具时说明具体缺项并暂停依赖它的步骤，其余可独立完成的部分可继续。

## 工作流程
1. 读取 [方法模块](references/methods.md) 中有关反馈、环境或协作的部分；需要来源时读取 [材料概览](references/BOOK_OVERVIEW.md)。
2. 区分用户目标、可观测结果、工具能力和权限；先说明哪些任务不需要 Agent。
3. 评估错误传播、反馈质量、成本与验证方式；输出条件性建议，不将能力假设当作已实现功能。

## 权限与完成检查
技能加载只提供说明，不自动执行脚本、安装依赖或授权操作。默认只读取任务相关材料；文件写入遵循用户当前请求与宿主审批。已有明确授权不重复询问；未回答的问题不是授权。不联网检索、上传、发送消息或调用外部服务来补齐证据。

如果生成文件，确认文件真实存在、可读取、内容完整，再报告路径。分别说明材料核对、格式检查、图像判读和实际计算哪些完成、哪些未做；不得把格式通过或访谈类比当作科学有效性证明。安装整个目录并按包内相对路径读取参考材料；没有运行时侧载脚本。

来源、许可与兼容状态见 [来源说明](references/provenance.md)。
