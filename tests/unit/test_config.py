import pytest
import os
from src.config.settings import validate_config, DEFAULT_LLM_MODEL


def test_validate_config_with_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    # Reload the module to pick up the env var
    import importlib
    import src.config.settings

    importlib.reload(src.config.settings)
    from src.config.settings import validate_config as reloaded_validate

    reloaded_validate()  # Should not raise


def test_validate_config_without_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    import importlib
    import src.config.settings

    importlib.reload(src.config.settings)
    from src.config.settings import validate_config as reloaded_validate

    with pytest.raises(ValueError, match="GROQ_API_KEY must be set"):
        reloaded_validate()


def test_constants():
    assert DEFAULT_LLM_MODEL == "llama3-8b-8192"
