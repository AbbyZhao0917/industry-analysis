# 经纬 · 行业洞察平台

基于肖璟《如何快速了解一个行业》（2025，人民邮电出版社）完整方法论构建的行业/企业分析工具。

## 七维度分析框架

| 维度 | 核心问题 | 主要模型 |
|------|---------|---------|
| 可行性 | 商业模式跑得通吗？ | 商业模式画布、对标法、UE模型 |
| 规模性 | 市场天花板多高？ | TAM/SAM/SOM、渗透率法 |
| 防守性 | 护城河够深吗？ | 护城河9子项评分卡 |
| 盈利性 | 钱被谁赚走了？ | CRn、五力模型、产业链利润分配 |
| 估值 | 当前阶段值多少钱？ | 生命周期对应估值法 |
| 外部因素 | 宏观环境影响？ | PEST分析 |
| 景气度 | 行业当前冷热？ | 行业类型→关键指标跟踪 |

## 项目结构

```
industry-analysis/
├── PLAN.md                    # 完整工作计划
├── skills/                    # 6个 Claude Code Skills
├── knowledge-base/            # 12个方法论知识库
├── app/                       # Streamlit 平台
│   ├── main.py                # 首页 Dashboard
│   ├── pages/                 # 7个功能页面
│   ├── services/              # Anthropic API 封装
│   ├── utils/                 # 知识库加载器 + CSS 注入
│   └── assets/                # 全局样式
├── reports/                   # 示例分析报告
├── Dockerfile
└── requirements.txt
```

## 快速开始

### 前提

- Python 3.11+
- Anthropic API Key

### 安装运行

```bash
git clone https://github.com/AbbyZhao0917/industry-analysis.git
cd industry-analysis
pip install -r requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入 ANTHROPIC_API_KEY

streamlit run app/main.py
```

访问 `http://localhost:8513`

### Docker 部署

```bash
docker build -t industry-analysis .
docker run -p 8513:8513 --env-file .env industry-analysis
```

## 参考资源

- 肖璟《如何快速了解一个行业》(2025, 人民邮电出版社, ISBN 9787115674937)
- [国家统计局](https://www.stats.gov.cn/)
- [CCFA 中国连锁经营协会](https://www.ccfa.org.cn/)

## License

MIT
