"""Prompt templates for LLM-based visualization generation."""
import json
from typing import Dict


class PromptTemplates:
    """Collection of prompt templates for visualization tasks."""

    @staticmethod
    def analyze_problem_and_data(
        problem: str, column_info: Dict[str, str], sample_data: str
    ) -> str:
        """Generate prompt for analyzing problem and recommending visualizations.

        Args:
            problem: User's problem statement
            column_info: Dictionary of column names to data types
            sample_data: Sample rows from the dataset

        Returns:
            Formatted prompt for the LLM
        """
        columns_str = "\n".join(
            [f"- {col}: {dtype}" for col, dtype in column_info.items()]
        )

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
