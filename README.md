# AI4asking

> 追问 > 提问：AI 时代真正的分水岭

## 安装

```powershell
git clone https://github.com/Yu-Qiao-sjtu/Qiaolab_skills.git
```

将 `skills/` 文件夹复制到 WispTerm 配置目录（任选其一）：

| 位置 | 路径 |
|------|------|
| 全局配置（推荐） | `%APPDATA%\wispterm\skills\` |
| 当前工作目录 | `<项目目录>\skills\` |
| WispTerm 可执行文件旁 | `<wispterm目录>\skills\` |

最终结构：

```
%APPDATA%\wispterm\skills\AI4asking\SKILL.md
```

## 使用

在 WispTerm Copilot 中输入：

```
$AI4asking 帮我审视这个分析还有什么遗漏
```

### 三级追问深度

| 级别 | 问什么 | 示例 |
|:--:|------|------|
| 一级 | 事实核查 | 「你引用的数据来源是什么？」 |
| 二级 | 逻辑链审计 | 「前提→推理→结论，哪一步最弱？」 |
| 三级 | 隐含假设爆破 | 「你依赖的那个没说的预设，推翻它会怎样？」 |

### 追问话术模板

- 「你的第 X 点隐含假设是 Y，验证过吗？」
- 「这个结论在 Z 条件下还适用吗？」
- 「你排除了哪些替代解释？」
- 「这个建议在我的约束 X 下可执行吗？」

## 验证安装

在 WispTerm Copilot 中输入 `/skills`，应看到 `AI4asking` 出现在列表中。

## License

MIT
