class IntelligentDataVizError(Exception):
    """Base exception for the application."""

    pass


class LLMError(IntelligentDataVizError):
    """Error related to LLM operations."""

    pass


class DataProcessingError(IntelligentDataVizError):
    """Error in data processing."""

    pass


class VisualizationError(IntelligentDataVizError):
    """Error in visualization generation."""

    pass


class ConfigurationError(IntelligentDataVizError):
    """Error in configuration."""

    pass


class ExportError(IntelligentDataVizError):
    """Error in exporting visualizations."""

    pass


class ValidationError(IntelligentDataVizError):
    """Error in data validation."""

    pass


class APIError(IntelligentDataVizError):
    """Error in API communication."""

    pass


class VLMError(IntelligentDataVizError):
    """Error in VLM (Vision Language Model) operations."""

    pass


def error_to_user_message(error: Exception) -> str:
    """Convert exception to user-friendly message."""
    if isinstance(error, LLMError):
        return "An error occurred with the AI analysis. Please try again."
    elif isinstance(error, DataProcessingError):
        return "There was an issue processing your data. Check the file format."
    elif isinstance(error, VisualizationError):
        return "Could not generate the visualization. Try a different dataset."
    elif isinstance(error, ConfigurationError):
        return "Configuration error. Please check your settings."
    elif isinstance(error, ExportError):
        return "Failed to export the visualization. Try again."
    elif isinstance(error, ValidationError):
        return "Data validation failed. Please check your input data."
    elif isinstance(error, APIError):
        return "API communication error. Please check your connection."
    else:
        return "An unexpected error occurred. Please contact support."
