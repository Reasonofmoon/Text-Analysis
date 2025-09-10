"""Configuration manager for handling configuration loading and validation."""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import yaml

from .settings import AnalysisConfig


class ConfigManager:
    """Manages configuration loading, validation, and environment integration."""
    
    DEFAULT_CONFIG_PATHS = [
        "english_text_analyzer_config.yaml",
        "english_text_analyzer_config.yml", 
        "english_text_analyzer_config.json",
        "config/english_text_analyzer.yaml",
        "config/english_text_analyzer.yml",
        "config/english_text_analyzer.json",
        ".english_text_analyzer.yaml",
        ".english_text_analyzer.yml",
        ".english_text_analyzer.json"
    ]
    
    ENV_PREFIX = "ETA_"  # English Text Analyzer
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        self._config: Optional[AnalysisConfig] = None
    
    def load_config(self, config_path: Optional[str] = None) -> AnalysisConfig:
        """Load configuration from file or create default configuration.
        
        Args:
            config_path: Optional path to configuration file
            
        Returns:
            AnalysisConfig instance
        """
        if config_path:
            self.config_path = config_path
        
        # Try to load from specified path or default paths
        config_dict = self._load_config_dict()
        
        # Apply environment variable overrides
        config_dict = self._apply_env_overrides(config_dict)
        
        # Create configuration object
        if config_dict:
            self._config = AnalysisConfig.from_dict(config_dict)
        else:
            self._config = AnalysisConfig()  # Use defaults
        
        # Validate configuration
        errors = self._config.validate()
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(error_msg)
        
        self.logger.info(f"Configuration loaded successfully from {self.config_path or 'defaults'}")
        return self._config
    
    def get_config(self) -> AnalysisConfig:
        """Get current configuration, loading if necessary."""
        if self._config is None:
            return self.load_config()
        return self._config
    
    def save_config(self, config: AnalysisConfig, file_path: str) -> None:
        """Save configuration to file.
        
        Args:
            config: Configuration to save
            file_path: Path where to save the configuration
        """
        config.save_to_file(file_path)
        self.logger.info(f"Configuration saved to {file_path}")
    
    def create_default_config_file(self, file_path: str) -> None:
        """Create a default configuration file.
        
        Args:
            file_path: Path where to create the configuration file
        """
        default_config = AnalysisConfig()
        self.save_config(default_config, file_path)
    
    def _load_config_dict(self) -> Dict[str, Any]:
        """Load configuration dictionary from file."""
        # If specific path provided, try to load it
        if self.config_path:
            if Path(self.config_path).exists():
                return self._load_file(self.config_path)
            else:
                self.logger.warning(f"Specified config file not found: {self.config_path}")
                return {}
        
        # Try default paths
        for path in self.DEFAULT_CONFIG_PATHS:
            if Path(path).exists():
                self.config_path = path
                return self._load_file(path)
        
        self.logger.info("No configuration file found, using defaults")
        return {}
    
    def _load_file(self, file_path: str) -> Dict[str, Any]:
        """Load configuration from a specific file."""
        path = Path(file_path)
        
        try:
            if path.suffix.lower() in ['.yaml', '.yml']:
                with open(path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f) or {}
        except Exception as e:
            self.logger.error(f"Failed to load configuration from {file_path}: {e}")
            return {}
    
    def _apply_env_overrides(self, config_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to configuration.
        
        Environment variables should be prefixed with ETA_ and use double
        underscores to separate nested keys. For example:
        - ETA_API_KEY -> api_key
        - ETA_VOCABULARY_CONFIG__ENABLE_CEFR_ANALYSIS -> vocabulary_config.enable_cefr_analysis
        """
        env_overrides = {}
        
        for key, value in os.environ.items():
            if key.startswith(self.ENV_PREFIX):
                # Remove prefix and convert to lowercase
                config_key = key[len(self.ENV_PREFIX):].lower()
                
                # Handle nested keys (double underscore separator)
                if '__' in config_key:
                    parts = config_key.split('__')
                    current = env_overrides
                    for part in parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    current[parts[-1]] = self._parse_env_value(value)
                else:
                    env_overrides[config_key] = self._parse_env_value(value)
        
        # Merge environment overrides with config dict
        return self._deep_merge(config_dict, env_overrides)
    
    def _parse_env_value(self, value: str) -> Any:
        """Parse environment variable value to appropriate type."""
        # Try to parse as JSON first (for lists, dicts, etc.)
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        
        # Try boolean values
        if value.lower() in ('true', 'yes', '1', 'on'):
            return True
        elif value.lower() in ('false', 'no', '0', 'off'):
            return False
        
        # Try numeric values
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries."""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def get_analyzer_config(self, analyzer_name: str) -> Dict[str, Any]:
        """Get configuration for a specific analyzer.
        
        Args:
            analyzer_name: Name of the analyzer
            
        Returns:
            Configuration dictionary for the analyzer
        """
        config = self.get_config()
        
        analyzer_config_map = {
            'vocabulary': config.vocabulary_config,
            'grammar': config.grammar_config,
            'structure': config.structure_config,
            'content': config.content_config,
            'complexity': config.complexity_config
        }
        
        if analyzer_name not in analyzer_config_map:
            raise ValueError(f"Unknown analyzer: {analyzer_name}")
        
        return analyzer_config_map[analyzer_name].__dict__
    
    def is_analyzer_enabled(self, analyzer_name: str) -> bool:
        """Check if an analyzer is enabled in the configuration.
        
        Args:
            analyzer_name: Name of the analyzer
            
        Returns:
            True if analyzer is enabled, False otherwise
        """
        config = self.get_config()
        return analyzer_name in config.enabled_analyzers
    
    def get_enabled_analyzers(self) -> List[str]:
        """Get list of enabled analyzers.
        
        Returns:
            List of enabled analyzer names
        """
        config = self.get_config()
        return config.enabled_analyzers.copy()
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update current configuration with new values.
        
        Args:
            updates: Dictionary of configuration updates
        """
        if self._config is None:
            self.load_config()
        
        # Apply updates
        current_dict = self._config.to_dict()
        updated_dict = self._deep_merge(current_dict, updates)
        
        # Create new config and validate
        self._config = AnalysisConfig.from_dict(updated_dict)
        errors = self._config.validate()
        if errors:
            error_msg = "Configuration update validation failed:\n" + "\n".join(f"  - {error}" for error in errors)
            raise ValueError(error_msg)
        
        self.logger.info("Configuration updated successfully")
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = AnalysisConfig()
        self.logger.info("Configuration reset to defaults")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration.
        
        Returns:
            Dictionary with configuration summary
        """
        config = self.get_config()
        
        return {
            "enabled_analyzers": config.enabled_analyzers,
            "api_configuration": {
                "has_api_key": bool(config.api_key),
                "model_name": config.model_name,
                "max_retries": config.max_retries
            },
            "processing_options": {
                "parallel_processing": config.parallel_processing,
                "cache_results": config.cache_results,
                "batch_size": config.batch_size
            },
            "output_configuration": {
                "default_format": config.output_config.default_format,
                "include_confidence_scores": config.output_config.include_confidence_scores,
                "include_examples": config.output_config.include_examples
            }
        }