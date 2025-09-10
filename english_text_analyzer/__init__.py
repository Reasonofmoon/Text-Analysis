"""
English Text Analyzer - A comprehensive tool for analyzing English texts using langextract.

This package provides modular analysis capabilities for vocabulary, grammar, structure,
content, and complexity analysis of English texts for educational purposes.
"""

from .core.analyzer import EnglishTextAnalyzer
from .core.orchestrator import AnalysisOrchestrator
from .models.results import AnalysisResults
from .config.settings import AnalysisConfig

__version__ = "1.0.0"
__author__ = "English Text Analysis Team"

__all__ = [
    "EnglishTextAnalyzer",
    "AnalysisOrchestrator", 
    "AnalysisResults",
    "AnalysisConfig"
]