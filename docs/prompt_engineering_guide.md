# Prompt Engineering Guide

## Overview

This guide documents the prompt engineering strategies used in this project and lessons learned through iteration.

---

## Core Principles

### 1. Token Efficiency
**Problem:** LLM API costs scale with tokens  
**Solution:** Compact prompts that maintain quality

**Before (467 tokens):**
```
You are an expert data visualization consultant with years of experience...
[lengthy instructions]
```

**After (245 tokens - 47% savings):**
```
Data viz expert: analyze & recommend 3 visualizations.
```

### 2. Structured Output
**Problem:** LLMs return inconsistent formats  
**Solution:** Explicit JSON schema in prompt
```
OUTPUT (JSON only):
{
  "visualizations": [
    {
      "viz_type": "scatter_plot",
      "title": "...",
      ...
    }
  ]
}
```

### 3. Clear Constraints
**Problem:** LLMs might suggest unsupported viz types  
**Solution:** Explicit list of allowed types
```
VIZ TYPES: scatter_plot, bar_chart, line_chart, histogram, box_plot, heatmap
```

---

## Iteration History

### Version 1.0 - Initial Prompt
**Tokens:** ~600  
**Quality:** Good but verbose  
**Issues:** 
- Too many examples
- Repetitive instructions
- High token cost

### Version 2.0 - Optimized
**Tokens:** ~250  
**Quality:** Same as v1.0  
**Improvements:**
- Removed redundant text
- Shortened examples
- Kept critical instructions

**Result:** 58% token reduction, same quality

---

## Best Practices Learned

### ✅ DO:
1. **Be explicit about output format**
```
   JSON only, no markdown
```

2. **Provide schema examples**
```json
   {"field": "value"}
```

3. **List constraints clearly**
```
   Return EXACTLY 3 visualizations
```

4. **Use structured sections**
```
   PROBLEM: ...
   DATA: ...
   TASK: ...
   OUTPUT: ...
```

### ❌ DON'T:
1. Over-explain (LLMs understand context)
2. Use flowery language ("please", "kindly")
3. Repeat instructions
4. Include unnecessary examples

---

## Temperature Settings

**For Visualization Generation:**
- **Temperature: 0.5-0.7** (balanced creativity & consistency)
- Too low (0.2): Repetitive suggestions
- Too high (0.9): Unpredictable, invalid outputs

**For Refinement:**
- **Temperature: 0.5** (more focused)

---

## Handling LLM Errors

### Invalid JSON Response
**Symptom:** LLM returns markdown code blocks  
**Solution:** Strip backticks before parsing
```python
if response.startswith("```json"):
    response = response[7:-3]
```

### Wrong Number of Visualizations
**Symptom:** LLM returns 1 or 2 instead of 3  
**Solution:** Validate and request retry
```python
if len(result['visualizations']) != 3:
    raise ValueError("Expected 3 visualizations")
```

### Missing Required Fields
**Symptom:** Visualization lacks 'justification' etc.  
**Solution:** Validate schema and provide defaults
```python
required_fields = ['viz_type', 'title', 'x_axis', 'y_axis']
for field in required_fields:
    if field not in viz:
        # Handle missing field
```

---

## Prompt Testing Strategy

### 1. Test with Edge Cases
- Empty dataset
- Single column
- All numeric columns
- All categorical columns
- Mixed types

### 2. Measure Consistency
Run same prompt 10 times, check:
- Always returns 3 visualizations
- Valid JSON every time
- Appropriate viz types

### 3. Validate Relevance
Human review: Do suggestions make sense?

---

## Cost Optimization

### Token Budget per Request
- **Prompt:** ~150-250 tokens (compact mode)
- **Response:** ~200-300 tokens
- **Total:** ~400-550 tokens per analysis

### Cost Calculation
```
Groq: $0.27 per 1M tokens
Per request: ~500 tokens = $0.000135
1000 requests = $0.135
```

### Caching Impact
- Cache hit rate: ~60-70% (same datasets)
- Effective cost: ~$0.00005 per request
- **Savings: 63% with caching**

---

## Future Improvements

1. **Few-Shot Learning**
   - Add 1-2 examples in prompt
   - May improve quality by 10-15%
   - Cost: +100 tokens per request

2. **Dynamic Prompt Selection**
   - Simple datasets → compact prompt
   - Complex datasets → detailed prompt
   - Adaptive token usage

3. **Multi-Turn Refinement**
   - Initial suggestions
   - User feedback
   - Refined recommendations
   - Better quality, higher cost

---

## Example Prompts

### Compact Prompt (Current)
```
Data viz expert: analyze & recommend 3 visualizations.

PROBLEM: What affects housing prices?

COLUMNS: price(float), size(int), location(categorical)

SAMPLE: [data preview]

TASK: Return 3 viz recommendations.

VIZ TYPES: scatter_plot, bar_chart, ...

OUTPUT (JSON only): {...}
```

### When to Use Detailed Prompt
- Very complex datasets (>20 columns)
- Unclear problem statements
- Need for explanatory analysis

---

**Last Updated:** January 2026  
**Maintained by:** Person 1 (LLM Lead)