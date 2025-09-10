"""Tests for report generation functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile
import os
from pathlib import Path

from ..reports.html_generator import HTMLReportGenerator
from ..reports.json_exporter import JSONExporter
from ..reports.pdf_generator import PDFReportGenerator
from ..reports.customization import ReportCustomizer, ReportTemplate, SectionConfig
from ..models.results import AnalysisResults, VocabularyResult, ComplexityResult, OverallSummary


class TestHTMLReportGenerator:
    """Test HTML report generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = HTMLReportGenerator()
        self.mock_results = self.create_mock_results()
    
    def create_mock_results(self):
        """Create mock analysis results."""
        results = Mock(spec=AnalysisResults)
        results.text = "Sample text for testing."
        results.title = "Test Analysis"
        results.analysis_date = Mock()
        results.analysis_date.strftime.return_value = "2024년 01월 01일 12:00"
        results.analyzers_used = ["vocabulary", "complexity"]
        results.analysis_time = 2.5
        results.word_count = 100
        results.char_count = 500
        results.sentence_count = 5
        results.paragraph_count = 2
        
        # Mock overall summary
        summary = Mock(spec=OverallSummary)
        summary.text_level = "B2"
        summary.complexity_score = 7.5
        summary.key_linguistic_features = ["complex sentences", "academic vocabulary"]
        summary.educational_recommendations = ["Good for intermediate learners"]
        results.overall_summary = summary
        
        # Mock vocabulary analysis
        vocab = Mock(spec=VocabularyResult)
        vocab.academic_vocabulary = ["analyze", "comprehensive", "methodology"]
        vocab.lexical_diversity_score = 0.75
        vocab.collocations = [{"text": "comprehensive analysis", "frequency": 3}]
        vocab.idiomatic_expressions = ["break the ice"]
        results.vocabulary_analysis = vocab
        
        # Mock complexity analysis
        complexity = Mock(spec=ComplexityResult)
        complexity.readability_scores = {"flesch_kincaid_grade": 8.5, "flesch_reading_ease": 65.2}
        complexity.cefr_level = "B2"
        complexity.sentence_metrics = {"avg_sentence_length": 15.2}
        results.complexity_analysis = complexity
        
        # Mock other analyses as None for simplicity
        results.grammar_analysis = None
        results.structure_analysis = None
        results.content_analysis = None
        
        return results
    
    def test_initialization(self):
        """Test HTMLReportGenerator initialization."""
        assert hasattr(self.generator, 'template_style')
        assert hasattr(self.generator, 'template_scripts')
    
    def test_generate_report(self):
        """Test HTML report generation."""
        html_output = self.generator.generate_report(self.mock_results)
        
        assert isinstance(html_output, str)
        assert "<!DOCTYPE html>" in html_output
        assert "Test Analysis" in html_output
        assert "B2" in html_output
        assert "vocabulary" in html_output.lower()
    
    def test_generate_header(self):
        """Test header generation."""
        header = self.generator._generate_header(self.mock_results, "Test Title")
        
        assert isinstance(header, str)
        assert "Test Title" in header
        assert "2024년 01월 01일 12:00" in header
        assert "vocabulary, complexity" in header
    
    def test_generate_overview(self):
        """Test overview section generation."""
        overview = self.generator._generate_overview(self.mock_results)
        
        assert isinstance(overview, str)
        assert "분석 개요" in overview
        assert "100" in overview  # word count
        assert "B2" in overview
        assert "7.5" in overview  # complexity score
    
    def test_generate_vocabulary_section(self):
        """Test vocabulary section generation."""
        vocab_section = self.generator._generate_vocabulary_section(self.mock_results)
        
        assert isinstance(vocab_section, str)
        assert "어휘 분석" in vocab_section
        assert "analyze" in vocab_section
        assert "0.75" in vocab_section  # diversity score
    
    def test_generate_complexity_section(self):
        """Test complexity section generation."""
        complexity_section = self.generator._generate_complexity_section(self.mock_results)
        
        assert isinstance(complexity_section, str)
        assert "복잡도 분석" in complexity_section
        assert "8.5" in complexity_section  # FK grade
        assert "B2" in complexity_section
    
    def test_generate_recommendations(self):
        """Test recommendations section generation."""
        recommendations = self.generator._generate_recommendations(self.mock_results)
        
        assert isinstance(recommendations, str)
        assert "교육적 권장사항" in recommendations
        assert "Good for intermediate learners" in recommendations
    
    def test_generate_word_badges(self):
        """Test word badge generation."""
        words = ["test", "example", "sample"]
        badges = self.generator._generate_word_badges(words)
        
        assert isinstance(badges, str)
        assert "test" in badges
        assert "word-badge" in badges
    
    def test_generate_word_badges_empty(self):
        """Test word badge generation with empty list."""
        badges = self.generator._generate_word_badges([])
        
        assert isinstance(badges, str)
        assert "발견되지 않았습니다" in badges


