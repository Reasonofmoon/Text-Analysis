"""Analysis orchestrator for coordinating multiple analyzers."""

from typing import Dict, List, Optional, Any
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from .base_analyzer import BaseAnalyzer, AnalysisResult
from ..models.results import AnalysisResults


class AnalysisOrchestrator:
    """Coordinates analysis across multiple analyzer modules.
    
    This class manages the registration and execution of different analyzers,
    handles parallel processing, and aggregates results.
    """
    
    def __init__(self, max_workers: int = 4):
        self.analyzers: Dict[str, BaseAnalyzer] = {}
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
    
    def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
        """Register an analyzer with the orchestrator.
        
        Args:
            analyzer: BaseAnalyzer instance to register
        """
        self.analyzers[analyzer.name] = analyzer
        self.logger.info(f"Registered analyzer: {analyzer.name}")
    
    def unregister_analyzer(self, analyzer_name: str) -> bool:
        """Unregister an analyzer.
        
        Args:
            analyzer_name: Name of analyzer to remove
            
        Returns:
            True if analyzer was removed, False if not found
        """
        if analyzer_name in self.analyzers:
            del self.analyzers[analyzer_name]
            self.logger.info(f"Unregistered analyzer: {analyzer_name}")
            return True
        return False
    
    def get_available_analyzers(self) -> List[str]:
        """Get list of registered analyzer names.
        
        Returns:
            List of analyzer names
        """
        return list(self.analyzers.keys())
    
    def coordinate_analysis(
        self, 
        text: str, 
        enabled_analyzers: Optional[List[str]] = None,
        parallel: bool = True
    ) -> AnalysisResults:
        """Coordinate analysis across multiple analyzers.
        
        Args:
            text: Text to analyze
            enabled_analyzers: List of analyzer names to use (None = all)
            parallel: Whether to run analyzers in parallel
            
        Returns:
            AnalysisResults containing aggregated results
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Determine which analyzers to use
        if enabled_analyzers is None:
            analyzers_to_use = self.analyzers
        else:
            analyzers_to_use = {
                name: analyzer for name, analyzer in self.analyzers.items()
                if name in enabled_analyzers
            }
        
        if not analyzers_to_use:
            raise ValueError("No analyzers available for analysis")
        
        # Validate text for each analyzer
        valid_analyzers = {}
        for name, analyzer in analyzers_to_use.items():
            if analyzer.validate_text(text):
                valid_analyzers[name] = analyzer
            else:
                self.logger.warning(f"Text validation failed for analyzer: {name}")
        
        if not valid_analyzers:
            raise ValueError("Text is not suitable for any available analyzers")
        
        # Run analysis
        start_time = time.time()
        
        if parallel and len(valid_analyzers) > 1:
            results = self._run_parallel_analysis(text, valid_analyzers)
        else:
            results = self._run_sequential_analysis(text, valid_analyzers)
        
        analysis_time = time.time() - start_time
        
        # Create aggregated results
        return self._create_analysis_results(text, results, analysis_time)
    
    def _run_parallel_analysis(
        self, 
        text: str, 
        analyzers: Dict[str, BaseAnalyzer]
    ) -> Dict[str, AnalysisResult]:
        """Run analyzers in parallel using ThreadPoolExecutor."""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all analysis tasks
            future_to_analyzer = {
                executor.submit(analyzer.analyze, text): name
                for name, analyzer in analyzers.items()
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_analyzer):
                analyzer_name = future_to_analyzer[future]
                try:
                    result = future.result()
                    results[analyzer_name] = result
                    self.logger.info(f"Completed analysis: {analyzer_name}")
                except Exception as e:
                    self.logger.error(f"Analysis failed for {analyzer_name}: {str(e)}")
                    # Continue with other analyzers
        
        return results
    
    def _run_sequential_analysis(
        self, 
        text: str, 
        analyzers: Dict[str, BaseAnalyzer]
    ) -> Dict[str, AnalysisResult]:
        """Run analyzers sequentially."""
        results = {}
        
        for name, analyzer in analyzers.items():
            try:
                result = analyzer.analyze(text)
                results[name] = result
                self.logger.info(f"Completed analysis: {name}")
            except Exception as e:
                self.logger.error(f"Analysis failed for {name}: {str(e)}")
                # Continue with other analyzers
        
        return results
    
    def _create_analysis_results(
        self, 
        text: str, 
        analyzer_results: Dict[str, AnalysisResult],
        analysis_time: float
    ) -> AnalysisResults:
        """Create aggregated AnalysisResults object."""
        return AnalysisResults(
            text=text,
            analyzer_results=analyzer_results,
            analysis_time=analysis_time,
            word_count=len(text.split()),
            char_count=len(text),
            analyzers_used=list(analyzer_results.keys())
        )
    
    def merge_results(self, results_list: List[AnalysisResults]) -> AnalysisResults:
        """Merge multiple AnalysisResults into a single result.
        
        Args:
            results_list: List of AnalysisResults to merge
            
        Returns:
            Merged AnalysisResults
        """
        if not results_list:
            raise ValueError("Cannot merge empty results list")
        
        if len(results_list) == 1:
            return results_list[0]
        
        # Combine all analyzer results
        merged_analyzer_results = {}
        merged_text_parts = []
        total_analysis_time = 0
        total_word_count = 0
        total_char_count = 0
        all_analyzers_used = set()
        
        for result in results_list:
            merged_analyzer_results.update(result.analyzer_results)
            merged_text_parts.append(result.text)
            total_analysis_time += result.analysis_time
            total_word_count += result.word_count
            total_char_count += result.char_count
            all_analyzers_used.update(result.analyzers_used)
        
        return AnalysisResults(
            text="\n\n".join(merged_text_parts),
            analyzer_results=merged_analyzer_results,
            analysis_time=total_analysis_time,
            word_count=total_word_count,
            char_count=total_char_count,
            analyzers_used=list(all_analyzers_used)
        )