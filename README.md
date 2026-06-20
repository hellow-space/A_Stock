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

## GitHub 存档

每完成一轮项目修改，都执行以下动作：

1. 在本 README 的“变更记录”中写明本轮改动。
2. 将代码、文档和 README 一起提交，保证提交内容与说明一致。
3. 立即推送到 GitHub，使用提交记录作为可回溯存档。

仓库提供了两个手动存档入口：

```powershell
.\scripts\git_push.ps1
```

也可以双击运行 `scripts/git_push.bat`。两个脚本都会提交当前修改并推送到 `main`。

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

## 变更记录

### 2026-06-20：Agent 协作工作流程

- 新增 `agents.md`，明确 Trae 和 CodeSize 的工作流程、分工、文件规范和检查清单。
- 确立协作原则：本地优先、同步先行、及时推送、保持一致。

### 2026-06-20：仓库可用性整理与自动存档

- 重写 `scripts/daily_report.py`：自动创建输出目录，校验接口响应，修正成交额字段，接口失败时不再生成误导性的空白报告。
- 新增 `requirements.txt`，声明 `requests` 运行依赖。
- 新增 `tests/test_daily_report.py`，覆盖报告生成、目录创建、行情填充和异常响应，共 3 项离线测试。
- 更新每日复盘模板，明确自动填写栏目和必须人工核验的栏目。
- 更新行业研究模板，增加信息截止日期、统计期、原始来源、验证指标和逻辑失效条件。
- 重写研究来源清单，将来源划分为法定原始来源、专业研究工具和新闻线索，并增加最低引用要求。
- 更新 `.gitignore`，扩大本地原始数据、测试缓存、日志和临时文件的忽略范围。
- 新增 `scripts/git_push.ps1` 和 `scripts/git_push.bat`，用于手动提交并推送项目修改。
- 确立存档规则：今后每轮项目修改都同步更新 README、创建 Git 提交并推送 GitHub。

### 2026-06-20：初始化仓库

- 创建研究目录规划、每日复盘模板、行业研究模板、来源清单和首个行情脚本。
