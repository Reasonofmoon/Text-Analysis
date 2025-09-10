"""Tests for batch processing functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import tempfile
import os

from ..batch.processor import BatchProcessor, BatchItem, BatchProgress, BatchResults
from ..batch.comparator import BatchComparator, ComparisonMetrics, CollectionSummary
from ..core.analyzer import EnglishTextAnalyzer
from ..models.results import AnalysisResults


class TestBatchItem:
    """Test BatchItem data class."""
    
    def test_initialization(self):
        """Test BatchItem initialization."""
        item = BatchItem(
            id="test_1",
            text="Sample text",
            title="Test Title"
        )
        
        assert item.id == "test_1"
        assert item.text == "Sample text"
        assert item.title == "Test Title"
        assert isinstance(item.metadata, dict)


class TestBatchProgress:
    """Test BatchProgress tracking."""
    
    def test_initialization(self):
        """Test BatchProgress initialization."""
        progress = BatchProgress(total_items=10)
        
        assert progress.total_items == 10
        assert progress.completed_items == 0
        assert progress.failed_items == 0
        assert isinstance(progress.start_time, datetime)
    
    def test_completion_percentage(self):
        """Test completion percentage calculation."""
        progress = BatchProgress(total_items=10)
        progress.completed_items = 3
        
        assert progress.completion_percentage == 30.0
        
        # Test edge case
        progress_empty = BatchProgress(total_items=0)
        assert progress_empty.completion_percentage == 100.0
    
    def test_elapsed_time(self):
        """Test elapsed time calculation."""
        progress = BatchProgress(total_items=10)
        
        # Should be very small since just created
        elapsed = progress.elapsed_time
        assert elapsed >= 0
        assert elapsed < 1  # Should be less than 1 second


class TestBatchResults:
    """Test BatchResults data class."""
    
    def test_initialization(self):
        """Test BatchResults initialization."""
        results = BatchResults(
            batch_id="test_batch",
            total_items=5
        )
        
        assert results.batch_id == "test_batch"
        assert results.total_items == 5
        assert isinstance(results.successful_results, list)
        assert isinstance(results.failed_items, list)
        assert isinstance(results.start_time, datetime)
    
    def test_success_rate(self):
        """Test success rate calculation."""
        results = BatchResults(batch_id="test", total_items=10)
        
        # Add some mock successful results
        for i in range(7):
            mock_result = Mock()
            results.successful_results.append(mock_result)
        
        assert results.success_rate == 70.0
        
        # Test edge case
        empty_results = BatchResults(batch_id="empty", total_items=0)
        assert empty_results.success_rate == 100.0


class TestBatchProcessor:
    """Test BatchProcessor functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_analyzer = Mock(spec=EnglishTextAnalyzer)
        self.processor = BatchProcessor(self.mock_analyzer, max_workers=2)
    
    def test_initialization(self):
        """Test BatchProcessor initialization."""
        assert self.processor.analyzer == self.mock_analyzer
        assert self.processor.max_workers == 2
        assert self.processor.progress_callback is None
    
    def test_set_progress_callback(self):
        """Test setting progress callback."""
        callback = Mock()
        self.processor.set_progress_callback(callback)
        
        assert self.processor.progress_callback == callback
    
    def test_process_single_item(self):
        """Test processing a single item."""
        # Mock analyzer response
        mock_result = Mock(spec=AnalysisResults)
        mock_result.title = None
        mock_result.metadata = {}
        self.mock_analyzer.analyze_text.return_value = mock_result
        
        item = BatchItem(
            id="test_1",
            text="Sample text",
            title="Test Title"
        )
        
        result = self.processor._process_single_item(item)
        
        assert result == mock_result
        assert result.title == "Test Title"
        self.mock_analyzer.analyze_text.assert_called_once_with("Sample text")
    
    def test_process_texts(self):
        """Test processing list of texts."""
        texts = ["Text 1", "Text 2", "Text 3"]
        titles = ["Title 1", "Title 2", "Title 3"]
        
        # Mock analyzer responses
        mock_results = []
        for i in range(3):
            mock_result = Mock(spec=AnalysisResults)
            mock_result.title = None
            mock_result.metadata = {}
            mock_results.append(mock_result)
        
        self.mock_analyzer.analyze_text.side_effect = mock_results
        
        batch_results = self.processor.process_texts(texts, titles)
        
        assert isinstance(batch_results, BatchResults)
        assert batch_results.total_items == 3
        assert len(batch_results.successful_results) == 3
        assert self.mock_analyzer.analyze_text.call_count == 3
    
    def test_process_files(self):
        """Test processing files."""
        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            file_paths = []
            for i in range(2):
                file_path = os.path.join(temp_dir, f"test_{i}.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Content of file {i}")
                file_paths.append(file_path)
            
            # Mock analyzer responses
            mock_results = []
            for i in range(2):
                mock_result = Mock(spec=AnalysisResults)
                mock_result.title = None
                mock_result.metadata = {}
                mock_results.append(mock_result)
            
            self.mock_analyzer.analyze_text.side_effect = mock_results
            
            batch_results = self.processor.process_files(file_paths)
            
            assert isinstance(batch_results, BatchResults)
            assert batch_results.total_items == 2
            assert len(batch_results.successful_results) == 2
    
    def test_create_progress_monitor(self):
        """Test creating progress monitor."""
        monitor = self.processor.create_progress_monitor()
        
        assert callable(monitor)
        
        # Test calling the monitor
        progress = BatchProgress(total_items=10)
        progress.completed_items = 5
        
        # Should not raise an exception
        monitor(progress)


