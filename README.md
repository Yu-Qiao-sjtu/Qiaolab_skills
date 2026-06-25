# AI4asking

> 追问 > 提问：AI 时代真正的分水岭

一键适配 6 大 AI 平台。核心论点：AI 降低了提问门槛，但区分度藏在追问的深度里。真正的功夫不在第一问，而在第十问。

---

## 快速安装

```powershell
git clone https://github.com/Yu-Qiao-sjtu/Qiaolab_skills.git
```

---

## 平台适配

### WispTerm

将 `skills/AI4asking/` 复制到配置目录：

| 位置 | 路径 |
|------|------|
| 全局（推荐） | `%APPDATA%\wispterm\skills\AI4asking\` |
| 项目级 | `<项目目录>\skills\AI4asking\` |
| 可执行文件旁 | `<wispterm目录>\skills\AI4asking\` |

```
$AI4asking 帮我审视这个分析还有什么遗漏
```

验证：输入 `/skills`，应看到 `AI4asking`。

---

### Claude Code

将 `CLAUDE.md` 复制到：

| 作用域 | 路径 |
|------|------|
| 项目级（推荐） | `<项目根目录>/CLAUDE.md` |
| 全局 | `~/.claude/CLAUDE.md` |

Claude Code 启动时自动加载，无需手动调用。

---

### OpenAI Codex CLI

将 `CODEX.md` 复制到：

| 作用域 | 路径 |
|------|------|
| 项目级（推荐） | `<项目根目录>/CODEX.md` |

Codex 启动时自动加载。

---

### Cursor

将 `.cursorrules` 复制到：

| 作用域 | 路径 |
|------|------|
| 项目级 | `<项目根目录>/.cursorrules` |

Cursor 自动读取，无需手动调用。

---

### Windsurf

将 `.windsurfrules` 复制到：

| 作用域 | 路径 |
|------|------|
| 项目级 | `<项目根目录>/.windsurfrules` |

Windsurf 自动读取。

---

### GitHub Copilot

将 `.github/copilot-instructions.md` 复制到：

| 作用域 | 路径 |
|------|------|
| 项目级 | `<项目根目录>/.github/copilot-instructions.md` |

Copilot 自动加载。

---

## 适用平台速查

| 平台 | 文件 | 加载方式 |
|------|------|:--:|
| WispTerm | `skills/AI4asking/SKILL.md` | `$AI4asking` 手动调用 |
| Claude Code | `CLAUDE.md` | 自动 |
| Codex CLI | `CODEX.md` | 自动 |
| Cursor | `.cursorrules` | 自动 |
| Windsurf | `.windsurfrules` | 自动 |
| GitHub Copilot | `.github/copilot-instructions.md` | 自动 |

---

## 三级追问深度

| 级别 | 核心问题 | 关注点 |
|:--:|------|------|
| **一级** | 「你说的是真的吗？」 | 事实核查：数据对吗？来源对吗？ |
| **二级** | 「推理过程有漏洞吗？」 | 逻辑链审计：前提→推理→结论，哪一步最弱？ |
| **三级** | 「你依赖了什么隐含假设？」 | 假设爆破：AI 没说的那个预设是什么？推翻它会怎样？ |

---

## 追问话术模板

- 「你的第 X 点隐含假设是 Y，验证过吗？」
- 「这个结论在 Z 条件下还适用吗？」
- 「你排除了哪些替代解释？」
- 「这个建议在我的约束 X 下可执行吗？」

---

## License

MIT
