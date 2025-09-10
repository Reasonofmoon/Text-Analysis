"""Base classes for plugin architecture."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

from ..core.base_analyzer import BaseAnalyzer, AnalysisResult
from ..models.results import AnalysisResults


@dataclass
class PluginMetadata:
    """Metadata for a plugin."""
    name: str
    version: str
    description: str
    author: str
    email: Optional[str] = None
    website: Optional[str] = None
    license: str = "MIT"
    requires: List[str] = None
    created_date: Optional[datetime] = None
    
    def __post_init__(self):
        if self.requires is None:
            self.requires = []
        if self.created_date is None:
            self.created_date = datetime.now()


class BasePlugin(ABC):
    """Base class for all plugins."""
    
    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self._enabled = True
        self._initialized = False
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin with configuration.
        
        Args:
            config: Plugin configuration dictionary
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass
    
    def enable(self) -> None:
        """Enable the plugin."""
        self._enabled = True
    
    def disable(self) -> None:
        """Disable the plugin."""
        self._enabled = False
    
    @property
    def enabled(self) -> bool:
        """Check if plugin is enabled."""
        return self._enabled
    
    @property
    def initialized(self) -> bool:
        """Check if plugin is initialized."""
        return self._initialized
    
    def validate_requirements(self) -> List[str]:
        """Validate plugin requirements.
        
        Returns:
            List of missing requirements
        """
        missing = []
        for requirement in self.metadata.requires:
            try:
                __import__(requirement)
            except ImportError:
                missing.append(requirement)
        return missing


class AnalyzerPlugin(BasePlugin):
    """Base class for analyzer plugins."""
    
    @abstractmethod
    def create_analyzer(self) -> BaseAnalyzer:
        """Create and return the analyzer instance.
        
        Returns:
            BaseAnalyzer instance
        """
        pass
    
    @abstractmethod
    def get_analyzer_name(self) -> str:
        """Get the name of the analyzer.
        
        Returns:
            Analyzer name
        """
        pass


class ProcessorPlugin(BasePlugin):
    """Base class for result processor plugins."""
    
    @abstractmethod
    def process_results(self, results: AnalysisResults) -> AnalysisResults:
        """Process analysis results.
        
        Args:
            results: Analysis results to process
            
        Returns:
            Processed analysis results
        """
        pass
    
    @abstractmethod
    def get_processor_name(self) -> str:
        """Get the name of the processor.
        
        Returns:
            Processor name
        """
        pass


class ExporterPlugin(BasePlugin):
    """Base class for export format plugins."""
    
    @abstractmethod
    def export_results(self, results: AnalysisResults, output_path: str, **kwargs) -> None:
        """Export results in the plugin's format.
        
        Args:
            results: Analysis results to export
            output_path: Path where to save the export
            **kwargs: Additional export options
        """
        pass
    
    @abstractmethod
    def get_format_name(self) -> str:
        """Get the name of the export format.
        
        Returns:
            Format name
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Get the file extension for this format.
        
        Returns:
            File extension (including dot)
        """
        pass


class ValidationPlugin(BasePlugin):
    """Base class for validation plugins."""
    
    @abstractmethod
    def validate_text(self, text: str) -> Dict[str, Any]:
        """Validate input text.
        
        Args:
            text: Text to validate
            
        Returns:
            Validation results dictionary
        """
        pass
    
    @abstractmethod
    def validate_results(self, results: AnalysisResults) -> Dict[str, Any]:
        """Validate analysis results.
        
        Args:
            results: Results to validate
            
        Returns:
            Validation results dictionary
        """
        pass