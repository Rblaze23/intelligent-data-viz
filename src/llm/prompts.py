"""Prompt templates for LLM-based visualization generation - Optimized for token efficiency."""
import json
from typing import Dict


class PromptTemplates:
    """Collection of prompt templates for visualization tasks."""
    
    @staticmethod
    def analyze_problem_and_data(
        problem: str,
        column_info: Dict[str, str],
        sample_data: str,
        compact: bool = True
    ) -> str:
        """Generate prompt for analyzing problem and recommending visualizations.
        
        Args:
            problem: User's problem statement
            column_info: Dictionary of column names to data types
            sample_data: Sample rows from the dataset
            compact: If True, use compact prompt (saves ~30% tokens)
            
        Returns:
            Formatted prompt for the LLM
        """
        if compact:
            return PromptTemplates._create_compact_prompt(problem, column_info, sample_data)
        else:
            return PromptTemplates._create_detailed_prompt(problem, column_info, sample_data)
    
    @staticmethod
    def _create_compact_prompt(
        problem: str,
        column_info: Dict[str, str],
        sample_data: str
    ) -> str:
        """Create compact, token-efficient prompt."""
        # Compact column info - just names and types
        columns_str = ", ".join([f"{col}({dtype})" for col, dtype in column_info.items()])
        
        # Limit sample data to first 200 chars
        sample_preview = sample_data[:200] + "..." if len(sample_data) > 200 else sample_data
        
        return f"""Data viz expert: analyze & recommend 3 visualizations.

PROBLEM: {problem}

COLUMNS: {columns_str}

SAMPLE:
{sample_preview}

TASK: Return 3 different viz recommendations following best practices.

VIZ TYPES: scatter_plot, bar_chart, line_chart, histogram, box_plot, heatmap

OUTPUT (JSON only):
{{
  "analysis": "brief insight",
  "visualizations": [
    {{
      "viz_type": "scatter_plot|bar_chart|line_chart|histogram|box_plot|heatmap",
      "title": "clear title",
      "x_axis": "column_name",
      "y_axis": "column_name",
      "color": "column_name or null",
      "group_by": null,
      "justification": "why this helps",
      "best_practices": ["practice1", "practice2"]
    }}
  ]
}}

Return 3 visualizations. JSON only, no markdown."""
    
    @staticmethod
    def _create_detailed_prompt(
        problem: str,
        column_info: Dict[str, str],
        sample_data: str
    ) -> str:
        """Create detailed prompt (uses more tokens but may give better results)."""
        columns_str = "\n".join([f"- {col}: {dtype}" for col, dtype in column_info.items()])
        
        return f"""You are an expert data visualization consultant. Analyze the problem and recommend visualizations.

**User's Problem:**
{problem}

**Dataset Columns:**
{columns_str}

**Sample Data (first 3 rows):**
{sample_data}

**Your Task:**
1. Analyze what the user wants to discover
2. Recommend EXACTLY 3 different visualization approaches
3. Each visualization must follow data visualization best practices

**Output Format (JSON only, no other text):**
{{
  "analysis": "Brief analysis of the user's question",
  "visualizations": [
    {{
      "viz_type": "scatter_plot",
      "title": "Descriptive title",
      "x_axis": "column_name",
      "y_axis": "column_name",
      "color": "optional_column_name or null",
      "group_by": "optional_column_name or null",
      "justification": "Why this visualization answers the question",
      "best_practices": ["practice1", "practice2", "practice3"]
    }},
    {{
      "viz_type": "bar_chart",
      "title": "Another title",
      "x_axis": "column_name",
      "y_axis": "column_name",
      "color": null,
      "group_by": null,
      "justification": "Why this is useful",
      "best_practices": ["practice1", "practice2"]
    }},
    {{
      "viz_type": "box_plot",
      "title": "Third option",
      "x_axis": "column_name",
      "y_axis": "column_name",
      "color": null,
      "group_by": null,
      "justification": "Why this helps",
      "best_practices": ["practice1", "practice2"]
    }}
  ]
}}

**Available viz_types:** scatter_plot, bar_chart, line_chart, histogram, box_plot, heatmap

Respond ONLY with valid JSON, no markdown code blocks, no additional text."""

    @staticmethod
    def bi_scaffold_step1_data_understanding(
        problem: str,
        column_info: Dict[str, str],
        sample_data: str,
        data_shape: tuple
    ) -> str:
        """Step 1 of BI scaffolded analysis: Data & problem understanding.

        Args:
            problem: User's problem statement
            column_info: Dictionary of column names to data types
            sample_data: Sample rows from the dataset
            data_shape: Tuple of (rows, cols)

        Returns:
            Formatted prompt for Step 1
        """
        columns_str = ", ".join([f"{col}({dtype})" for col, dtype in column_info.items()])

        return f"""You are a senior BI analyst. Perform Step 1: Data & Problem Understanding.

PROBLEM: {problem}
DATASET: {data_shape[0]} rows × {data_shape[1]} columns
COLUMNS: {columns_str}

SAMPLE DATA:
{sample_data[:500]}

Provide a structured analysis covering:
1. **Business Context**: What business domain does this data represent? What decisions could it inform?
2. **Key Hypotheses**: What are 3-5 testable hypotheses based on the problem and data?
3. **Key Metrics**: Which columns are the most important KPIs? What aggregations matter?
4. **Data Quality Notes**: Any concerns about missing values, outliers, or data types?
5. **Segmentation Opportunities**: What natural groupings exist in the data?

Be specific and reference actual column names. Output plain text (no JSON)."""

    @staticmethod
    def bi_scaffold_step2_figure_interpretation(
        step1_context: str,
        figure_descriptions: str
    ) -> str:
        """Step 2 of BI scaffolded analysis: Figure interpretation.

        Args:
            step1_context: Output from Step 1
            figure_descriptions: Text descriptions of the generated figures

        Returns:
            Formatted prompt for Step 2
        """
        return f"""You are a senior BI analyst. Perform Step 2: Figure Interpretation.

CONTEXT FROM STEP 1:
{step1_context}

GENERATED FIGURES:
{figure_descriptions}

Based on the business context from Step 1 and the figures above, provide:
1. **Performance Insights**: What do the figures reveal about overall performance?
2. **Segment Analysis**: How do different segments/categories compare?
3. **Trend Observations**: Any temporal patterns or directional trends?
4. **Distribution Findings**: What do distributions tell us about the data?
5. **Correlation Discoveries**: Any notable relationships between variables?
6. **Anomalies Detected**: Any outliers, unexpected patterns, or data points that stand out?

Reference specific figures and data points. Output plain text (no JSON)."""

    @staticmethod
    def bi_scaffold_step3_synthesis(
        step1_context: str,
        step2_context: str
    ) -> str:
        """Step 3 of BI scaffolded analysis: Executive synthesis.

        Args:
            step1_context: Output from Step 1
            step2_context: Output from Step 2

        Returns:
            Formatted prompt for Step 3
        """
        return f"""You are a senior BI analyst writing an executive report. Perform Step 3: Executive Synthesis.

DATA UNDERSTANDING (Step 1):
{step1_context}

FIGURE INTERPRETATION (Step 2):
{step2_context}

Synthesize all findings into a professional executive report with these sections:
1. **Executive Summary**: 3-4 sentence high-level overview of the most important findings
2. **Key Findings**: Top 5 data-driven findings with supporting evidence
3. **Trend Analysis**: Summary of trends, patterns, and their business implications
4. **Performance Insights**: How key metrics are performing against expectations
5. **Segment Analysis**: Performance breakdown by relevant categories/segments
6. **Anomalies & Alerts**: Any concerning patterns, outliers, or risks detected
7. **Risk Factors**: Business risks revealed by the data analysis
8. **Recommendations**: 3-5 specific, actionable recommendations ranked by impact
9. **Optimization Opportunities**: Areas where performance could be improved
10. **Next Steps**: Concrete follow-up analyses or actions to take

Write in professional business language. Be specific and data-driven. Output plain text (no JSON)."""

    @staticmethod
    def bi_analysis_prompt(
        problem: str,
        column_info: Dict[str, str],
        sample_data: str,
        data_shape: tuple,
        figure_descriptions: str
    ) -> str:
        """Deprecated: Single-shot BI analysis prompt. Use the 3-step scaffold instead.

        This is kept for backward compatibility but the scaffolded approach
        (step1 → step2 → step3) produces significantly richer analysis.
        """
        columns_str = ", ".join([f"{col}({dtype})" for col, dtype in column_info.items()])
        return f"""You are a senior BI analyst. Analyze this data and figures.

PROBLEM: {problem}
DATASET: {data_shape[0]} rows × {data_shape[1]} columns
COLUMNS: {columns_str}
SAMPLE: {sample_data[:300]}

FIGURES:
{figure_descriptions}

Provide executive summary, key findings, recommendations, and next steps.
Output plain text."""


