"""Main English text analyzer class."""

import logging
from typing import List, Optional, Dict, Any
import langextract as lx

from .orchestrator import AnalysisOrchestrator
from ..models.results import AnalysisResults
from ..config.settings import AnalysisConfig
from ..config.manager import ConfigManager


class EnglishTextAnalyzer:
    """Main class for English text analysis using langextract.
    
    This class provides a high-level interface for analyzing English texts
    across multiple dimensions including vocabulary, grammar, structure,
    content, and complexity.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None,
        config: Optional[AnalysisConfig] = None,
        config_path: Optional[str] = None
    ):
        """Initialize the English text analyzer.
        
        Args:
            api_key: API key for langextract (if None, will try to get from config or env)
            config: Analysis configuration (if None, will load from file or use defaults)
            config_path: Path to configuration file
        """
        # Set up configuration
        if config is None:
            config_manager = ConfigManager(config_path)
            self.config = config_manager.load_config()
        else:
            self.config = config
        
        # Set up API key
        self.api_key = api_key or self.config.api_key
        if not self.api_key:
            # Try to get from environment or langextract default
            try:
                # langextract will handle API key from environment
                pass
            except Exception:
                logging.warning("No API key provided. Some features may not work.")
        
        # Set up logging
        self._setup_logging()
        
        # Initialize orchestrator
        self.orchestrator = AnalysisOrchestrator(max_workers=self.config.max_workers)
        
        # Register analyzers (will be implemented in later tasks)
        self._register_analyzers()
        
        self.logger.info("EnglishTextAnalyzer initialized successfully")
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        log_level = getattr(logging, self.config.log_level.upper())
        
        # Configure logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # Add file handler if specified
        if self.config.log_file:
            file_handler = logging.FileHandler(self.config.log_file)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def _register_analyzers(self) -> None:
        """Register available analyzers with the orchestrator.
        
        This method will be expanded in later tasks as analyzers are implemented.
        """
        # Placeholder for analyzer registration
        # Analyzers will be registered here as they are implemented
        self.logger.info("Analyzer registration placeholder - will be implemented in later tasks")
    
    def analyze_text(
        self, 
        text: str,
        title: Optional[str] = None,
        analysis_types: Optional[List[str]] = None
    ) -> AnalysisResults:
        """Analyze a single English text.
        
        Args:
            text: The text to analyze
            title: Optional title for the text
            analysis_types: List of analysis types to perform (None = all enabled)
            
        Returns:
            AnalysisResults containing the analysis findings
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Validate text length
        text_length = len(text)
        if text_length < self.config.min_text_length:
            raise ValueError(f"Text too short (minimum {self.config.min_text_length} characters)")
        
        if text_length > self.config.max_text_length:
            raise ValueError(f"Text too long (maximum {self.config.max_text_length} characters)")
        
        # Determine which analyzers to use
        if analysis_types is None:
            enabled_analyzers = self.config.enabled_analyzers
        else:
            # Filter requested types by enabled analyzers
            enabled_analyzers = [
                analyzer for analyzer in analysis_types 
                if analyzer in self.config.enabled_analyzers
            ]
        
        if not enabled_analyzers:
            raise ValueError("No analyzers available for the requested analysis types")
        
        self.logger.info(f"Starting analysis with analyzers: {enabled_analyzers}")
        
        # Perform analysis using orchestrator
        results = self.orchestrator.coordinate_analysis(
            text=text,
            enabled_analyzers=enabled_analyzers,
            parallel=self.config.parallel_processing
        )
        
        # Set title and calculate text statistics
        results.title = title
        results.calculate_text_statistics()
        
        # Generate summary
        results.generate_summary()
        
        self.logger.info(f"Analysis completed in {results.analysis_time:.2f} seconds")
        return results
    
    def batch_analyze(
        self, 
        texts: List[str],
        titles: Optional[List[str]] = None,
        analysis_types: Optional[List[str]] = None
    ) -> List[AnalysisResults]:
        """Analyze multiple English texts.
        
        Args:
            texts: List of texts to analyze
            titles: Optional list of titles (must match length of texts)
            analysis_types: List of analysis types to perform (None = all enabled)
            
        Returns:
            List of AnalysisResults, one for each input text
        """
        if not texts:
            raise ValueError("No texts provided for analysis")
        
        if titles and len(titles) != len(texts):
            raise ValueError("Number of titles must match number of texts")
        
        results = []
        
        for i, text in enumerate(texts):
            title = titles[i] if titles else None
            
            try:
                result = self.analyze_text(
                    text=text,
                    title=title,
                    analysis_types=analysis_types
                )
                results.append(result)
                self.logger.info(f"Completed analysis {i+1}/{len(texts)}")
                
            except Exception as e:
                self.logger.error(f"Failed to analyze text {i+1}: {str(e)}")
                # Continue with other texts
                continue
        
        self.logger.info(f"Batch analysis completed: {len(results)}/{len(texts)} successful")
        return results
    
    def generate_report(
        self, 
        results: AnalysisResults,
        format: str = "html",
        output_path: Optional[str] = None
    ) -> str:
        """Generate a report from analysis results.
        
        Args:
            results: AnalysisResults to generate report from
            format: Report format ("html", "json", "pdf")
            output_path: Optional path to save the report
            
        Returns:
            Report content as string
        """
        if format.lower() == "json":
            report_content = results.to_json(indent=2)
        elif format.lower() == "html":
            # HTML report generation will be implemented in later tasks
            report_content = self._generate_html_report(results)
        elif format.lower() == "pdf":
            # PDF report generation will be implemented in later tasks
            report_content = self._generate_pdf_report(results)
        else:
            raise ValueError(f"Unsupported report format: {format}")
        
        # Save to file if path provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            self.logger.info(f"Report saved to {output_path}")
        
        return report_content
    
    def _generate_html_report(self, results: AnalysisResults) -> str:
        """Generate HTML report (placeholder implementation).
        
        This will be fully implemented in later tasks.
        """
        # Basic HTML report template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>English Text Analysis Report</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>English Text Analysis Report</h1>
            <h2>Text Information</h2>
            <p><strong>Title:</strong> {results.title or 'Untitled'}</p>
            <p><strong>Analysis Date:</strong> {results.analysis_date}</p>
            <p><strong>Word Count:</strong> {results.word_count}</p>
            <p><strong>Character Count:</strong> {results.char_count}</p>
            <p><strong>Analysis Time:</strong> {results.analysis_time:.2f} seconds</p>
            
            <h2>Analyzers Used</h2>
            <ul>
                {''.join(f'<li>{analyzer}</li>' for analyzer in results.analyzers_used)}
            </ul>
            
            <h2>Analysis Results</h2>
            <p><em>Detailed analysis results will be implemented in later tasks.</em></p>
            
            <h2>Raw Data (JSON)</h2>
            <pre>{results.to_json(indent=2)}</pre>
        </body>
        </html>
        """
        return html_content
    
    def _generate_pdf_report(self, results: AnalysisResults) -> str:
        """Generate PDF report (placeholder implementation).
        
        This will be fully implemented in later tasks.
        """
        # For now, return a message indicating PDF generation is not yet implemented
        return "PDF report generation will be implemented in later tasks."
    
    def get_available_analyzers(self) -> List[str]:
        """Get list of available analyzers.
        
        Returns:
            List of analyzer names
        """
        return self.orchestrator.get_available_analyzers()
    
    def get_enabled_analyzers(self) -> List[str]:
        """Get list of enabled analyzers from configuration.
        
        Returns:
            List of enabled analyzer names
        """
        return self.config.enabled_analyzers.copy()
    
    def is_analyzer_available(self, analyzer_name: str) -> bool:
        """Check if an analyzer is available.
        
        Args:
            analyzer_name: Name of the analyzer to check
            
        Returns:
            True if analyzer is available, False otherwise
        """
        return analyzer_name in self.get_available_analyzers()
    
    def get_configuration(self) -> AnalysisConfig:
        """Get current configuration.
        
        Returns:
            Current AnalysisConfig
        """
        return self.config