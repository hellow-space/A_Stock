# A股投资研究仓库

> 用于沉淀 A 股市场复盘、行业研究和数据分析。自动化结果是研究草稿，不代替人工核验。

## 当前能力

- 从东方财富公开行情接口获取主要指数和涨幅居前板块。
- 生成带时间戳的每日复盘 Markdown 草稿。
- 提供每日复盘和行业研究模板。
- 按来源层级整理监管、交易所、数据终端和媒体入口。

目前只有“大盘表现”和“行业热点”由脚本自动填写，其余栏目需要结合原始公告和可信来源人工补充。

## 快速开始

建议使用 Python 3.10 或更高版本。

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python scripts\daily_report.py
```

报告默认写入 `docs/strategy/daily-report-YYYY-MM-DD.md`。也可以指定路径：

```powershell
python scripts\daily_report.py --output-dir docs/strategy
```

运行离线测试：

```powershell
python -m unittest discover -s tests -v
```

## 仓库结构

```text
A_Stock/
├── README.md
├── requirements.txt
├── docs/                     # 研究成果，使用时按主题创建
├── data/                     # 本地数据；原始数据默认不提交
├── scripts/                  # 数据获取与报告生成
├── sources/                  # 来源分级与引用规则
├── templates/                # 研究模板
├── tests/                    # 不访问网络的自动化测试
└── archive/                  # 确有归档内容时再按季度创建
```

Git 不保存空目录，因此 `docs/`、`data/` 和 `archive/` 的子目录按实际需要创建。报告脚本会自动创建输出目录。

## 研究约定

1. 数据和事实尽量附原始链接、发布日期与数据截止日期。
2. 明确区分事实、推断和个人假设；二手来源不能替代正式公告。
3. 自动数据获取失败时停止生成报告，避免把空白内容误认为有效结果。
4. 原始大文件放在 `data/raw/`，不要提交账户信息、持仓截图或访问凭据。

来源选择方法见 [sources/authoritative-sources.md](sources/authoritative-sources.md)。

## 协作方式

- `main` 保持可运行、可阅读。
- 只有在存在明确任务时才创建短期分支，例如 `feature/daily-report` 或 `docs/industry-template`。
- 不按 Agent 身份维护长期分支；完成后通过 Pull Request 合并并删除任务分支。
- 两个 Agent 同时修改时，需要使用不同的 Git worktree 或独立克隆，分支本身不能隔离同一个工作目录。

## 风险说明

仓库内容仅用于个人研究记录，不构成投资建议。行情接口、第三方数据和自动生成内容都可能延迟、缺失或发生口径变化，实际决策前必须回到交易所公告等原始来源核验。

## 更新日志

- 2026-06-20：补齐运行依赖、错误处理、离线测试和研究协作约定。
- 2026-06-20：初始化仓库。
