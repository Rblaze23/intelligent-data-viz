# LLM Module Documentation

## Overview

This module handles all LLM (Large Language Model) interactions for intelligent visualization generation using Groq API.

## Components

### `client.py` - LLM API Client

**Purpose:** Manages communication with Groq API with retry logic.

**Key Features:**
- Automatic retry on rate limits (exponential backoff)
- Support for multiple Groq models
- Error handling and validation

**Usage:**
```python
from src.llm.client import LLMClient

client = LLMClient(model="llama-3.3-70b-versatile")
response = client.generate_completion("Your prompt here")
```

**Available Models:**
- `llama-3.3-70b-versatile` (default, recommended)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `llama-3.1-8b-instant`

---

### `prompts.py` - Prompt Templates

**Purpose:** Provides optimized prompt templates for visualization tasks.

**Key Features:**
- Token-efficient compact prompts (50% fewer tokens)
- Detailed prompts for complex analysis
- Structured JSON output format

**Usage:**
```python
from src.llm.prompts import PromptTemplates

templates = PromptTemplates()

# Use compact prompt (saves tokens)
prompt = templates.analyze_problem_and_data(
    problem="What affects prices?",
    column_info={"price": "float", "size": "int"},
    sample_data="price,size\n100,50",
    compact=True  # 50% token savings
)
```

**Token Savings:**
- Compact mode: ~150-250 tokens per request
- Detailed mode: ~300-500 tokens per request
- **Savings: ~47% with compact mode**

---

### `analyzer.py` - Main Analyzer

**Purpose:** Orchestrates LLM calls to generate visualization recommendations.

**Key Features:**
- Generates 3 visualization recommendations
- Caching system (avoid repeated API calls)
- Token usage tracking
- Validation of LLM responses

**Usage:**
```python
from src.llm.analyzer import VisualizationAnalyzer
import pandas as pd

# Initialize
analyzer = VisualizationAnalyzer(
    use_cache=True,      # Enable caching
    track_tokens=True    # Track token usage
)

# Analyze
df = pd.read_csv("data.csv")
result = analyzer.analyze_and_recommend(
    problem="What factors affect housing prices?",
    df=df
)

# Result structure:
# {
#   "analysis": "Brief analysis...",
#   "visualizations": [
#     {
#       "viz_type": "scatter_plot",
#       "title": "Price vs Size",
#       "x_axis": "size",
#       "y_axis": "price",
#       "color": "location",
#       "justification": "Shows correlation...",
#       "best_practices": [...]
#     },
#     ... 2 more visualizations
#   ]
# }
```

**Caching:**
```python
# First call - hits API
result1 = analyzer.analyze_and_recommend(problem, df)

# Second call with same data - uses cache
result2 = analyzer.analyze_and_recommend(problem, df)

# Force refresh (bypass cache)
result3 = analyzer.analyze_and_recommend(problem, df, force_refresh=True)

# Clear all cache
analyzer.clear_cache()
```

---

### `refiner.py` - Visualization Refiner

**Purpose:** Enhances selected visualizations with additional details.

**Key Features:**
- Adds professional styling
- Optimizes axis labels
- Suggests color palettes
- Adds annotations

**Usage:**
```python
from src.llm.refiner import VisualizationRefiner

refiner = VisualizationRefiner()

# Refine a selected visualization
enhanced = refiner.refine_visualization(
    viz_config=selected_viz,
    df=df
)

# Enhanced config includes:
# - axis_labels with units
# - color_palette (colorblind-safe)
# - figure_size
# - additional_params
```

---

## Configuration

### Environment Variables

Required in `.env`:
```bash
# Groq API Key (required)
GROQ_API_KEY=your_groq_api_key_here

# Optional settings
LLM_MODEL=llama-3.3-70b-versatile
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
```

---

## Performance

### Token Usage

**Average tokens per request:**
- Compact mode: ~400 tokens total (prompt + response)
- Detailed mode: ~700 tokens total
- **Recommendation: Use compact mode for production**

**Cost Estimates (Groq pricing):**
- Compact: ~$0.0001 per request
- Detailed: ~$0.0002 per request
- 1000 requests/day: ~$3/month (compact mode)

### Caching Benefits

- **First request:** ~1-2 seconds (API call)
- **Cached requests:** <0.1 seconds (instant)
- **Savings:** Avoid 100% of API costs for repeated queries

---

## Error Handling

All modules include comprehensive error handling:
```python
try:
    result = analyzer.analyze_and_recommend(problem, df)
except ValueError as e:
    # Data validation errors
    print(f"Invalid data: {e}")
except Exception as e:
    # API or parsing errors
    print(f"LLM error: {e}")
```

**Common Errors:**
- `ValueError: GROQ_API_KEY not found` → Set API key in `.env`
- `Groq API error: Rate limit` → Retry logic handles automatically
- `Failed to parse LLM response` → LLM returned invalid JSON

---

## Best Practices

1. **Always use caching in production**
```python
   analyzer = VisualizationAnalyzer(use_cache=True)
```

2. **Use compact prompts to save costs**
```python
   prompt = templates.analyze_problem_and_data(..., compact=True)
```

3. **Track tokens in development**
```python
   analyzer = VisualizationAnalyzer(track_tokens=True)
   # ... use analyzer ...
   analyzer.token_counter.print_stats()
```

4. **Handle errors gracefully**
```python
   try:
       result = analyzer.analyze_and_recommend(problem, df)
   except Exception as e:
       # Show user-friendly error
       st.error(f"Could not generate visualizations: {e}")
```

---

## Testing

Run tests:
```bash
pytest tests/unit/test_llm*.py -v
```

Test coverage:
```bash
pytest tests/unit/test_llm*.py --cov=src.llm
```

---

## Future Improvements

Potential enhancements:
- [ ] Support for more LLM providers (OpenAI, Claude)
- [ ] Streaming responses for faster UX
- [ ] Multi-language support
- [ ] Custom visualization types
- [ ] A/B testing different prompts

---

## Support

For issues or questions:
1. Check error messages carefully
2. Verify `.env` configuration
3. Check Groq API status
4. Review logs in `logs/` directory

---

**Last Updated:** January 2026  
**Version:** 1.0