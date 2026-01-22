"""Main analyzer for generating visualization recommendations."""
import json
from typing import Dict, Any
import pandas as pd
from src.llm.client import LLMClient
from src.llm.prompts import PromptTemplates


class VisualizationAnalyzer:
    """Analyzes problems and generates visualization recommendations using LLM."""

    def __init__(self):
        """Initialize the analyzer with LLM client."""
        self.llm = LLMClient()
        self.prompts = PromptTemplates()

    def analyze_and_recommend(self, problem: str, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze problem and dataset, return visualization recommendations.

        Args:
            problem: User's problem statement
            df: Pandas DataFrame with the data

        Returns:
            Dictionary with analysis and 3 visualization recommendations
        """
        # Prepare data information
        column_info = {col: str(df[col].dtype) for col in df.columns}
        sample_data = df.head(3).to_string()

        # Generate prompt
        prompt = self.prompts.analyze_problem_and_data(
            problem=problem, column_info=column_info, sample_data=sample_data
        )

        # Get LLM response
        response = self.llm.generate_completion(prompt)

        # Parse JSON response
        try:
            # Clean response (remove markdown code blocks if present)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]

            result = json.loads(response.strip())

            # Validate we have 3 visualizations
            if "visualizations" not in result:
                raise ValueError("Response missing 'visualizations' key")

            if len(result["visualizations"]) != 3:
                raise ValueError(
                    f"Expected 3 visualizations, got {len(result['visualizations'])}"
                )

            return result

        except json.JSONDecodeError as e:
            raise Exception(
                f"Failed to parse LLM response as JSON: {str(e)}\n\nResponse was:\n{response}"
            )
        except Exception as e:
            raise Exception(f"Error processing LLM response: {str(e)}")


# Quick test
if __name__ == "__main__":
    # Create sample data
    test_df = pd.DataFrame(
        {
            "price": [100, 200, 150, 300, 250],
            "size": [50, 75, 60, 100, 85],
            "location": ["Paris", "Lyon", "Paris", "Lyon", "Paris"],
        }
    )

    analyzer = VisualizationAnalyzer()

    try:
        result = analyzer.analyze_and_recommend(
            "What factors affect the price?", test_df
        )

        print("✅ Analysis successful!")
        print(f"\n📊 Analysis: {result['analysis']}")
        print(f"\n🎨 Generated {len(result['visualizations'])} visualizations:")
        for i, viz in enumerate(result["visualizations"], 1):
            print(f"\n  {i}. {viz['title']}")
            print(f"     Type: {viz['viz_type']}")
            print(f"     Justification: {viz['justification']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
