# 经纬 · 行业洞察

基于肖璟《如何快速了解一个行业》（2025，人民邮电出版社）完整方法论构建的智能行业/企业分析平台。输入行业或企业名称，自动检索最新公开数据，输出结构化研究报告。

## 核心流程

```
输入 → 搜索 → 生成报告 → 事实校验 → 输出报告
         │                    │
    两路并行搜索         独立校验员逐条比对
    ├─ 7维度通用搜索      ├─ ✅ 已验证
    └─ 权威源定向搜索      ├─ ⚠️ 部分匹配
                           └─ ❌ 无来源
```

1. **多维度并行搜索** — 7 个维度（市场规模、竞争格局、商业模式、政策监管、技术创新、投融资、风险挑战）同时在 Tavily 搜索，再加上国家统计局、招股书、券商研报、行业协会等权威源的 `site:` 定向检索
2. **流式生成报告** — Claude 实时输出分析报告，过程可见
3. **独立事实校验** — 另一个 Claude 实例逐条比对报告声明与搜索来源，输出验证表格
4. **完整报告输出** — 报告 + 校验结果合并展示，支持下载 Markdown

## 分析框架

系统自动判断输入类型，选择适配框架：

**行业分析**（七维度）：
| 维度 | 核心问题 |
|------|---------|
| 生命周期定位 | 行业处于导入/成长/成熟/衰退？ |
| 可行性 | 商业模式跑得通吗？ |
| 规模性 | 市场天花板多高？ |
| 防守性 | 护城河够深吗？ |
| 盈利性 | 钱被谁赚走了？ |
| 估值 | 当前阶段值多少钱？ |
| 外部因素(PEST) | 宏观环境影响？ |
| 景气度 | 行业当前冷热？ |

**企业分析**：
| 模块 | 内容 |
|------|------|
| 企业概览与行业定位 | 竞争格局 + 行业位置 |
| 商业模式画布 | 9 要素完整填写 |
| UE 单位经济模型 | 单店/单客收入-成本-利润 |
| 护城河评分卡 | 9 项 1-5 分评分 |
| 竞争定位 | 对标分析 |
| 估值框架 | 可比公司分析 |
| 综合评估 | — |

每种模式下报告末尾都包含 **数据来源说明**、**事实校验** 和 **合规要求**（现行政策法规及标准清单）。

**对比分析**（用 `vs` 隔开）支持三种组合：
- 行业 vs 行业 → 七维度并排对比
- 企业 vs 企业 → 商业模式/UE/护城河/估值 PK
- 企业 vs 行业 → 企业在行业中定位 + 全景分析

## 数据来源优先级

报告引用的数据按以下优先级：

1. **招股书 / 年报**（最权威、最详实、免费）— 巨潮资讯网 cninfo.com.cn
2. **国家统计局 / 行业协会** — stats.gov.cn、CCFA、中汽协等
3. **券商研报** — 东方财富 eastmoney.com 免费获取
4. **咨询公司报告** — 艾瑞、亿欧、麦肯锡、BCG 等
5. **专业数据库** — Wind、Euromonitor、Statista 等

> 数据来源大全见应用内「资源库」页面（15 大类、130+ 个来源），以及 `knowledge-base/data-sources.md`。

## 功能亮点

- **智能类型判断** — 自动识别输入是行业还是企业，选择适配分析框架
- **实时流式输出** — 报告生成和事实校验过程可见，非黑盒等待
- **权威源定向搜索** — 用 `site:` 语法精准检索国家统计局、招股书、行业协会、券商研报
- **Firecrawl 全文抓取** — 自动抓取搜索结果中排名靠前的权威页面全文
- **图表可视化** — 支持柱状图、折线图、饼图、雷达图（JSON → matplotlib 渲染）
- **目录导航** — 左侧 TOC 点击跳转，仅显示 `##` 章节标题
- **报告存档** — 自动保存 Markdown 到 `reports/` 目录，支持一键下载
- **资源库** — 15 大类、130+ 个数据来源，可搜索筛选，点击直达

## 项目结构

```
industry-analysis/
├── app/
│   ├── main.py                 # 主页（智能分析入口）
│   ├── pages/
│   │   ├── 6_报告中心.py        # 报告存档浏览
│   │   └── 7_资源库.py          # 全书资源清单（15类130+来源）
│   ├── services/
│   │   └── claude_client.py    # Claude API 封装（含流式）
│   ├── utils/
│   │   ├── search.py           # 联网搜索（Tavily + Firecrawl 双引擎）
│   │   ├── chart.py            # 图表解析与渲染
│   │   ├── knowledge.py        # 知识库加载器
│   │   └── style.py            # CSS 注入
│   └── assets/                 # 全局样式
├── knowledge-base/             # 12 个方法论知识库
│   ├── data-sources.md         # 数据来源大全（15 大类）
│   ├── business-model-canvas.md
│   ├── moat-framework.md
│   ├── competitive-analysis.md
│   ├── valuation-guide.md
│   ├── market-sizing.md
│   ├── industry-lifecycle.md
│   ├── pest-framework.md
│   ├── prosperity-tracking.md
│   ├── ai-research-guide.md
│   ├── research-cookbook.md
│   └── glossary.md
├── skills/                     # Claude Code Skills
│   ├── industry-analyzer.md    # 行业分析
│   ├── company-analyzer.md     # 企业分析
│   ├── industry-compare.md     # 行业对比
│   ├── company-compare.md      # 企业对比
│   ├── research-method.md      # 研究方法
│   └── industry-glossary.md    # 术语查询
├── reports/                    # 生成的报告存档
├── Dockerfile
├── requirements.txt
├── PLAN.md                     # 完整工作计划
└── README.md
```

## 快速开始

### 前提

- Python 3.8+
- Anthropic API Key（或中转站 Key）
- Tavily API Key（免费 1000 次/月，注册：[tavily.com](https://tavily.com)）
- Firecrawl API Key（免费 500 credits/月，注册：[firecrawl.dev](https://firecrawl.dev)）

### 安装运行

```bash
git clone https://github.com/AbbyZhao0917/industry-analysis.git
cd industry-analysis
pip install -r requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入 ANTHROPIC_API_KEY、TAVILY_API_KEY、FIRECRAWL_API_KEY
# 如使用中转站，设置 ANTHROPIC_BASE_URL 和 ANTHROPIC_MODEL

streamlit run app/main.py
```

访问 `http://localhost:8501`

### Docker 部署

```bash
docker build -t industry-analysis .
docker run -p 8501:8501 --env-file .env industry-analysis
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `ANTHROPIC_API_KEY` | Anthropic API Key（必填） |
| `ANTHROPIC_BASE_URL` | API 地址（直接连 Anthropic 可不填） |
| `ANTHROPIC_MODEL` | 模型名称，如 `anthropic/claude-sonnet-4.6` |
| `TAVILY_API_KEY` | Tavily 搜索 Key（必填，[注册](https://tavily.com)） |
| `FIRECRAWL_API_KEY` | Firecrawl 抓取 Key（必填，[注册](https://firecrawl.dev)） |

## 参考资源

- 肖璟《如何快速了解一个行业》(2025，人民邮电出版社，ISBN 9787115674937)
- 应用内「资源库」页面：15 大类、130+ 个权威数据来源

## License

MIT
