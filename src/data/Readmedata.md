# Data Module Documentation

## Overview

This module handles all data processing, validation, and profiling for the intelligent visualization system.

## Components

### `processor.py` - CSV Processing

**Purpose:** Load and process CSV files with automatic format detection.

**Key Features:**
- Auto-detect encoding (UTF-8, Latin-1, CP1252, etc.)
- Auto-detect separator (comma, semicolon, tab, pipe)
- File size validation (default: 10MB max)
- Data cleaning and preprocessing

**Usage:**
```python
from src.data.processor import DataProcessor

processor = DataProcessor(max_file_size_mb=10)

# Load from file
df = processor.load_csv(file_path="data.csv")

# Load from bytes (file upload)
df = processor.load_csv(file_content=file_bytes)

# Get column information
col_info = processor.get_column_info(df)
# Returns: {'price': 'integer', 'location': 'categorical', ...}

# Get sample data
sample = processor.get_sample_data(df, n_rows=3)

# Clean data
df_clean = processor.clean_data(df, drop_missing=True)
```

**Supported Formats:**
- CSV with comma (,)
- CSV with semicolon (;)
- TSV with tabs (\t)
- PSV with pipes (|)

---

### `profiler.py` - Data Profiling

**Purpose:** Generate comprehensive data profiles for LLM context.

**Key Features:**
- Column-level statistics
- Data quality assessment
- Correlation detection
- Visualization recommendations

**Usage:**
```python
from src.data.profiler import DataProfiler

profiler = DataProfiler(df)

# Generate full profile
profile = profiler.generate_profile()

# Profile includes:
# - basic_info: shape, memory, dtypes
# - column_profiles: stats for each column
# - correlations: correlation matrix
# - data_quality: issues and warnings
# - recommendations: suggested viz types

# Get LLM-friendly summary
summary = profiler.get_summary_for_llm()
```

**Profile Structure:**
```python
{
  "basic_info": {
    "n_rows": 100,
    "n_columns": 5,
    "memory_usage_mb": 0.01
  },
  "column_profiles": {
    "price": {
      "type": "numeric",
      "min": 100,
      "max": 500,
      "mean": 250,
      "has_outliers": false
    },
    "location": {
      "type": "categorical",
      "n_categories": 3,
      "most_common": "Paris"
    }
  },
  "correlations": {...},
  "data_quality": {
    "overall_quality": "good",
    "missing_percent": 2.5,
    "issues": [],
    "warnings": ["Duplicate rows found: 2"]
  }
}
```

---

### `validator.py` - Data Validation

**Purpose:** Validate data quality and visualization compatibility.

**Key Features:**
- Data quality checks
- Column existence validation
- Visualization type validation

**Usage:**
```python
from src.data.validator import DataValidator

validator = DataValidator()

# Check data quality
quality = validator.check_data_quality(df)
# Returns: {'is_valid': True, 'warnings': [...], 'errors': [...]}

# Validate columns for visualization
validator.validate_visualization_columns(
    df,
    viz_type="scatter_plot",
    x_axis="size",
    y_axis="price"
)
```

---

## Data Quality Checks

The module performs these automatic checks:

### 1. File Validation
- ✅ File size within limits
- ✅ Valid CSV format
- ✅ Proper encoding
- ✅ Minimum 2 columns

### 2. Data Quality
- ✅ No excessive missing values (>50% = error)
- ✅ Duplicate detection
- ✅ Constant column detection
- ✅ Minimum row count (3 rows required)

### 3. Column Type Detection
```python
# Automatically detects:
- integer (int64, int32)
- float (float64, float32)
- categorical (object with <50% unique values)
- text (object with >50% unique values)
- datetime (datetime64)
- boolean (bool)
```

---

## Error Handling

Common errors and solutions:

**File Too Large:**
```python
# Error: "File too large. Maximum size: 10MB"
# Solution: Increase limit or reduce file size
processor = DataProcessor(max_file_size_mb=20)
```

**Encoding Issues:**
```python
# Automatically handled with fallbacks:
# UTF-8 → Latin-1 → CP1252 → ISO-8859-1
```

**Too Few Columns:**
```python
# Error: "CSV must have at least 2 columns"
# Solution: Ensure CSV has multiple columns
```

---

## Performance

### Processing Speed
- Small files (<100KB): <0.1s
- Medium files (1MB): ~0.5s
- Large files (10MB): ~2-3s

### Memory Usage
- DataFrame memory ≈ file size × 2-3
- 10MB CSV ≈ 20-30MB RAM usage

---

## Best Practices

1. **Always validate data before visualization**
```python
   quality = validator.check_data_quality(df)
   if not quality['is_valid']:
       # Handle errors
       for error in quality['errors']:
           print(f"Error: {error}")
```

2. **Profile data for better LLM context**
```python
   profiler = DataProfiler(df)
   summary = profiler.get_summary_for_llm()
   # Use summary in LLM prompts
```

3. **Clean data before analysis**
```python
   df_clean = processor.clean_data(df, drop_missing=False)
```

4. **Handle large files efficiently**
```python
   # For very large files, sample first
   df = processor.load_csv(file_path)
   if len(df) > 10000:
       df = df.sample(n=10000, random_state=42)
```

---

## Testing

Run data module tests:
```bash
pytest tests/unit/test_data*.py -v
```

---

**Last Updated:** January 2026  
**Version:** 1.0