# Quick test to compare token usage
if __name__ == "__main__":
    templates = PromptTemplates()
    
    test_columns = {
        'price': 'float64',
        'size': 'int64',
        'rooms': 'int64',
        'location': 'object',
        'year_built': 'int64'
    }
    
    test_sample = """price  size  rooms location  year_built
100    50    2     Paris     2010
200    75    3     Lyon      2015
150    60    2     Paris     2012"""
    
    test_problem = "What factors influence housing prices in French cities?"
    
    # Generate both versions
    compact = templates.analyze_problem_and_data(test_problem, test_columns, test_sample, compact=True)
    detailed = templates.analyze_problem_and_data(test_problem, test_columns, test_sample, compact=False)
    
    # Estimate tokens (rough estimate: 1 token ≈ 4 characters)
    compact_tokens = len(compact) // 4
    detailed_tokens = len(detailed) // 4
    savings = ((detailed_tokens - compact_tokens) / detailed_tokens) * 100
    
    print("=" * 60)
    print("TOKEN OPTIMIZATION COMPARISON")
    print("=" * 60)
    print(f"\n📊 Compact Prompt:")
    print(f"   Characters: {len(compact)}")
    print(f"   Est. Tokens: ~{compact_tokens}")
    print(f"\n📊 Detailed Prompt:")
    print(f"   Characters: {len(detailed)}")
    print(f"   Est. Tokens: ~{detailed_tokens}")
    print(f"\n💰 Savings: ~{savings:.1f}% fewer tokens with compact version")
    print(f"   (≈{detailed_tokens - compact_tokens} tokens saved per request)")
    
    print("\n" + "=" * 60)
    print("COMPACT PROMPT PREVIEW:")
    print("=" * 60)
    print(compact[:300] + "...\n")