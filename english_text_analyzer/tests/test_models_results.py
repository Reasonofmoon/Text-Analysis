"""Tests for results data models."""

import pytest
from datetime import datetime
import json

from ..models.results import (
    AnalysisResults, VocabularyResult, GrammarResult, 
    StructureResult, ContentResult, ComplexityResult, OverallSummary
)
from ..core.base_analyzer import AnalysisResult


class TestVocabularyResult:
    """Test VocabularyResult data model."""
    
    def test_initialization(self):
        """Test VocabularyResult initialization."""
        vocab_result = VocabularyResult()
        
        assert isinstance(vocab_result.difficulty_distribution, dict)
        assert isinstance(vocab_result.academic_vocabulary, list)
        assert isinstance(vocab_result.collocations, list)
        assert vocab_result.lexical_diversity_score == 0.0
    
    def test_with_data(self):
        """Test VocabularyResult with actual data."""
        vocab_result = VocabularyResult(
            difficulty_distribution={"A1": ["cat", "dog"], "B1": ["analyze"]},
            academic_vocabulary=["analyze", "comprehensive"],
            lexical_diversity_score=0.75
        )
        
        assert len(vocab_result.difficulty_distribution) == 2
        assert len(vocab_result.academic_vocabulary) == 2
        assert vocab_result.lexical_diversity_score == 0.75


class TestComplexityResult:
    """Test ComplexityResult data model."""
    
    def test_initialization(self):
        """Test ComplexityResult initialization."""
        complexity_result = ComplexityResult()
        
        assert isinstance(complexity_result.readability_scores, dict)
        assert complexity_result.cefr_level == "Unknown"
        assert isinstance(complexity_result.adaptation_recommendations, list)
    
    def test_with_data(self):
        """Test ComplexityResult with actual data."""
        complexity_result = ComplexityResult(
            readability_scores={"flesch_kincaid_grade": 8.5},
            cefr_level="B2",
            adaptation_recommendations=["Use simpler vocabulary"]
        )
        
        assert complexity_result.readability_scores["flesch_kincaid_grade"] == 8.5
        assert complexity_result.cefr_level == "B2"
        assert len(complexity_result.adaptation_recommendations) == 1


