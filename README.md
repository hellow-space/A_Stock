# A股投资研究仓库

> 个人投资研究笔记与数据分析，聚焦A股市场宏观、行业与个股研究。

## 仓库结构

```
A_Stock/
├── README.md                 # 本文件
├── docs/                     # 研究文档
│   ├── macro/               # 宏观研究（政策、经济数据、市场策略）
│   ├── industry/            # 行业研究（AI、新能源、半导体等）
│   ├── company/             # 公司研究（个股深度分析）
│   └── strategy/            # 策略研究（交易思路、仓位管理）
├── data/                     # 数据文件
│   ├── raw/                 # 原始数据（不过度提交）
│   └── processed/           # 处理后数据
├── sources/                  # 信息来源汇总
├── scripts/                  # 自动化脚本
├── templates/                # 文档模板
└── archive/                  # 归档
    └── 2026-Q2/
```

## 协作分支规范

| 分支 | 用途 | 负责人 |
|------|------|--------|
| `main` | 稳定版本，仅合并审核后的内容 | 维护者 |
| `agent-trae` | Trae Agent 工作区 | Trae |
| `agent-codesize` | CodeSize Agent 工作区 | CodeSize |

## 工作流程

1. 各Agent在各自分支工作
2. 完成编辑后提交到个人分支
3. 创建 Pull Request 合并到 `main`
4. 另一方审核后合并

## 信息来源

见 [sources/authoritative-sources.md](sources/authoritative-sources.md)

## 更新日志

- 2026-06-20: 仓库初始化