class TestComparisonMetrics:
    """Test ComparisonMetrics data class."""
    
    def test_initialization(self):
        """Test ComparisonMetrics initialization."""
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        metrics = ComparisonMetrics("test_metric", values)
        
        assert metrics.metric_name == "test_metric"
        assert metrics.values == values
        assert metrics.mean == 3.0
        assert metrics.median == 3.0
        assert metrics.min_value == 1.0
        assert metrics.max_value == 5.0
        assert metrics.range_value == 4.0
        assert metrics.std_dev > 0
    
    def test_empty_values(self):
        """Test ComparisonMetrics with empty values."""
        metrics = ComparisonMetrics("empty_metric", [])
        
        assert metrics.mean == 0.0
        assert metrics.median == 0.0
        assert metrics.std_dev == 0.0


class TestBatchComparator:
    """Test BatchComparator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.comparator = BatchComparator()
    
    def test_initialization(self):
        """Test BatchComparator initialization."""
        assert self.comparator.outlier_threshold == 2.0
    
    def create_mock_analysis_results(self, count=3):
        """Create mock analysis results for testing."""
        results = []
        
        for i in range(count):
            mock_result = Mock(spec=AnalysisResults)
            mock_result.word_count = 100 + i * 50
            mock_result.sentence_count = 5 + i
            
            # Mock overall summary
            mock_summary = Mock()
            mock_summary.text_level = ["A1", "B1", "C1"][i % 3]
            mock_summary.complexity_score = 3.0 + i * 2.0
            mock_summary.key_linguistic_features = [f"feature_{i}", "common_feature"]
            mock_result.overall_summary = mock_summary
            
            # Mock complexity analysis
            mock_complexity = Mock()
            mock_complexity.readability_scores = {"flesch_kincaid_grade": 5.0 + i * 3.0}
            mock_complexity.sentence_metrics = {"avg_sentence_length": 10.0 + i * 2.0}
            mock_result.complexity_analysis = mock_complexity
            
            # Mock vocabulary analysis
            mock_vocabulary = Mock()
            mock_vocabulary.academic_vocabulary = [f"word_{i}_1", f"word_{i}_2", "common_word"]
            mock_vocabulary.lexical_diversity_score = 0.5 + i * 0.1
            mock_vocabulary.difficulty_distribution = {
                "A1": [f"simple_{i}"],
                "B1": [f"medium_{i}"],
                "C1": [f"complex_{i}"]
            }
            mock_result.vocabulary_analysis = mock_vocabulary
            
            # Mock grammar analysis
            mock_grammar = Mock()
            mock_grammar.sentence_type_distribution = {"simple": 3 + i, "complex": 2 + i}
            mock_grammar.syntactic_complexity_score = 4.0 + i
            mock_grammar.complex_structures = [{"type": f"structure_{i}", "text": f"example_{i}"}]
            mock_grammar.tense_usage = {"present": [f"example_{i}"], "past": [f"example_{i}"]}
            mock_result.grammar_analysis = mock_grammar
            
            results.append(mock_result)
        
        return results
    
    def test_analyze_level_distribution(self):
        """Test CEFR level distribution analysis."""
        mock_results = self.create_mock_analysis_results(3)
        
        distribution = self.comparator._analyze_level_distribution(mock_results)
        
        assert isinstance(distribution, dict)
        assert "A1" in distribution
        assert "B1" in distribution
        assert "C1" in distribution
    
    def test_calculate_complexity_metrics(self):
        """Test complexity metrics calculation."""
        mock_results = self.create_mock_analysis_results(3)
        
        metrics = self.comparator._calculate_complexity_metrics(mock_results)
        
        assert isinstance(metrics, dict)
        assert "complexity_score" in metrics
        assert "word_count" in metrics
        assert "sentence_length" in metrics
        assert "readability" in metrics
        
        for metric in metrics.values():
            assert isinstance(metric, ComparisonMetrics)
    
    def test_analyze_vocabulary_patterns(self):
        """Test vocabulary pattern analysis."""
        mock_results = self.create_mock_analysis_results(3)
        
        patterns = self.comparator._analyze_vocabulary_patterns(mock_results)
        
        assert isinstance(patterns, dict)
        assert "common_academic_words" in patterns
        assert "average_diversity" in patterns
        assert "difficulty_trends" in patterns
        
        # Should find common words
        assert "common_word" in patterns["common_academic_words"]
    
    def test_analyze_grammar_patterns(self):
        """Test grammar pattern analysis."""
        mock_results = self.create_mock_analysis_results(3)
        
        patterns = self.comparator._analyze_grammar_patterns(mock_results)
        
        assert isinstance(patterns, dict)
        assert "sentence_type_trends" in patterns
        assert "average_complexity" in patterns
        assert "common_structures" in patterns
        assert "tense_patterns" in patterns
    
    def test_identify_common_features(self):
        """Test common feature identification."""
        mock_results = self.create_mock_analysis_results(3)
        
        common_features = self.comparator._identify_common_features(mock_results)
        
        assert isinstance(common_features, list)
        assert "common_feature" in common_features
    
    def test_detect_outliers(self):
        """Test outlier detection."""
        mock_results = self.create_mock_analysis_results(5)
        
        # Create metrics with some variation
        metrics = {
            "test_metric": ComparisonMetrics("test", [1.0, 2.0, 3.0, 4.0, 10.0])  # 10.0 is outlier
        }
        
        outliers = self.comparator._detect_outliers(mock_results, metrics)
        
        assert isinstance(outliers, list)
        # Should detect the outlier (index 4 with value 10.0)
        if outliers:
            assert any(outlier["text_index"] == 4 for outlier in outliers)
    
    def test_compare_batch_results(self):
        """Test complete batch comparison."""
        # Create mock batch results
        mock_batch_results = Mock()
        mock_batch_results.successful_results = self.create_mock_analysis_results(3)
        
        summary = self.comparator.compare_batch_results(mock_batch_results)
        
        assert isinstance(summary, CollectionSummary)
        assert summary.total_texts == 3
        assert len(summary.level_distribution) > 0
        assert len(summary.complexity_metrics) > 0
        assert len(summary.recommendations) > 0
    
    def test_generate_comparison_report(self):
        """Test comparison report generation."""
        summary = CollectionSummary(
            total_texts=3,
            level_distribution={"A1": 1, "B1": 1, "C1": 1},
            recommendations=["Test recommendation"]
        )
        
        report = self.comparator.generate_comparison_report(summary)
        
        assert isinstance(report, str)
        assert "텍스트 컬렉션 비교 분석 보고서" in report
        assert "총 텍스트 수: 3" in report
    
    def test_export_comparison_data(self):
        """Test comparison data export."""
        summary = CollectionSummary(
            total_texts=3,
            level_distribution={"A1": 1, "B1": 1, "C1": 1},
            recommendations=["Test recommendation"]
        )
        
        export_data = self.comparator.export_comparison_data(summary)
        
        assert isinstance(export_data, dict)
        assert "collection_info" in export_data
        assert "complexity_analysis" in export_data
        assert "patterns" in export_data
        assert "recommendations" in export_data


if __name__ == "__main__":
    pytest.main([__file__])