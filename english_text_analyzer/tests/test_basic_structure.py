"""Basic tests to verify project structure and imports."""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_package_imports():
    """Test that main package components can be imported."""
    try:
        from english_text_analyzer import EnglishTextAnalyzer, AnalysisOrchestrator, AnalysisResults, AnalysisConfig
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import main package components: {e}")


def test_core_imports():
    """Test that core components can be imported."""
    try:
        from english_text_analyzer.core import EnglishTextAnalyzer, AnalysisOrchestrator, BaseAnalyzer
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import core components: {e}")


def test_config_imports():
    """Test that configuration components can be imported."""
    try:
        from english_text_analyzer.config import AnalysisConfig, ConfigManager
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import config components: {e}")


def test_utils_imports():
    """Test that utility components can be imported."""
    try:
        from english_text_analyzer.utils import TextPreprocessor, EnglishTextAnalysisError
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import utility components: {e}")


def test_models_imports():
    """Test that model components can be imported."""
    try:
        from english_text_analyzer.models import AnalysisResults, AnalysisConfig
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import model components: {e}")


def test_analyzer_initialization():
    """Test that EnglishTextAnalyzer can be initialized."""
    try:
        from english_text_analyzer import EnglishTextAnalyzer
        
        # Test initialization without API key (should work but with warnings)
        analyzer = EnglishTextAnalyzer()
        assert analyzer is not None
        assert hasattr(analyzer, 'config')
        assert hasattr(analyzer, 'orchestrator')
        
    except Exception as e:
        pytest.fail(f"Failed to initialize EnglishTextAnalyzer: {e}")


def test_config_creation():
    """Test that configuration can be created."""
    try:
        from english_text_analyzer.config import AnalysisConfig
        
        config = AnalysisConfig()
        assert config is not None
        assert hasattr(config, 'enabled_analyzers')
        assert hasattr(config, 'parallel_processing')
        
        # Test validation
        errors = config.validate()
        assert isinstance(errors, list)
        
    except Exception as e:
        pytest.fail(f"Failed to create configuration: {e}")


def test_text_preprocessor():
    """Test that TextPreprocessor works."""
    try:
        from english_text_analyzer.utils import TextPreprocessor
        
        preprocessor = TextPreprocessor()
        
        # Test text cleaning
        test_text = "  This is a test.  "
        cleaned = preprocessor.clean_text(test_text)
        assert cleaned == "This is a test."
        
        # Test validation
        validation = preprocessor.validate_text("This is a test sentence.")
        assert isinstance(validation, dict)
        assert 'is_valid' in validation
        
    except Exception as e:
        pytest.fail(f"Failed to test TextPreprocessor: {e}")


if __name__ == "__main__":
    pytest.main([__file__])