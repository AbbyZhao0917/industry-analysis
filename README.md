# 🔬 行业分析平台 Industry Analysis Platform

基于肖璟《如何快速了解一个行业》（2025，人民邮电出版社）完整方法论构建的行业/企业分析工具。

## 🧠 七维度分析框架

| 维度 | 核心问题 | 主要模型 |
|------|---------|---------|
| **可行性** | 商业模式跑得通吗？ | 商业模式画布、对标法、UE模型 |
| **规模性** | 市场天花板多高？ | TAM/SAM/SOM、渗透率法 |
| **防守性** | 护城河够深吗？ | 护城河9子项评分卡 |
| **盈利性** | 钱被谁赚走了？ | CRn、五力模型、产业链利润分配 |
| **估值** | 当前阶段值多少钱？ | 生命周期对应估值法 |
| **外部因素** | 宏观环境影响？ | PEST分析 |
| **景气度** | 行业当前冷热？ | 行业类型→关键指标跟踪 |

## 📂 项目结构

```
industry-analysis/
├── PLAN.md                    # 完整工作计划
├── skills/                    # 6个 Claude Code Skills
│   ├── industry-analyzer.md   # 行业分析
│   ├── company-analyzer.md    # 企业分析
│   ├── company-compare.md     # 企业对比
│   ├── industry-compare.md    # 行业对比
│   ├── research-method.md     # 研究方法
│   └── industry-glossary.md   # 术语解释
├── knowledge-base/            # 12个方法论知识库
│   ├── industry-lifecycle.md  # 产业生命周期
│   ├── business-model-canvas.md
│   ├── market-sizing.md
│   ├── moat-framework.md
│   ├── competitive-analysis.md
│   ├── pest-framework.md
│   ├── valuation-guide.md
│   ├── prosperity-tracking.md
│   ├── research-cookbook.md
│   ├── data-sources.md
│   ├── ai-research-guide.md
│   └── glossary.md
├── app/                       # Streamlit 平台
│   ├── main.py                # 首页 Dashboard
│   ├── pages/                 # 7个功能页面
│   │   ├── 1_行业分析.py
│   │   ├── 2_企业分析.py
│   │   ├── 3_企业对比.py
│   │   ├── 4_行业对比.py
│   │   ├── 5_研究工具箱.py
│   │   ├── 6_报告中心.py
│   │   └── 7_知识库.py
│   ├── services/
│   │   └── claude_client.py   # Anthropic API 封装
│   └── utils/
│       └── knowledge.py       # 知识库加载器
├── reports/                   # 示例分析报告
├── Dockerfile                 # Docker 部署
└── requirements.txt
```

## 🚀 快速开始

### 前提条件

- Python 3.11+
- Anthropic API Key

### 安装运行

```bash
# 克隆仓库
git clone https://github.com/AbbyZhao0917/industry-analysis.git
cd industry-analysis

# 安装依赖
pip install -r requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入你的 ANTHROPIC_API_KEY

# 启动
streamlit run app/main.py
```

访问 `http://localhost:8513`

### Docker 部署

```bash
docker build -t industry-analysis .
docker run -p 8513:8513 --env-file .env industry-analysis
```

## 📊 使用 Claude Code Skills

将 `skills/` 目录下的 `.md` 文件注册到 Claude Code，即可在对话中使用：

- `/行业分析 便利店` — 七维度行业分析
- `/企业分析 见福便利店` — 商业模式+UE+护城河
- `/企业对比 罗森 见福` — 双企业PK
- `/行业对比 便利店 社区团购` — 跨行业对比
- `/研究方法 如何评估连锁餐饮扩张潜力` — 研究方案生成

## 📖 参考资源

- 肖璟《如何快速了解一个行业》(2025, 人民邮电出版社, ISBN 9787115674937)
- [国家统计局](https://www.stats.gov.cn/)
- [东方财富](https://www.eastmoney.com/)
- [CCFA 中国连锁经营协会](https://www.ccfa.org.cn/)

## 📄 License

MIT