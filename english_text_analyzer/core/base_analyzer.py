"""Base analyzer abstract class for all analysis modules."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import langextract as lx


class AnalysisResult:
    """Base class for analysis results from individual analyzers."""
    
    def __init__(self, analyzer_name: str, analysis_data: Dict[str, Any]):
        self.analyzer_name = analyzer_name
        self.analysis_data = analysis_data
        self.metadata = {}
    
    def add_metadata(self, key: str, value: Any) -> None:
        """Add metadata to the analysis result."""
        self.metadata[key] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format."""
        return {
            "analyzer_name": self.analyzer_name,
            "analysis_data": self.analysis_data,
            "metadata": self.metadata
        }


class BaseAnalyzer(ABC):
    """Abstract base class for all text analyzers.
    
    This class defines the common interface that all analyzers must implement
    to work with the analysis orchestrator and langextract library.
    """
    
    def __init__(self, name: str):
        self.name = name
        self._examples = None
        self._prompt_description = None
    
    @abstractmethod
    def get_examples(self) -> List[lx.data.ExampleData]:
        """Return example data for this analyzer.
        
        Returns:
            List of ExampleData objects that demonstrate the expected
            analysis patterns for this analyzer.
        """
        pass
    
    @abstractmethod
    def get_prompt_description(self) -> str:
        """Return the prompt description for this analyzer.
        
        Returns:
            String describing what this analyzer should extract
            and how it should format the results.
        """
        pass
    
    @abstractmethod
    def analyze(self, text: str) -> AnalysisResult:
        """Perform analysis on the given text.
        
        Args:
            text: The text to analyze
            
        Returns:
            AnalysisResult containing the analysis findings
        """
        pass
    
    def post_process_results(self, raw_results: lx.data.AnnotatedDocument) -> AnalysisResult:
        """Post-process raw langextract results into structured format.
        
        Args:
            raw_results: Raw AnnotatedDocument from langextract
            
        Returns:
            Processed AnalysisResult with structured data
        """
        # Default implementation - can be overridden by specific analyzers
        extractions = {}
        for extraction in raw_results.extractions:
            extraction_class = extraction.extraction_class
            if extraction_class not in extractions:
                extractions[extraction_class] = []
            
            extractions[extraction_class].append({
                "text": extraction.extraction_text,
                "attributes": extraction.attributes,
                "start_index": getattr(extraction, 'start_index', None),
                "end_index": getattr(extraction, 'end_index', None)
            })
        
        return AnalysisResult(
            analyzer_name=self.name,
            analysis_data=extractions
        )
    
    def validate_text(self, text: str) -> bool:
        """Validate if text is suitable for this analyzer.
        
        Args:
            text: Text to validate
            
        Returns:
            True if text can be analyzed, False otherwise
        """
        if not text or not text.strip():
            return False
        
        # Minimum length check - can be overridden by specific analyzers
        return len(text.strip()) >= 10
    
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Return configuration schema for this analyzer.
        
        Returns:
            Dictionary describing configurable parameters
        """
        return {
            "enabled": {
                "type": "boolean",
                "default": True,
                "description": f"Enable/disable {self.name} analyzer"
            }
        }