# Wisp Science 技能规范

本仓库按 [Wisp Science 作者指南](https://github.com/xuzhougeng/wisp-science/blob/ffd8dd7af4ec80bf4fed3f3cdb878c766b970d9c/docs/skill-authoring.md) 和实际 Rust 解析器适配，固定参考提交 `ffd8dd7af4ec80bf4fed3f3cdb878c766b970d9c`，作者声明目标版本为 **1.11.0**。

## 目录与触发

每个 `skills/<name>/` 是完整、自包含的安装单元。`SKILL.md` 的 `name` 与目录名一致，使用小写字母、数字和单连字符。`description` 同时说明适用场景与排除范围；正文按“职责 → 触发 → 输入 → 交付物 → 排除范围”展开，再说明依赖、流程和权限。详细材料在包内 `references/`，按需要读取。

`wisp` 采用 schema_version 1 及当前解析器的受控词表。我们声明 `project_write` 是因为用户可要求项目内 Markdown 文件；默认交付仍在对话中。此字段不授予任何写入权限。没有匹配的受控 output 类型时使用空数组，不发明新值。

## 安装和更新

Wisp 的持久用户技能目录是 `~/.wisp/skills`；项目技能目录是 `<项目>/.wisp/skills`。不要沿用 WispTerm 的 APPDATA 或 `.config/wispterm` 路径，不要放入应用资源目录。

公开仓库可在 **Settings → Skills** 中导入 GitHub 技能目录链接；必须安装完整目录，不能只复制 SKILL.md。私有仓库不受当前 GitHub 商店支持，应先通过有权限的 Git 客户端克隆，然后项目安装，或用上游打包工具生成 `.skill` 后通过 Settings 导入。

项目安装示例（当前工作目录为本仓库根目录；先用实际存在的项目路径替换参数）：

```sh
python scripts/install_skill.py --skill ai4asking --project /path/to/research-project
```

Windows 同样使用此 Python 命令，项目路径可写成 `D:/Research/MyProject`。脚本只复制本地完整目录，不联网，不安装依赖，不覆盖同名包。刷新或重新打开项目后，通过 `search_skills` 查找并用 `use_skill` 加载；这是发现/加载步骤，不是模型任务验证。

更新已有安装前先将整个旧目录备份到发现目录之外并检查本地改动。仓库更新和应用升级不会自动更新已安装技能；当前商店也不会覆盖同名包。

## 验证层次

1. 自有离线检查：所有 Markdown 资源路径、完整文件复制、拒绝覆盖与失败时不暴露半成品。
2. 固定上游 `quick_validate.py`：名称、frontmatter、描述长度等作者约定。
3. 原版 Rust `manifest.rs` 和 `distribution.rs`：真实 YAML/metadata 解析、资源检查、临时目录安装、安装后重读及同名拒绝覆盖。相关源文件由明确的维护命令下载并校验 SHA-256，不作为技能资源分发。
4. 真实 Wisp 模型任务：需要模型和实际 Wisp 会话；本次未执行。因此 `verified_wisp` 保持 null，`evals/` 只保存待执行案例，不将它们描述为已通过模型评测。

维护者验证命令见 [仓库开发规则](../AGENTS.md)。Rust 验证工具依其目录许可证使用 AGPL-3.0-only；技能包保留各自原许可证。

## 可导入包

执行 `python scripts/fetch_wisp_validator.py` 后，再执行 `python scripts/package_skills.py`，会使用固定的上游打包器生成 `dist/<name>.skill` 并逐文件核对包内容。生成包不等于安装到当前用户环境，私有技能包不得上传公开仓库。CI 的 Rust 验证工具固定为 1.96.1；它是维护依赖，不是使用这些文本技能的依赖。
