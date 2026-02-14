# Changelog — Session Updates (February 14, 2026)

## New Features

### 1. BI Analyst Explanation Module (Step 5)
After dashboard generation, users can click **"🧠 Generate BI Analysis"** to produce a professional textual interpretation of the dashboard figures, written from the perspective of a senior BI analyst. The output includes an executive summary, key findings, trend analysis, anomalies, risk factors, recommendations, and next steps.

**Files:** `app.py`, `src/ui/components.py`

---

### 2. 3-Step Scaffolded LLM Prompting (Chained Analysis)
The BI analysis uses a **chained prompt scaffolding technique** where each step builds on the previous one:

| Step | Purpose | Output |
|------|---------|--------|
| **Step 1** | Data & problem understanding | Business context, hypotheses, key metrics |
| **Step 2** | Figure interpretation (receives Step 1 context) | Performance insights, segment analysis, figure-level findings |
| **Step 3** | Executive synthesis (receives Steps 1 + 2) | Executive summary, recommendations, risk factors, next steps |

This produces significantly richer analysis than a single-shot prompt because each step is focused on a narrower task with full context from prior steps.

**Files:** `src/llm/prompts.py` — added `bi_scaffold_step1_data_understanding()`, `bi_scaffold_step2_figure_interpretation()`, `bi_scaffold_step3_synthesis()`

---

### 3. Dynamic Dashboard Based on User Selection
The dashboard now uses the user's **selected visualization** as the primary figure instead of showing generic content regardless of which chart the user picked. The `selected_idx` parameter is threaded through the entire pipeline:

```
app.py (selected_idx) → vlm_enhancer.generate_dashboard_spec(selected_idx) → _generate_basic_dashboard_spec(selected_idx)
```

The selected visualization is displayed prominently as "📌 Primary", with remaining charts shown side-by-side as "Supporting Visualizations".

**Files:** `app.py`, `src/visualization/vlm_enhancer.py`

---

### 4. Real Plotly Figures in Dashboard
The dashboard section now renders the user's **actual generated Plotly charts** — not just supplementary KPI/metrics visuals. Each chart gets a unique key to prevent Streamlit duplicate element ID errors.

**Files:** `app.py`

---

### 5. BI Insights Display Component
Added `display_insights()` static method to `UIComponents` that renders the full BI analysis report with structured sections: executive summary, key findings, trend analysis, performance insights, segment analysis, anomalies & alerts, risk factors, recommendations, optimization opportunities, next steps, and an expandable data context section.

**Files:** `src/ui/components.py`

---

## Bug Fixes

### 6. Fixed `name 'prompt' is not defined`
**Root cause:** Stray code block inside `VisualizationAnalyzer.__init__()` in `analyzer.py` that called `self.llm.generate_completion(prompt)` where `prompt` was not yet defined. This was a misplaced code comment/snippet that executed at class instantiation.

**Fix:** Removed the 9-line stray block (lines 36–44). The actual LLM call already exists correctly inside `analyze_and_recommend()`.

**File:** `src/llm/analyzer.py`

---

### 7. Fixed `'LLMClient' object has no attribute 'initialized'`
**Root cause:** `app.py` checks `llm_client.initialized` and `analyzer.llm.initialized` but `LLMClient` never set that attribute.

**Fix:** Added `self.initialized = True` to `LLMClient.__init__()` after successful Groq client creation.

**File:** `src/llm/client.py`

---

### 8. Fixed `StreamlitDuplicateElementId`
**Root cause:** Multiple `st.plotly_chart()` calls in the dashboard rendered the same figure objects without unique keys.

**Fix:** Added unique `key` parameters: `dash_primary_{idx}` for the primary chart, `dash_support_{idx}` for supporting charts.

**File:** `app.py`

---

### 9. Fixed `_generate_basic_dashboard_spec() takes 4 positional arguments but 5 were given`
**Root cause:** `generate_dashboard()` in `app.py` passed `selected_idx` but `generate_dashboard_spec()` and `_generate_basic_dashboard_spec()` in `vlm_enhancer.py` didn't accept it.

**Fix:** Added `selected_idx=0` parameter to both method signatures and all 4 internal fallback call sites.

**File:** `src/visualization/vlm_enhancer.py`

---

## Pipeline Flow (After Changes)

```
Step 1️⃣  Upload Data         → CSV/Excel upload + preview
Step 2️⃣  Problem Statement   → User describes analysis goal
Step 3️⃣  AI Visualization    → LLM recommends 3 chart types → Plotly generates them
Step 4️⃣  Dashboard           → VLM builds dashboard spec with selected chart as primary
Step 5️⃣  BI Analysis (NEW)   → 3-step scaffolded LLM produces analyst report
Step 6️⃣  Export              → PNG / HTML export of selected visualization
```

---

## Files Modified Summary

| File | Type | Changes |
|------|------|---------|
| `app.py` | Feature + Fix | Added `generate_bi_analysis()`, `selected_idx` threading, BI section (Step 5), session state vars, export renumbered to Step 6, unique chart keys |
| `src/llm/prompts.py` | Feature | Added 3 scaffolded prompt methods + deprecated wrapper |
| `src/llm/client.py` | Fix | Added `self.initialized = True` |
| `src/llm/analyzer.py` | Fix | Removed misplaced stray code block from `__init__` |
| `src/visualization/vlm_enhancer.py` | Feature + Fix | Added `selected_idx` parameter throughout dashboard generation pipeline |
| `src/ui/components.py` | Feature | Added `display_insights()` method for rendering BI analysis |
