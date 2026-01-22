import pytest
from src.utils.exceptions import (
    IntelligentDataVizError,
    LLMError,
    DataProcessingError,
    error_to_user_message,
)


def test_custom_exceptions():
    with pytest.raises(IntelligentDataVizError):
        raise IntelligentDataVizError("Test error")

    with pytest.raises(LLMError):
        raise LLMError("LLM failed")

    with pytest.raises(DataProcessingError):
        raise DataProcessingError("Data issue")


def test_error_to_user_message():
    from src.utils.exceptions import ValidationError, APIError

    assert (
        error_to_user_message(LLMError())
        == "An error occurred with the AI analysis. Please try again."
    )
    assert (
        error_to_user_message(DataProcessingError())
        == "There was an issue processing your data. Check the file format."
    )
    assert (
        error_to_user_message(ValidationError())
        == "Data validation failed. Please check your input data."
    )
    assert (
        error_to_user_message(APIError())
        == "API communication error. Please check your connection."
    )
    assert (
        error_to_user_message(ValueError())
        == "An unexpected error occurred. Please contact support."
    )
