"""Data profiling module for analyzing dataset characteristics."""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional


class DataProfiler:
    """Profile and analyze datasets to provide insights for visualization."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize profiler with a DataFrame.
        
        Args:
            df: Pandas DataFrame to profile
        """
        self.df = df
        self._profile_cache = None
    
    def generate_profile(self) -> Dict[str, Any]:
        """Generate comprehensive data profile.
        
        Returns:
            Dictionary containing complete dataset profile
        """
        if self._profile_cache is not None:
            return self._profile_cache
        
        profile = {
            "basic_info": self._get_basic_info(),
            "column_profiles": self._get_column_profiles(),
            "correlations": self._get_correlations(),
            "data_quality": self._get_data_quality(),
            "recommendations": self._get_recommendations()
        }
        
        self._profile_cache = profile
        return profile
    
    def _get_basic_info(self) -> Dict[str, Any]:
        """Get basic dataset information."""
        return {
            "n_rows": len(self.df),
            "n_columns": len(self.df.columns),
            "columns": list(self.df.columns),
            "memory_usage_mb": self.df.memory_usage(deep=True).sum() / (1024 * 1024),
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        }
    
    def _get_column_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Profile each column individually."""
        profiles = {}
        
        for col in self.df.columns:
            col_data = self.df[col]
            
            profile = {
                "name": col,
                "dtype": str(col_data.dtype),
                "n_unique": int(col_data.nunique()),
                "n_missing": int(col_data.isnull().sum()),
                "missing_percent": float((col_data.isnull().sum() / len(col_data)) * 100)
            }
            
            # Numeric column statistics
            if pd.api.types.is_numeric_dtype(col_data):
                profile.update({
                    "type": "numeric",
                    "min": float(col_data.min()) if not col_data.isnull().all() else None,
                    "max": float(col_data.max()) if not col_data.isnull().all() else None,
                    "mean": float(col_data.mean()) if not col_data.isnull().all() else None,
                    "median": float(col_data.median()) if not col_data.isnull().all() else None,
                    "std": float(col_data.std()) if not col_data.isnull().all() else None,
                    "has_outliers": self._detect_outliers(col_data),
                    "is_continuous": col_data.nunique() > 20
                })
            
            # Categorical/text column statistics
            elif pd.api.types.is_object_dtype(col_data):
                value_counts = col_data.value_counts()
                profile.update({
                    "type": "categorical" if col_data.nunique() < len(col_data) * 0.5 else "text",
                    "top_values": value_counts.head(5).to_dict(),
                    "n_categories": int(col_data.nunique()),
                    "most_common": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                    "most_common_freq": int(value_counts.iloc[0]) if len(value_counts) > 0 else None
                })
            
            # Datetime column statistics
            elif pd.api.types.is_datetime64_any_dtype(col_data):
                profile.update({
                    "type": "datetime",
                    "min_date": str(col_data.min()) if not col_data.isnull().all() else None,
                    "max_date": str(col_data.max()) if not col_data.isnull().all() else None,
                    "date_range_days": (col_data.max() - col_data.min()).days if not col_data.isnull().all() else None
                })
            
            # Boolean column statistics
            elif pd.api.types.is_bool_dtype(col_data):
                value_counts = col_data.value_counts()
                profile.update({
                    "type": "boolean",
                    "true_count": int(value_counts.get(True, 0)),
                    "false_count": int(value_counts.get(False, 0)),
                    "true_percent": float((value_counts.get(True, 0) / len(col_data)) * 100)
                })
            
            profiles[col] = profile
        
        return profiles
    
    def _get_correlations(self) -> Dict[str, Any]:
        """Calculate correlations between numeric columns."""
        numeric_df = self.df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) < 2:
            return {
                "has_correlations": False,
                "message": "Not enough numeric columns for correlation analysis"
            }
        
        corr_matrix = numeric_df.corr()
        
        # Find strong correlations (> 0.7 or < -0.7)
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    strong_correlations.append({
                        "column1": corr_matrix.columns[i],
                        "column2": corr_matrix.columns[j],
                        "correlation": float(corr_value),
                        "strength": "strong positive" if corr_value > 0 else "strong negative"
                    })
        
        return {
            "has_correlations": True,
            "correlation_matrix": corr_matrix.to_dict(),
            "strong_correlations": strong_correlations,
            "n_numeric_columns": len(numeric_df.columns)
        }
    
    def _get_data_quality(self) -> Dict[str, Any]:
        """Assess data quality issues."""
        quality = {
            "overall_quality": "good",
            "issues": [],
            "warnings": []
        }
        
        # Check for missing values
        total_missing = self.df.isnull().sum().sum()
        total_cells = len(self.df) * len(self.df.columns)
        missing_percent = (total_missing / total_cells) * 100
        
        if missing_percent > 50:
            quality["issues"].append(f"High missing values: {missing_percent:.1f}%")
            quality["overall_quality"] = "poor"
        elif missing_percent > 20:
            quality["warnings"].append(f"Moderate missing values: {missing_percent:.1f}%")
            quality["overall_quality"] = "fair"
        
        # Check for duplicate rows
        n_duplicates = self.df.duplicated().sum()
        if n_duplicates > 0:
            dup_percent = (n_duplicates / len(self.df)) * 100
            if dup_percent > 10:
                quality["issues"].append(f"High duplicate rows: {dup_percent:.1f}%")
            else:
                quality["warnings"].append(f"Duplicate rows found: {n_duplicates}")
        
        # Check for constant columns
        for col in self.df.columns:
            if self.df[col].nunique() == 1:
                quality["warnings"].append(f"Column '{col}' has only one unique value")
        
        # Check for very small dataset
        if len(self.df) < 10:
            quality["warnings"].append(f"Small dataset: only {len(self.df)} rows")
        
        quality["missing_percent"] = float(missing_percent)
        quality["n_duplicates"] = int(n_duplicates)
        
        return quality
    
    def _get_recommendations(self) -> List[str]:
        """Generate recommendations for visualization."""
        recommendations = []
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.df.select_dtypes(include=['object']).columns
        
        # Recommend based on column types
        if len(numeric_cols) >= 2:
            recommendations.append(
                "Consider scatter plots to explore relationships between numeric variables"
            )
            recommendations.append(
                "Correlation heatmap could reveal patterns between numeric columns"
            )
        
        if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
            recommendations.append(
                "Box plots or bar charts can compare numeric values across categories"
            )
        
        if len(numeric_cols) >= 1:
            recommendations.append(
                "Histograms can show distribution of numeric variables"
            )
        
        # Check for time series
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns
        if len(datetime_cols) >= 1 and len(numeric_cols) >= 1:
            recommendations.append(
                "Line charts are ideal for showing trends over time"
            )
        
        # Warn about data issues
        if self.df.isnull().sum().sum() > 0:
            recommendations.append(
                "Consider handling missing values before visualization"
            )
        
        return recommendations
    
    def _detect_outliers(self, series: pd.Series) -> bool:
        """Detect if a numeric series has outliers using IQR method.
        
        Args:
            series: Pandas Series
            
        Returns:
            True if outliers detected
        """
        if not pd.api.types.is_numeric_dtype(series):
            return False
        
        # Remove NaN values
        clean_series = series.dropna()
        
        if len(clean_series) < 4:
            return False
        
        Q1 = clean_series.quantile(0.25)
        Q3 = clean_series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = (clean_series < lower_bound) | (clean_series > upper_bound)
        
        return outliers.any()
    
    def get_summary_for_llm(self) -> str:
        """Get a concise summary formatted for LLM consumption.
        
        Returns:
            Formatted string summarizing the dataset
        """
        profile = self.generate_profile()
        
        summary_parts = [
            f"Dataset: {profile['basic_info']['n_rows']} rows × {profile['basic_info']['n_columns']} columns",
            f"\nColumns:",
        ]
        
        for col, col_profile in profile['column_profiles'].items():
            col_type = col_profile['type']
            missing = col_profile['missing_percent']
            
            if col_type == 'numeric':
                summary_parts.append(
                    f"  - {col} ({col_type}): "
                    f"range [{col_profile.get('min', 'N/A'):.2f} - {col_profile.get('max', 'N/A'):.2f}], "
                    f"mean {col_profile.get('mean', 'N/A'):.2f}"
                )
            elif col_type == 'categorical':
                summary_parts.append(
                    f"  - {col} ({col_type}): "
                    f"{col_profile['n_categories']} categories, "
                    f"most common: {col_profile.get('most_common', 'N/A')}"
                )
            else:
                summary_parts.append(f"  - {col} ({col_type})")
            
            if missing > 0:
                summary_parts[-1] += f" [{missing:.1f}% missing]"
        
        # Add quality issues
        if profile['data_quality']['issues']:
            summary_parts.append("\nData Quality Issues:")
            for issue in profile['data_quality']['issues']:
                summary_parts.append(f"  - {issue}")
        
        # Add correlations
        if profile['correlations']['has_correlations']:
            strong_corr = profile['correlations']['strong_correlations']
            if strong_corr:
                summary_parts.append("\nStrong Correlations:")
                for corr in strong_corr[:3]:  # Show top 3
                    summary_parts.append(
                        f"  - {corr['column1']} ↔ {corr['column2']}: "
                        f"{corr['correlation']:.2f} ({corr['strength']})"
                    )
        
        return "\n".join(summary_parts)


# Quick test
if __name__ == "__main__":
    # Create test data
    np.random.seed(42)
    test_df = pd.DataFrame({
        'price': np.random.randint(100, 500, 50),
        'size': np.random.randint(30, 150, 50),
        'rooms': np.random.randint(1, 6, 50),
        'location': np.random.choice(['Paris', 'Lyon', 'Marseille'], 50),
        'has_parking': np.random.choice([True, False], 50),
        'year_built': np.random.randint(1990, 2024, 50)
    })
    
    # Add some missing values
    test_df.loc[0:2, 'price'] = np.nan
    
    # Profile the data
    profiler = DataProfiler(test_df)
    profile = profiler.generate_profile()
    
    print("=" * 60)
    print("📊 DATA PROFILE REPORT")
    print("=" * 60)
    
    # Basic info
    print("\n🔍 Basic Information:")
    basic = profile['basic_info']
    print(f"   Rows: {basic['n_rows']}")
    print(f"   Columns: {basic['n_columns']}")
    print(f"   Memory: {basic['memory_usage_mb']:.2f} MB")
    
    # Column profiles
    print("\n📈 Column Profiles:")
    for col, col_prof in profile['column_profiles'].items():
        print(f"\n   {col} ({col_prof['type']}):")
        print(f"      Unique values: {col_prof['n_unique']}")
        print(f"      Missing: {col_prof['missing_percent']:.1f}%")
        
        if col_prof['type'] == 'numeric':
            print(f"      Range: [{col_prof['min']:.1f} - {col_prof['max']:.1f}]")
            print(f"      Mean: {col_prof['mean']:.1f}")
            print(f"      Outliers: {col_prof['has_outliers']}")
        elif col_prof['type'] == 'categorical':
            print(f"      Categories: {col_prof['n_categories']}")
            print(f"      Most common: {col_prof['most_common']} ({col_prof['most_common_freq']})")
    
    # Correlations
    print("\n🔗 Correlations:")
    if profile['correlations']['has_correlations']:
        strong = profile['correlations']['strong_correlations']
        if strong:
            for corr in strong:
                print(f"   {corr['column1']} ↔ {corr['column2']}: "
                      f"{corr['correlation']:.2f} ({corr['strength']})")
        else:
            print("   No strong correlations found")
    
    # Data quality
    print("\n✅ Data Quality:")
    quality = profile['data_quality']
    print(f"   Overall: {quality['overall_quality']}")
    print(f"   Missing: {quality['missing_percent']:.1f}%")
    print(f"   Duplicates: {quality['n_duplicates']}")
    
    if quality['issues']:
        print("   Issues:")
        for issue in quality['issues']:
            print(f"      - {issue}")
    
    if quality['warnings']:
        print("   Warnings:")
        for warning in quality['warnings']:
            print(f"      - {warning}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    for rec in profile['recommendations']:
        print(f"   - {rec}")
    
    # LLM Summary
    print("\n" + "=" * 60)
    print(" LLM SUMMARY")
    print("=" * 60)
    print(profiler.get_summary_for_llm())
    
    print("\n✅ Profiling complete!")