class TestAnalysisResults:
    """Test AnalysisResults container class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_text = "This is a sample text for testing purposes."
        self.results = AnalysisResults(
            text=self.sample_text,
            title="Test Analysis"
        )
    
    def test_initialization(self):
        """Test AnalysisResults initialization."""
        assert self.results.text == self.sample_text
        assert self.results.title == "Test Analysis"
        assert isinstance(self.results.analysis_date, datetime)
        assert self.results.word_count == 0  # Not calculated yet
        assert isinstance(self.results.analyzer_results, dict)
    
    def test_calculate_text_statistics(self):
        """Test text statistics calculation."""
        self.results.calculate_text_statistics()
        
        assert self.results.word_count > 0
        assert self.results.char_count > 0
        assert self.results.sentence_count >= 1
        assert self.results.paragraph_count >= 1
    
    def test_add_analyzer_result(self):
        """Test adding analyzer results."""
        # Create mock analyzer result
        analyzer_result = AnalysisResult(
            analyzer_name="test_analyzer",
            analysis_data={"test_key": "test_value"}
        )
        analyzer_result.results = {"test_key": "test_value"}
        
        self.results.add_analyzer_result(analyzer_result)
        
        assert "test_analyzer" in self.results.analyzer_results
        assert "test_analyzer" in self.results.analyzers_used
        assert self.results.get_analyzer_result("test_analyzer") == analyzer_result
    
    def test_add_complexity_analyzer_result(self):
        """Test adding complexity analyzer result."""
        complexity_data = {
            "readability_scores": {"flesch_kincaid_grade": 8.5},
            "cefr_level": "B2",
            "lexical_diversity": {"ttr": 0.75},
            "sentence_metrics": {"avg_sentence_length": 12.0},
            "syntactic_complexity": {"syntactic_complexity_score": 6.0},
            "information_density": {"content_word_ratio": 0.6},
            "recommendations": ["Use simpler vocabulary"]
        }
        
        analyzer_result = AnalysisResult(
            analyzer_name="complexity",
            analysis_data={"complexity_analysis": [complexity_data]}
        )
        analyzer_result.results = complexity_data
        
        self.results.add_analyzer_result(analyzer_result)
        
        assert self.results.complexity_analysis is not None
        assert self.results.complexity_analysis.cefr_level == "B2"
        assert self.results.complexity_analysis.readability_scores["flesch_kincaid_grade"] == 8.5
    
    def test_has_analyzer_result(self):
        """Test checking for analyzer results."""
        assert not self.results.has_analyzer_result("nonexistent")
        
        # Add a result
        analyzer_result = AnalysisResult(
            analyzer_name="test_analyzer",
            analysis_data={}
        )
        self.results.add_analyzer_result(analyzer_result)
        
        assert self.results.has_analyzer_result("test_analyzer")
    
    def test_generate_summary(self):
        """Test summary generation."""
        # Add some analyzer results first
        complexity_data = {
            "readability_scores": {"flesch_kincaid_grade": 8.5},
            "cefr_level": "B2",
            "lexical_diversity": {"ttr": 0.75},
            "sentence_metrics": {"avg_sentence_length": 12.0},
            "syntactic_complexity": {"syntactic_complexity_score": 6.0},
            "information_density": {"content_word_ratio": 0.6},
            "recommendations": ["Use simpler vocabulary"]
        }
        
        complexity_result = AnalysisResult(
            analyzer_name="complexity",
            analysis_data={"complexity_analysis": [complexity_data]}
        )
        complexity_result.results = complexity_data
        
        self.results.add_analyzer_result(complexity_result)
        self.results.calculate_text_statistics()
        
        summary = self.results.generate_summary()
        
        assert isinstance(summary, OverallSummary)
        assert summary.text_level == "B2"
        assert summary.complexity_score > 0
        assert len(summary.educational_recommendations) > 0
    
    def test_to_dict(self):
        """Test dictionary conversion."""
        self.results.calculate_text_statistics()
        result_dict = self.results.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict["text"] == self.sample_text
        assert result_dict["title"] == "Test Analysis"
        assert "analysis_date" in result_dict
        assert "word_count" in result_dict
    
    def test_to_json(self):
        """Test JSON conversion."""
        self.results.calculate_text_statistics()
        json_str = self.results.to_json()
        
        assert isinstance(json_str, str)
        
        # Verify it's valid JSON
        parsed = json.loads(json_str)
        assert parsed["text"] == self.sample_text
        assert parsed["title"] == "Test Analysis"
    
    def test_from_dict(self):
        """Test creating AnalysisResults from dictionary."""
        self.results.calculate_text_statistics()
        original_dict = self.results.to_dict()
        
        restored_results = AnalysisResults.from_dict(original_dict)
        
        assert restored_results.text == self.results.text
        assert restored_results.title == self.results.title
        assert restored_results.word_count == self.results.word_count
    
    def test_from_json(self):
        """Test creating AnalysisResults from JSON."""
        self.results.calculate_text_statistics()
        json_str = self.results.to_json()
        
        restored_results = AnalysisResults.from_json(json_str)
        
        assert restored_results.text == self.results.text
        assert restored_results.title == self.results.title
        assert restored_results.word_count == self.results.word_count


class TestOverallSummary:
    """Test OverallSummary data model."""
    
    def test_initialization(self):
        """Test OverallSummary initialization."""
        summary = OverallSummary()
        
        assert summary.text_level == "Unknown"
        assert isinstance(summary.dominant_themes, list)
        assert isinstance(summary.key_linguistic_features, list)
        assert isinstance(summary.educational_recommendations, list)
        assert summary.complexity_score == 0.0
        assert summary.confidence_score == 0.0
    
    def test_with_data(self):
        """Test OverallSummary with actual data."""
        summary = OverallSummary(
            text_level="B2",
            dominant_themes=["education", "technology"],
            key_linguistic_features=["complex sentences", "academic vocabulary"],
            educational_recommendations=["Good for intermediate learners"],
            complexity_score=7.5,
            confidence_score=0.85
        )
        
        assert summary.text_level == "B2"
        assert len(summary.dominant_themes) == 2
        assert len(summary.key_linguistic_features) == 2
        assert summary.complexity_score == 7.5
        assert summary.confidence_score == 0.85


if __name__ == "__main__":
    pytest.main([__file__])