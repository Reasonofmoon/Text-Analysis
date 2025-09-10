"""Tests for configuration management."""

import pytest
from unittest.mock import Mock, patch, mock_open
import tempfile
import os
import json
import yaml

from ..config.manager import ConfigManager
from ..config.settings import AnalysisConfig


class TestConfigManager:
    """Test ConfigManager functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config_manager = ConfigManager()
    
    def test_initialization(self):
        """Test ConfigManager initialization."""
        assert self.config_manager.config_path is None
        assert self.config_manager._config is None
        assert len(self.config_manager.DEFAULT_CONFIG_PATHS) > 0
        assert self.config_manager.ENV_PREFIX == "ETA_"
    
    def test_initialization_with_path(self):
        """Test ConfigManager initialization with config path."""
        config_manager = ConfigManager("/path/to/config.yaml")
        assert config_manager.config_path == "/path/to/config.yaml"
    
    @patch.dict(os.environ, {}, clear=True)
    def test_load_config_defaults(self):
        """Test loading default configuration."""
        config = self.config_manager.load_config()
        
        assert isinstance(config, AnalysisConfig)
        assert config.enabled_analyzers  # Should have default analyzers
        assert config.model_name  # Should have default model
    
    def test_load_config_from_file(self):
        """Test loading configuration from file."""
        config_data = {
            "api_key": "test_key",
            "model_name": "test_model",
            "enabled_analyzers": ["vocabulary", "grammar"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            config = self.config_manager.load_config(config_path)
            
            assert config.api_key == "test_key"
            assert config.model_name == "test_model"
            assert config.enabled_analyzers == ["vocabulary", "grammar"]
        finally:
            os.unlink(config_path)
    
    def test_load_config_yaml(self):
        """Test loading YAML configuration."""
        config_data = {
            "api_key": "yaml_test_key",
            "model_name": "yaml_model",
            "enabled_analyzers": ["vocabulary"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            config = self.config_manager.load_config(config_path)
            
            assert config.api_key == "yaml_test_key"
            assert config.model_name == "yaml_model"
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {
        'ETA_API_KEY': 'env_test_key',
        'ETA_MODEL_NAME': 'env_model',
        'ETA_VOCABULARY_CONFIG__ENABLE_CEFR_ANALYSIS': 'true'
    })
    def test_apply_env_overrides(self):
        """Test environment variable overrides."""
        config = self.config_manager.load_config()
        
        assert config.api_key == "env_test_key"
        assert config.model_name == "env_model"
        # Test nested override
        assert config.vocabulary_config.enable_cefr_analysis == True
    
    def test_parse_env_value(self):
        """Test environment value parsing."""
        # Test boolean values
        assert self.config_manager._parse_env_value("true") == True
        assert self.config_manager._parse_env_value("false") == False
        assert self.config_manager._parse_env_value("yes") == True
        assert self.config_manager._parse_env_value("no") == False
        
        # Test numeric values
        assert self.config_manager._parse_env_value("42") == 42
        assert self.config_manager._parse_env_value("3.14") == 3.14
        
        # Test JSON values
        assert self.config_manager._parse_env_value('["a", "b"]') == ["a", "b"]
        assert self.config_manager._parse_env_value('{"key": "value"}') == {"key": "value"}
        
        # Test string values
        assert self.config_manager._parse_env_value("simple_string") == "simple_string"
    
    def test_deep_merge(self):
        """Test deep dictionary merging."""
        base = {
            "level1": {
                "level2": {
                    "key1": "value1",
                    "key2": "value2"
                },
                "other": "data"
            }
        }
        
        override = {
            "level1": {
                "level2": {
                    "key2": "new_value2",
                    "key3": "value3"
                }
            },
            "new_key": "new_value"
        }
        
        result = self.config_manager._deep_merge(base, override)
        
        assert result["level1"]["level2"]["key1"] == "value1"  # preserved
        assert result["level1"]["level2"]["key2"] == "new_value2"  # overridden
        assert result["level1"]["level2"]["key3"] == "value3"  # added
        assert result["level1"]["other"] == "data"  # preserved
        assert result["new_key"] == "new_value"  # added
    
    def test_get_config(self):
        """Test getting current configuration."""
        # First call should load config
        config1 = self.config_manager.get_config()
        assert isinstance(config1, AnalysisConfig)
        
        # Second call should return cached config
        config2 = self.config_manager.get_config()
        assert config1 is config2
    
    def test_save_config(self):
        """Test saving configuration."""
        config = AnalysisConfig()
        config.api_key = "test_save_key"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            self.config_manager.save_config(config, config_path)
            
            # Verify file was created and contains correct data
            assert os.path.exists(config_path)
            
            with open(config_path, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data["api_key"] == "test_save_key"
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)
    
    def test_create_default_config_file(self):
        """Test creating default configuration file."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            config_path = f.name
        
        try:
            self.config_manager.create_default_config_file(config_path)
            
            assert os.path.exists(config_path)
            
            # Load and verify it's a valid config
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            
            assert "enabled_analyzers" in config_data
            assert "model_name" in config_data
        finally:
            if os.path.exists(config_path):
                os.unlink(config_path)
    
    def test_get_analyzer_config(self):
        """Test getting analyzer-specific configuration."""
        config = self.config_manager.load_config()
        
        vocab_config = self.config_manager.get_analyzer_config("vocabulary")
        assert isinstance(vocab_config, dict)
        
        # Test invalid analyzer
        with pytest.raises(ValueError):
            self.config_manager.get_analyzer_config("nonexistent")
    
    def test_is_analyzer_enabled(self):
        """Test checking if analyzer is enabled."""
        config = self.config_manager.load_config()
        
        # Test with default enabled analyzers
        for analyzer in config.enabled_analyzers:
            assert self.config_manager.is_analyzer_enabled(analyzer)
        
        # Test with disabled analyzer
        assert not self.config_manager.is_analyzer_enabled("nonexistent_analyzer")
    
    def test_get_enabled_analyzers(self):
        """Test getting list of enabled analyzers."""
        analyzers = self.config_manager.get_enabled_analyzers()
        
        assert isinstance(analyzers, list)
        assert len(analyzers) > 0
        
        # Should return a copy, not the original list
        original_config = self.config_manager.get_config()
        analyzers.append("test_analyzer")
        assert "test_analyzer" not in original_config.enabled_analyzers
    
    def test_update_config(self):
        """Test updating configuration."""
        # Load initial config
        self.config_manager.load_config()
        
        # Update with new values
        updates = {
            "api_key": "updated_key",
            "model_name": "updated_model"
        }
        
        self.config_manager.update_config(updates)
        
        updated_config = self.config_manager.get_config()
        assert updated_config.api_key == "updated_key"
        assert updated_config.model_name == "updated_model"
    
    def test_update_config_validation_error(self):
        """Test update config with validation error."""
        self.config_manager.load_config()
        
        # Try to update with invalid data
        invalid_updates = {
            "enabled_analyzers": "not_a_list"  # Should be a list
        }
        
        with pytest.raises(ValueError):
            self.config_manager.update_config(invalid_updates)
    
    def test_reset_to_defaults(self):
        """Test resetting configuration to defaults."""
        # Load and modify config
        config = self.config_manager.load_config()
        original_api_key = config.api_key
        
        self.config_manager.update_config({"api_key": "modified_key"})
        assert self.config_manager.get_config().api_key == "modified_key"
        
        # Reset to defaults
        self.config_manager.reset_to_defaults()
        
        reset_config = self.config_manager.get_config()
        assert reset_config.api_key == original_api_key
    
    def test_get_config_summary(self):
        """Test getting configuration summary."""
        config = self.config_manager.load_config()
        summary = self.config_manager.get_config_summary()
        
        assert isinstance(summary, dict)
        assert "enabled_analyzers" in summary
        assert "api_configuration" in summary
        assert "processing_options" in summary
        assert "output_configuration" in summary
        
        # Check API configuration
        api_config = summary["api_configuration"]
        assert "has_api_key" in api_config
        assert "model_name" in api_config
        assert "max_retries" in api_config
    
    @patch('builtins.open', mock_open(read_data='invalid json'))
    def test_load_file_invalid_json(self):
        """Test loading invalid JSON file."""
        result = self.config_manager._load_file("invalid.json")
        assert result == {}
    
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_file_not_found(self):
        """Test loading non-existent file."""
        result = self.config_manager._load_file("nonexistent.json")
        assert result == {}
    
    def test_load_config_nonexistent_path(self):
        """Test loading config with non-existent path."""
        config = self.config_manager.load_config("/nonexistent/path/config.json")
        
        # Should fall back to defaults
        assert isinstance(config, AnalysisConfig)


if __name__ == "__main__":
    pytest.main([__file__])