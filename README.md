# PPT Skills for AI-Assisted Content Creation

两个 AI Skill，用于汇报类 PPT 的内容策划与 SVG 页面生成。加载到 AI 编程助手后，AI 会按已验证的流程工作。

配套教程：[《汇报类 PPT 的 AI 生成实践与 Skill 分享》](#)

## 包含什么

| Skill | 文件 | 作用 |
|---|---|---|
| ppt-content-strategist | `SKILL.md` | 五步采访流程 → 金字塔/SCQA/MECE → 逐页大纲 |
| ppt-svg-builder | `SKILL.md` + `validate_svg.py` | 六套 SVG 模板 + 六条安全规则 + 自动验证器 |

## 前置条件

- 安装一款 AI 编程助手：Trae IDE、DSH、Cursor、Claude Code 均可
- 跑 SVG 生成 + 导出：还需 Python 3.x + `pip install ppt-master`
- 只用「内容策略师」做内容框架：Python 非必需

## 安装

```
你的项目目录/
└── .trae/                （DSH 用 .dsh/，Cursor 用 .cursor/，Claude Code 用 .claude/）
    └── skills/
        ├── ppt-content-strategist/
        │   └── SKILL.md
        └── ppt-svg-builder/
            ├── SKILL.md
            └── validate_svg.py
```

把本仓库对应文件夹复制到你的 AI 编程助手项目根目录下即可。

## 使用

- 「加载 ppt-content-strategist，帮我想清楚要讲什么」——AI 采访你后输出内容 Brief
- 「加载 ppt-svg-builder，用 card-single 模板做一页」——AI 选模板、生成 SVG、提示跑 checker

加载一次后，整个会话中 Skill 持续生效。

## 没有编程助手？

手动走七站流程效果一样。模板和 checker 脚本可单独用：打开 SKILL.md → 复制模板 SVG → 浏览器预览 → 手动填文字。`python validate_svg.py 你的页面.svg` 独立运行。

---

*方法论来源：麦肯锡金字塔原理 / SCQA / MECE；工具基础：PPT Master 开源框架；实战数据：累计 99 页 SVG 产出 + 55 条踩坑记录。*