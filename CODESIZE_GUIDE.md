# CodeSize 协作指南

## 你的任务

帮助用户管理 `https://github.com/hellow-space/A_Stock` 仓库，进行A股投资研究。

## 每次工作前必读

1. **读取 `README.md`** — 了解项目当前状态和进度
2. **读取 `CODESIZE_GUIDE.md`**（本文件）— 确认协作规范
3. **检查变更记录** — 了解上次修改内容

## 每次工作后必做

1. **修改 `README.md`** — 在"变更记录"中写明本轮改动
2. **提交并推送** — 执行以下命令：
   ```bash
   git add .
   git commit -m "描述修改内容"
   git push origin main
   ```

## 项目结构

```
A_Stock/
├── README.md              # 项目总览（每次修改前必读）
├── CODESIZE_GUIDE.md      # 本文件
├── docs/                  # 研究文档
│   ├── macro/            # 宏观研究
│   ├── industry/         # 行业研究
│   ├── company/          # 公司研究
│   └── strategy/         # 策略研究（每日复盘放这里）
├── scripts/              # 自动化脚本
├── templates/            # 文档模板
├── sources/              # 信息来源汇总
└── data/                 # 数据文件（原始数据不提交）
```

## 你可以做的事

| 任务类型 | 示例 |
|----------|------|
| 行业研究 | 在 `docs/industry/` 创建 `AI算力.md`、`新能源.md` 等 |
| 公司分析 | 在 `docs/company/` 创建个股深度分析 |
| 策略报告 | 在 `docs/strategy/` 创建周报、月报 |
| 数据获取 | 运行/修改 `scripts/daily_report.py` |
| 模板优化 | 改进 `templates/` 中的研究模板 |

## 研究规范

1. **数据来源**：优先使用证监会、交易所、Wind等权威来源
2. **事实标注**：区分事实、推断、假设，附原始链接
3. **日期标注**：所有数据必须注明截止日期
4. **风险提示**：明确写出逻辑失效条件

## 与Trae的分工

- **Trae**：负责每日市场复盘、数据获取、信息整理
- **CodeSize**：负责深度研究、策略分析、报告撰写

## 紧急联系

如果遇到Git推送问题，告诉用户运行：
```powershell
.\scripts\git_push.ps1
```

或双击 `scripts/git_push.bat`
