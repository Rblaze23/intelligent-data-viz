---
title: Intelligent Data Viz
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.30.0
app_file: app.py
pinned: false
license: mit
---

# 📊 Intelligent Data Visualization Platform

> **AI-Powered Data Analysis & Visualization using Groq LLM**

An intelligent web application that automatically generates professional data visualizations and executive-level BI analysis reports from your datasets using natural language. Simply upload your data, describe what you want to analyze, and let AI do the rest.

[![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://python.org)
[![Plotly](https://img.shields.io/badge/Plotly-5.18.0-3F4F75?logo=plotly)](https://plotly.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🌟 Key Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| 📤 **Smart Data Upload** | CSV/Excel files up to 10MB with automatic encoding & delimiter detection |
| 💬 **Natural Language Input** | Describe your analysis goal in plain English |
| 🤖 **AI-Powered Recommendations** | LLM generates 3 optimal visualization proposals with justifications |
| 📊 **Interactive Visualizations** | 6 chart types rendered with Plotly (scatter, bar, line, histogram, box, heatmap) |
| 📋 **Dynamic Dashboards** | VLM-generated dashboard specs with KPIs, metrics, and insights |
| 🧠 **BI Analysis Reports** | Executive-level analysis using 3-step scaffolded LLM prompting |
| 💾 **Multi-Format Export** | High-quality PNG (2x scale) and interactive HTML |
| 🎨 **Professional Styling** | Colorblind-safe palettes, consistent theming |
| ⚡ **Response Caching** | Faster repeat queries with intelligent caching |

### Smart BI Module: 

- **BI Analyst Module** — Generate professional textual interpretation of dashboard figures
- **3-Step Scaffolded Prompting** — Chained LLM analysis for richer insights
- **Dynamic Dashboard Selection** — User's selected chart displayed as primary figure
- **Real Plotly Figures in Dashboard** — Actual generated charts, not just supplementary visuals

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Groq API Key](https://console.groq.com/) (free tier available)

### Installation

```bash
# Clone the repository
git clone https://github.com/Rblaze23/intelligent-data-viz.git
cd intelligent-data-viz

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure API key
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### Run the Application

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### Example Datasets

Try the app with our sample datasets in `examples/`:
- `housing_prices.csv` — Real estate price analysis
- `sales_data.csv` — Product sales trends
- `student_performance.csv` — Educational performance analysis

---

## 📖 How It Works

### 6-Step Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Step 1️⃣  Upload Data        →  CSV/Excel upload + automatic validation    │
│  Step 2️⃣  Problem Statement  →  Natural language analysis goal             │
│  Step 3️⃣  AI Visualization   →  LLM recommends 3 chart types + generates   │
│  Step 4️⃣  Dashboard          →  VLM builds dashboard with selected primary │
│  Step 5️⃣  BI Analysis (NEW)  →  3-step scaffolded executive report         │
│  Step 6️⃣  Export             →  PNG / HTML download                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### BI Analysis: 3-Step Scaffolded Prompting

The BI analysis uses a **chained prompt scaffolding technique** where each step builds on the previous one:

| Step | Purpose | Output |
|------|---------|--------|
| **Step 1** | Data & problem understanding | Business context, hypotheses, key metrics |
| **Step 2** | Figure interpretation (receives Step 1) | Performance insights, segment analysis |
| **Step 3** | Executive synthesis (receives Steps 1+2) | Executive summary, recommendations, next steps |

This produces significantly richer analysis than a single-shot prompt.

---

## 🏗️ Architecture

```
intelligent-data-viz/
├── app.py                    # Main Streamlit application (1100+ lines)
├── src/
│   ├── config/
│   │   └── settings.py       # Environment & constants
│   ├── data/
│   │   ├── processor.py      # CSV loading, encoding detection (369 lines)
│   │   ├── profiler.py       # Data profiling & statistics (437 lines)
│   │   └── validator.py      # Data quality validation (139 lines)
│   ├── llm/
│   │   ├── client.py         # Groq API client with retry logic
│   │   ├── analyzer.py       # LLM-based visualization analyzer (245 lines)
│   │   └── prompts.py        # Prompt templates (incl. BI scaffolds)
│   ├── visualization/
│   │   ├── generator.py      # 6 Plotly chart generators (383 lines)
│   │   ├── styler.py         # Colorblind-safe theming (150 lines)
│   │   ├── exporter.py       # PNG/HTML export (216 lines)
│   │   └── vlm_enhancer.py   # VLM dashboard generation (906 lines)
│   ├── ui/
│   │   └── components.py     # Reusable Streamlit components (380+ lines)
│   └── utils/
│       ├── logger.py         # Centralized logging
│       ├── exceptions.py     # Custom exception hierarchy (8 types)
│       └── token_counter.py  # Token usage & cost tracking
├── tests/
│   ├── unit/                 # 49 unit tests
│   ├── integration/          # 6 end-to-end tests
│   └── conftest.py           # Pytest fixtures
├── examples/                 # Sample datasets
│   ├── housing_prices.csv
│   ├── sales_data.csv
│   └── student_performance.csv
└── docs/
    └── architecture.md
```

### Data Flow

```
User Upload → DataProcessor → DataProfiler → DataValidator
                                    ↓
                            VisualizationAnalyzer (LLM)
                                    ↓
                         VisualizationGenerator (Plotly)
                                    ↓
                           GroqVLMEnhancer (Dashboard)
                                    ↓
                          BI Analysis (3-step LLM)
                                    ↓
                         VisualizationExporter (PNG/HTML)
```

### Module Descriptions

| Module | Description |
|--------|-------------|
| **DataProcessor** | Loads CSV/Excel with automatic encoding (chardet) and delimiter detection |
| **DataProfiler** | Generates comprehensive column stats, correlations, data quality metrics |
| **DataValidator** | Validates minimum rows/columns, missing values, visualization suitability |
| **LLMClient** | Groq API wrapper with exponential backoff retry logic |
| **VisualizationAnalyzer** | Generates 3 visualization specs from problem + data using LLM |
| **PromptTemplates** | Token-optimized prompts (compact mode saves ~30% tokens) |
| **VisualizationGenerator** | Creates 6 chart types from specs using Plotly Express |
| **Styler** | Applies colorblind-safe palettes (Okabe-Ito) and consistent theming |
| **GroqVLMEnhancer** | VLM-powered dashboard spec generation with KPIs and insights |
| **VisualizationExporter** | Exports to PNG (with Kaleido) and interactive HTML |
| **UIComponents** | 15+ reusable Streamlit components (tabs, metrics, expanders) |
| **TokenCounter** | Tracks token usage and estimates costs per model |

---

## 📊 Supported Visualizations

| Type | Best For | Example Use Case |
|------|----------|------------------|
| **Scatter Plot** | Relationships between 2 variables | Price vs. Size correlation |
| **Bar Chart** | Categorical comparisons | Sales by region |
| **Line Chart** | Trends over time | Revenue growth |
| **Histogram** | Distribution analysis | Age distribution |
| **Box Plot** | Statistical summaries & outliers | Salary ranges by department |
| **Heatmap** | Correlation matrices | Feature correlations |

---

## 🧪 Testing

```bash
# Run all tests (55 test functions)
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run integration tests (requires GROQ_API_KEY)
pytest tests/integration/

# Quick unit tests only
pytest tests/unit/ -v
```

### Test Coverage

| Module | Tests |
|--------|-------|
| Data Processor | 19 |
| LLM Analyzer | 10 |
| LLM Client | 7 |
| Full Flow Integration | 6 |
| Prompts | 5 |
| Config | 3 |
| Logger | 3 |
| Utils | 2 |
| **Total** | **55** |

---

## 🛠️ Development

### Code Quality Tools

```bash
# Format code
black src/ tests/ app.py

# Lint
flake8 src/ tests/ app.py

# Type checking
mypy src/
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for LLM access | ✅ |

### LLM Models Used

| Model | Purpose |
|-------|---------|
| `llama-3.3-70b-versatile` | Visualization analysis & BI reports |
| `meta-llama/llama-4-scout-17b-16e-instruct` | VLM dashboard generation |

---

## 📦 Dependencies

```
streamlit>=1.30.0          # Web framework
pandas>=2.0.0              # Data manipulation
plotly>=5.18.0             # Interactive visualizations
groq>=0.4.0                # LLM API client
langchain-groq>=0.0.1      # LangChain integration
kaleido>=0.2.1             # Static image export
python-dotenv>=1.0.0       # Environment management
chardet>=5.0.0             # Encoding detection
numpy>=1.24.0              # Numerical operations
```

---

## 🌐 Deployment

**Live Demo**: [https://huggingface.co/spaces/Yassineh13/intelligent-data-viz](https://huggingface.co/spaces/Yassineh13/intelligent-data-viz)

The app is deployed on Hugging Face Spaces with automatic deployment from the main branch.

### Docker (Optional)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## 👥 Team

| Name | Role |
|------|------|
| **Ramy Lazgheb** | LLM & Data Processing Lead |
| **Chiheb Guesmi** | Generated Visualizations & Frontend Lead |
| **Mohamed Yassine Madhi** | Infrastructure & Quality Lead |

---

## 📝 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📚 Documentation

- [Architecture Guide](docs/architecture.md)
- [LLM Integration](src/llm/ReadmeLLM.md)
- [Data Processing](src/data/Readmedata.md)
- [Changelog](CHANGELOG.md)

---

## 🙏 Acknowledgments

- [Groq](https://groq.com) — Lightning-fast LLM inference
- [Streamlit](https://streamlit.io) — Web framework
- [Plotly](https://plotly.com) — Interactive visualizations
- Open source community

---

<div align="center">

**Master 2 BDIA — Data Visualization Project**

*February 2026*

</div>
