"""Tests for ComplexityAnalyzer."""

import pytest
from unittest.mock import Mock, patch
import langextract as lx

from ..analyzers.complexity import ComplexityAnalyzer
from ..core.base_analyzer import AnalysisResult


class TestComplexityAnalyzer:
    """Test cases for ComplexityAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = ComplexityAnalyzer()
        self.simple_text = "The cat sat on the mat. It was warm and sunny."
        self.complex_text = "The paradigmatic shift in contemporary linguistic theory necessitates a comprehensive reevaluation of traditional syntactic frameworks."
    
    def test_initialization(self):
        """Test analyzer initialization."""
        assert self.analyzer.name == "complexity"
        assert isinstance(self.analyzer.get_examples(), list)
        assert len(self.analyzer.get_examples()) > 0
    
    def test_get_examples(self):
        """Test example data generation."""
        examples = self.analyzer.get_examples()
        
        assert len(examples) == 3
        for example in examples:
            assert isinstance(example, lx.data.ExampleData)
            assert example.text
            assert len(example.extractions) > 0
    
    def test_get_prompt_description(self):
        """Test prompt description."""
        prompt = self.analyzer.get_prompt_description()
        
        assert isinstance(prompt, str)
        assert "complexity" in prompt.lower()
        assert "readability" in prompt.lower()
        assert "cefr" in prompt.lower()
    
    def test_calculate_readability_scores_simple(self):
        """Test readability calculation for simple text."""
        scores = self.analyzer.calculate_readability_scores(self.simple_text)
        
        assert "flesch_kincaid_grade" in scores
        assert "flesch_reading_ease" in scores
        assert scores["flesch_kincaid_grade"] < 5  # Should be low for simple text
        assert scores["flesch_reading_ease"] > 80  # Should be high for simple text
    
    def test_calculate_readability_scores_complex(self):
        """Test readability calculation for complex text."""
        scores = self.analyzer.calculate_readability_scores(self.complex_text)
        
        assert scores["flesch_kincaid_grade"] > 15  # Should be high for complex text
        assert scores["flesch_reading_ease"] < 30  # Should be low for complex text
    
    def test_calculate_readability_scores_empty(self):
        """Test readability calculation for empty text."""
        scores = self.analyzer.calculate_readability_scores("")
        
        assert scores["flesch_kincaid_grade"] == 0.0
        assert scores["flesch_reading_ease"] == 0.0
    
    def test_estimate_cefr_level(self):
        """Test CEFR level estimation."""
        # Simple text should be A1/A2
        simple_level = self.analyzer.estimate_cefr_level(self.simple_text)
        assert simple_level in ["A1", "A2"]
        
        # Complex text should be C1/C2
        complex_level = self.analyzer.estimate_cefr_level(self.complex_text)
        assert complex_level in ["C1", "C2"]
    
    def test_analyze_lexical_diversity(self):
        """Test lexical diversity analysis."""
        diversity = self.analyzer.analyze_lexical_diversity(self.simple_text)
        
        assert "ttr" in diversity
        assert "avg_word_length" in diversity
        assert "long_word_ratio" in diversity
        
        assert 0 <= diversity["ttr"] <= 1
        assert diversity["avg_word_length"] > 0
        assert 0 <= diversity["long_word_ratio"] <= 1
    
    def test_analyze_lexical_diversity_empty(self):
        """Test lexical diversity analysis for empty text."""
        diversity = self.analyzer.analyze_lexical_diversity("")
        
        assert diversity["ttr"] == 0.0
        assert diversity["avg_word_length"] == 0.0
        assert diversity["long_word_ratio"] == 0.0
    
    def test_analyze_syntactic_complexity(self):
        """Test syntactic complexity analysis."""
        complexity = self.analyzer.analyze_syntactic_complexity(self.complex_text)
        
        assert "avg_clauses_per_sentence" in complexity
        assert "complex_sentence_ratio" in complexity
        assert "syntactic_complexity_score" in complexity
        
        assert complexity["avg_clauses_per_sentence"] >= 1.0
        assert 0 <= complexity["complex_sentence_ratio"] <= 1.0
        assert 0 <= complexity["syntactic_complexity_score"] <= 10.0
    
    def test_calculate_information_density(self):
        """Test information density calculation."""
        density = self.analyzer.calculate_information_density(self.simple_text)
        
        assert "content_word_ratio" in density
        assert "information_density" in density
        
        assert 0 <= density["content_word_ratio"] <= 1.0
        assert density["information_density"] >= 0
    
    def test_generate_adaptation_recommendations(self):
        """Test adaptation recommendations generation."""
        # Create mock complexity data
        complexity_data = {
            "readability_scores": {"flesch_kincaid_grade": 15.0},
            "cefr_level": "C1",
            "syntactic_complexity": {"syntactic_complexity_score": 8.0}
        }
        
        recommendations = self.analyzer.generate_adaptation_recommendations(complexity_data)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) <= 8
        for rec in recommendations:
            assert isinstance(rec, str)
            assert len(rec) > 0
    
    def test_count_sentences(self):
        """Test sentence counting."""
        text = "First sentence. Second sentence! Third sentence?"
        count = self.analyzer._count_sentences(text)
        assert count == 3
        
        # Test with no sentences
        count = self.analyzer._count_sentences("no punctuation")
        assert count == 1  # Should return at least 1
    
    def test_count_words(self):
        """Test word counting."""
        text = "Hello world! This is a test."
        count = self.analyzer._count_words(text)
        assert count == 6
        
        # Test with empty text
        count = self.analyzer._count_words("")
        assert count == 0
    
    def test_count_syllables(self):
        """Test syllable counting."""
        # Test known syllable counts
        assert self.analyzer._count_syllables_in_word("cat") == 1
        assert self.analyzer._count_syllables_in_word("hello") == 2
        assert self.analyzer._count_syllables_in_word("beautiful") == 3
        assert self.analyzer._count_syllables_in_word("education") == 4
    
    def test_post_process_results(self):
        """Test post-processing of results."""
        # Create mock annotated document
        mock_doc = Mock()
        mock_doc.text = self.simple_text
        mock_doc.extractions = []
        
        result = self.analyzer.post_process_results(mock_doc)
        
        assert isinstance(result, AnalysisResult)
        assert result.analyzer_name == "complexity"
        assert result.analysis_type == "complexity_analysis"
        assert "readability_scores" in result.results
        assert "cefr_level" in result.results
        assert "recommendations" in result.results
    
    @patch('langextract.extract')
    def test_analyze_integration(self, mock_extract):
        """Test full analysis integration."""
        # Mock langextract response
        mock_doc = Mock()
        mock_doc.text = self.simple_text
        mock_doc.extractions = []
        mock_extract.return_value = mock_doc
        
        result = self.analyzer.analyze(self.simple_text)
        
        assert isinstance(result, AnalysisResult)
        assert result.analyzer_name == "complexity"
        mock_extract.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])