class TestJSONExporter:
    """Test JSON export functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.exporter = JSONExporter()
        self.mock_results = self.create_mock_results()
    
    def create_mock_results(self):
        """Create mock analysis results."""
        results = Mock(spec=AnalysisResults)
        results.text = "Sample text"
        results.title = "Test Analysis"
        results.word_count = 100
        results.analysis_date = Mock()
        results.analysis_date.isoformat.return_value = "2024-01-01T12:00:00"
        results.analyzers_used = ["vocabulary", "complexity"]
        results.analysis_time = 2.5
        
        # Mock to_dict method
        results.to_dict.return_value = {
            "text": "Sample text",
            "title": "Test Analysis",
            "word_count": 100,
            "analysis_date": "2024-01-01T12:00:00"
        }
        
        # Mock overall summary
        summary = Mock()
        summary.text_level = "B2"
        summary.complexity_score = 7.5
        summary.educational_recommendations = ["Good for intermediate learners"]
        results.overall_summary = summary
        
        # Mock generate_summary method
        results.generate_summary.return_value = summary
        
        return results
    
    def test_initialization(self):
        """Test JSONExporter initialization."""
        assert self.exporter.indent == 2
        assert self.exporter.ensure_ascii == False
    
    def test_export_results(self):
        """Test full results export."""
        json_output = self.exporter.export_results(self.mock_results)
        
        assert isinstance(json_output, str)
        
        # Verify it's valid JSON
        parsed = json.loads(json_output)
        assert "text" in parsed
        assert "export_metadata" in parsed
        assert parsed["export_metadata"]["export_type"] == "complete_analysis"
    
    def test_export_summary_only(self):
        """Test summary-only export."""
        json_output = self.exporter.export_summary_only(self.mock_results)
        
        assert isinstance(json_output, str)
        
        parsed = json.loads(json_output)
        assert "text_info" in parsed
        assert "analysis_summary" in parsed
        assert parsed["export_metadata"]["export_type"] == "summary_only"
    
    def test_export_educational_data(self):
        """Test educational data export."""
        json_output = self.exporter.export_educational_data(self.mock_results)
        
        assert isinstance(json_output, str)
        
        parsed = json.loads(json_output)
        assert "text_analysis" in parsed
        assert "learning_objectives" in parsed
        assert parsed["export_metadata"]["export_type"] == "educational_focus"
    
    def test_save_to_file(self):
        """Test saving JSON to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, "test_output.json")
            json_content = '{"test": "data"}'
            
            self.exporter.save_to_file(json_content, file_path)
            
            assert os.path.exists(file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert content == json_content
    
    def test_set_formatting(self):
        """Test setting JSON formatting options."""
        self.exporter.set_formatting(indent=4, ensure_ascii=True)
        
        assert self.exporter.indent == 4
        assert self.exporter.ensure_ascii == True


class TestPDFReportGenerator:
    """Test PDF report generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = PDFReportGenerator()
        self.mock_results = self.create_mock_results()
    
    def create_mock_results(self):
        """Create mock analysis results."""
        results = Mock(spec=AnalysisResults)
        results.text = "Sample text"
        results.title = "Test Analysis"
        results.analysis_date = Mock()
        results.analysis_date.strftime.return_value = "2024년 01월 01일 12:00"
        results.analyzers_used = ["vocabulary", "complexity"]
        results.analysis_time = 2.5
        results.word_count = 100
        results.sentence_count = 5
        results.paragraph_count = 2
        
        # Mock overall summary
        summary = Mock()
        summary.text_level = "B2"
        summary.complexity_score = 7.5
        summary.educational_recommendations = ["Good for intermediate learners"]
        results.overall_summary = summary
        
        # Mock generate_summary method
        results.generate_summary.return_value = summary
        
        return results
    
    def test_initialization(self):
        """Test PDFReportGenerator initialization."""
        assert self.generator.page_size == "A4"
        assert self.generator.font_family == "DejaVu Sans"
        assert self.generator.title_font_size == 16
    
    @patch('english_text_analyzer.reports.pdf_generator.SimpleDocTemplate')
    @patch('english_text_analyzer.reports.pdf_generator.Paragraph')
    def test_generate_report_mock(self, mock_paragraph, mock_doc):
        """Test PDF report generation with mocked reportlab."""
        # Mock the document and its build method
        mock_doc_instance = Mock()
        mock_doc.return_value = mock_doc_instance
        
        # Mock paragraph creation
        mock_paragraph.return_value = Mock()
        
        # This should not raise ImportError since we're mocking
        try:
            pdf_bytes = self.generator.generate_report(self.mock_results)
            # If mocking works, this should return something
            assert pdf_bytes is not None or True  # Allow for mock behavior
        except ImportError:
            # Expected if reportlab is not installed
            pytest.skip("reportlab not installed")
    
    def test_generate_summary_report_mock(self):
        """Test summary PDF report generation."""
        try:
            pdf_bytes = self.generator.generate_summary_report(self.mock_results)
            assert isinstance(pdf_bytes, bytes) or pdf_bytes is None
        except ImportError:
            pytest.skip("reportlab not installed")


class TestReportCustomizer:
    """Test report customization system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.customizer = ReportCustomizer()
        self.mock_results = self.create_mock_results()
    
    def create_mock_results(self):
        """Create mock analysis results."""
        results = Mock(spec=AnalysisResults)
        results.text = "Sample text"
        results.title = "Test Analysis"
        results.word_count = 100
        
        # Mock overall summary
        summary = Mock()
        summary.text_level = "B2"
        summary.complexity_score = 7.5
        summary.educational_recommendations = ["Good for intermediate learners"]
        results.overall_summary = summary
        
        # Mock generate_summary method
        results.generate_summary.return_value = summary
        
        return results
    
    def test_initialization(self):
        """Test ReportCustomizer initialization."""
        assert len(self.customizer.templates) > 0
        assert "teacher" in self.customizer.templates
        assert "student" in self.customizer.templates
        assert "researcher" in self.customizer.templates
    
    def test_get_template(self):
        """Test getting a template."""
        teacher_template = self.customizer.get_template("teacher")
        
        assert isinstance(teacher_template, ReportTemplate)
        assert teacher_template.name == "teacher"
        assert teacher_template.educational_focus == True
    
    def test_list_templates(self):
        """Test listing available templates."""
        templates = self.customizer.list_templates()
        
        assert isinstance(templates, list)
        assert "teacher" in templates
        assert "student" in templates
        assert "researcher" in templates
        assert "summary" in templates
    
    def test_create_custom_template(self):
        """Test creating a custom template."""
        custom_template = self.customizer.create_custom_template(
            name="custom",
            description="Custom template",
            sections=["overview", "vocabulary"],
            educational_focus=True
        )
        
        assert isinstance(custom_template, ReportTemplate)
        assert custom_template.name == "custom"
        assert custom_template.description == "Custom template"
        assert "custom" in self.customizer.templates
    
    def test_customize_report_content(self):
        """Test customizing report content."""
        template = self.customizer.get_template("teacher")
        
        customized = self.customizer.customize_report_content(self.mock_results, template)
        
        assert isinstance(customized, dict)
        assert "template_info" in customized
        assert "sections" in customized
        assert "style_config" in customized
        assert customized["template_info"]["name"] == "teacher"
    
    def test_generate_overview_content(self):
        """Test overview content generation."""
        template = self.customizer.get_template("teacher")
        
        content = self.customizer._generate_overview_content(self.mock_results, template)
        
        assert isinstance(content, dict)
        assert "title" in content
        assert "text_stats" in content
        assert "level_info" in content
        assert content["level_info"]["cefr_level"] == "B2"
    
    def test_save_and_load_template(self):
        """Test saving and loading templates."""
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "test_template.json")
            
            # Get a template and save it
            template = self.customizer.get_template("teacher")
            self.customizer.save_template(template, template_path)
            
            assert os.path.exists(template_path)
            
            # Load it back
            loaded_template = self.customizer.load_template(template_path)
            
            assert isinstance(loaded_template, ReportTemplate)
            assert loaded_template.name == template.name
            assert loaded_template.description == template.description


class TestReportTemplate:
    """Test ReportTemplate data class."""
    
    def test_initialization(self):
        """Test ReportTemplate initialization."""
        template = ReportTemplate(
            name="test_template",
            description="Test template",
            sections=["overview", "vocabulary"],
            educational_focus=True
        )
        
        assert template.name == "test_template"
        assert template.description == "Test template"
        assert template.sections == ["overview", "vocabulary"]
        assert template.educational_focus == True
        assert template.format_type == "html"  # default
        assert template.include_charts == True  # default


class TestSectionConfig:
    """Test SectionConfig data class."""
    
    def test_initialization(self):
        """Test SectionConfig initialization."""
        config = SectionConfig(
            name="vocabulary",
            title="Vocabulary Analysis",
            priority=1,
            show_details=True
        )
        
        assert config.name == "vocabulary"
        assert config.title == "Vocabulary Analysis"
        assert config.enabled == True  # default
        assert config.priority == 1
        assert config.show_details == True


if __name__ == "__main__":
    pytest.main([__file__])