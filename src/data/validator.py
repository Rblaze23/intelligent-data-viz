"""Data validation utilities."""
import pandas as pd
from typing import List, Dict, Any


class DataValidator:
    """Validate data quality and suitability for visualization."""

    @staticmethod
    def check_data_quality(df: pd.DataFrame) -> Dict[str, Any]:
        """Check overall data quality.

        Args:
            df: Pandas DataFrame

        Returns:
            Dictionary with quality metrics
        """
        quality_report = {"is_valid": True, "warnings": [], "errors": []}

        # Check minimum rows
        if len(df) < 3:
            quality_report["errors"].append("Dataset has less than 3 rows")
            quality_report["is_valid"] = False

        # Check minimum columns
        if len(df.columns) < 2:
            quality_report["errors"].append("Dataset has less than 2 columns")
            quality_report["is_valid"] = False

        # Check for too many missing values
        missing_percent = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_percent > 50:
            quality_report["warnings"].append(
                f"High missing values: {missing_percent:.1f}%"
            )

        # Check for constant columns (all same value)
        for col in df.columns:
            if df[col].nunique() == 1:
                quality_report["warnings"].append(
                    f"Column '{col}' has only one unique value"
                )

        # Check for numeric columns
        numeric_cols = df.select_dtypes(include=["number"]).columns
        if len(numeric_cols) == 0:
            quality_report["warnings"].append("No numeric columns found")

        return quality_report

    @staticmethod
    def validate_visualization_columns(
        df: pd.DataFrame,
        viz_type: str,
        x_axis: str = None,
        y_axis: str = None,
        color: str = None,
    ) -> bool:
        """Validate that columns are appropriate for visualization type.

        Args:
            df: Pandas DataFrame
            viz_type: Type of visualization
            x_axis: X-axis column name
            y_axis: Y-axis column name
            color: Color column name

        Returns:
            True if valid

        Raises:
            ValueError: If validation fails
        """
        # Check columns exist
        required_cols = [col for col in [x_axis, y_axis, color] if col is not None]
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Columns not found: {', '.join(missing)}")

        # Validate based on viz type
        if viz_type == "scatter_plot":
            if not x_axis or not y_axis:
                raise ValueError("Scatter plot requires both x_axis and y_axis")

            # Both should be numeric
            if not pd.api.types.is_numeric_dtype(df[x_axis]):
                raise ValueError(
                    f"X-axis column '{x_axis}' must be numeric for scatter plot"
                )
            if not pd.api.types.is_numeric_dtype(df[y_axis]):
                raise ValueError(
                    f"Y-axis column '{y_axis}' must be numeric for scatter plot"
                )

        elif viz_type == "bar_chart":
            if not x_axis or not y_axis:
                raise ValueError("Bar chart requires both x_axis and y_axis")

        elif viz_type == "histogram":
            if not x_axis:
                raise ValueError("Histogram requires x_axis")
            if not pd.api.types.is_numeric_dtype(df[x_axis]):
                raise ValueError(
                    f"X-axis column '{x_axis}' must be numeric for histogram"
                )

        return True


# Quick test
if __name__ == "__main__":
    # Create test data
    df = pd.DataFrame(
        {
            "price": [100, 200, 150],
            "size": [50, 75, 60],
            "location": ["Paris", "Lyon", "Paris"],
        }
    )

    validator = DataValidator()

    # Check quality
    quality = validator.check_data_quality(df)
    print("✅ Quality Check:")
    print(f"   Valid: {quality['is_valid']}")
    print(f"   Warnings: {quality['warnings']}")
    print(f"   Errors: {quality['errors']}")

    # Validate visualization
    try:
        validator.validate_visualization_columns(
            df, viz_type="scatter_plot", x_axis="size", y_axis="price"
        )
        print("\n✅ Visualization validation passed!")
    except ValueError as e:
        print(f"\n❌ Validation error: {e}")
