"""Batch processing engine for multiple English texts."""

import asyncio
import concurrent.futures
from typing import List, Dict, Any, Optional, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import time
import logging

from ..core.analyzer import EnglishTextAnalyzer
from ..models.results import AnalysisResults
from ..config.settings import AnalysisConfig


@dataclass
class BatchItem:
    """Individual item in a batch processing job."""
    id: str
    text: str
    title: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchProgress:
    """Progress tracking for batch processing."""
    total_items: int
    completed_items: int = 0
    failed_items: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    current_item: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    
    @property
    def completion_percentage(self) -> float:
        """Calculate completion percentage."""
        if self.total_items == 0:
            return 100.0
        return (self.completed_items / self.total_items) * 100
    
    @property
    def elapsed_time(self) -> float:
        """Calculate elapsed time in seconds."""
        return (datetime.now() - self.start_time).total_seconds()
    
    def estimate_completion_time(self) -> None:
        """Estimate completion time based on current progress."""
        if self.completed_items > 0:
            avg_time_per_item = self.elapsed_time / self.completed_items
            remaining_items = self.total_items - self.completed_items
            remaining_seconds = avg_time_per_item * remaining_items
            self.estimated_completion = datetime.now() + timedelta(seconds=remaining_seconds)


@dataclass
class BatchResults:
    """Results from batch processing."""
    batch_id: str
    total_items: int
    successful_results: List[AnalysisResults] = field(default_factory=list)
    failed_items: List[Dict[str, Any]] = field(default_factory=list)
    processing_time: float = 0.0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate percentage."""
        if self.total_items == 0:
            return 100.0
        return (len(self.successful_results) / self.total_items) * 100


class BatchProcessor:
    """Engine for processing multiple texts in parallel with progress tracking."""
    
    def __init__(self, analyzer: EnglishTextAnalyzer, max_workers: int = 4):
        """Initialize batch processor.
        
        Args:
            analyzer: EnglishTextAnalyzer instance
            max_workers: Maximum number of parallel workers
        """
        self.analyzer = analyzer
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
        self.progress_callback: Optional[Callable[[BatchProgress], None]] = None
    
    def set_progress_callback(self, callback: Callable[[BatchProgress], None]) -> None:
        """Set callback function for progress updates.
        
        Args:
            callback: Function to call with BatchProgress updates
        """
        self.progress_callback = callback
    
    def process_batch(self, batch_items: List[BatchItem], 
                     batch_id: Optional[str] = None) -> BatchResults:
        """Process a batch of texts with parallel execution.
        
        Args:
            batch_items: List of BatchItem objects to process
            batch_id: Optional identifier for the batch
            
        Returns:
            BatchResults containing all processing results
        """
        if not batch_id:
            batch_id = f"batch_{int(time.time())}"
        
        start_time = datetime.now()
        progress = BatchProgress(total_items=len(batch_items))
        
        results = BatchResults(
            batch_id=batch_id,
            total_items=len(batch_items),
            start_time=start_time
        )
        
        self.logger.info(f"Starting batch processing: {batch_id} with {len(batch_items)} items")
        
        # Process items in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(self._process_single_item, item): item 
                for item in batch_items
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_item):
                item = future_to_item[future]
                progress.current_item = item.id
                
                try:
                    analysis_result = future.result()
                    results.successful_results.append(analysis_result)
                    progress.completed_items += 1
                    
                    self.logger.debug(f"Completed analysis for item: {item.id}")
                    
                except Exception as e:
                    error_info = {
                        "item_id": item.id,
                        "error": str(e),
                        "error_type": type(e).__name__
                    }
                    results.failed_items.append(error_info)
                    progress.failed_items += 1
                    
                    self.logger.error(f"Failed to process item {item.id}: {e}")
                
                # Update progress
                progress.estimate_completion_time()
                if self.progress_callback:
                    self.progress_callback(progress)
        
        # Finalize results
        results.end_time = datetime.now()
        results.processing_time = (results.end_time - start_time).total_seconds()
        
        self.logger.info(
            f"Batch processing completed: {batch_id}. "
            f"Success: {len(results.successful_results)}, "
            f"Failed: {len(results.failed_items)}, "
            f"Time: {results.processing_time:.2f}s"
        )
        
        return results
    
    def _process_single_item(self, item: BatchItem) -> AnalysisResults:
        """Process a single batch item.
        
        Args:
            item: BatchItem to process
            
        Returns:
            AnalysisResults for the item
        """
        try:
            # Analyze the text
            result = self.analyzer.analyze_text(item.text)
            
            # Add batch-specific metadata
            if not result.title and item.title:
                result.title = item.title
            
            # Add item metadata to results
            if hasattr(result, 'metadata'):
                result.metadata.update(item.metadata)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing item {item.id}: {e}")
            raise
    
    def process_texts(self, texts: List[str], titles: Optional[List[str]] = None,
                     batch_id: Optional[str] = None) -> BatchResults:
        """Process a list of texts (convenience method).
        
        Args:
            texts: List of text strings to analyze
            titles: Optional list of titles for the texts
            batch_id: Optional identifier for the batch
            
        Returns:
            BatchResults containing all processing results
        """
        # Create batch items
        batch_items = []
        for i, text in enumerate(texts):
            title = titles[i] if titles and i < len(titles) else None
            item = BatchItem(
                id=f"text_{i+1}",
                text=text,
                title=title
            )
            batch_items.append(item)
        
        return self.process_batch(batch_items, batch_id)
    
    def process_files(self, file_paths: List[str], batch_id: Optional[str] = None) -> BatchResults:
        """Process a list of text files.
        
        Args:
            file_paths: List of file paths to process
            batch_id: Optional identifier for the batch
            
        Returns:
            BatchResults containing all processing results
        """
        batch_items = []
        
        for i, file_path in enumerate(file_paths):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                item = BatchItem(
                    id=f"file_{i+1}",
                    text=text,
                    title=Path(file_path).stem,
                    metadata={"source_file": file_path}
                )
                batch_items.append(item)
                
            except Exception as e:
                self.logger.error(f"Failed to read file {file_path}: {e}")
                # Add as failed item
                error_item = BatchItem(
                    id=f"file_{i+1}_error",
                    text="",
                    title=Path(file_path).stem,
                    metadata={"source_file": file_path, "read_error": str(e)}
                )
                batch_items.append(error_item)
        
        return self.process_batch(batch_items, batch_id)
    
    async def process_batch_async(self, batch_items: List[BatchItem], 
                                 batch_id: Optional[str] = None) -> BatchResults:
        """Process batch asynchronously (for integration with async frameworks).
        
        Args:
            batch_items: List of BatchItem objects to process
            batch_id: Optional identifier for the batch
            
        Returns:
            BatchResults containing all processing results
        """
        loop = asyncio.get_event_loop()
        
        # Run the synchronous batch processing in a thread pool
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, 
                self.process_batch, 
                batch_items, 
                batch_id
            )
        
        return result
    
    def create_progress_monitor(self) -> Callable[[BatchProgress], None]:
        """Create a simple console progress monitor.
        
        Returns:
            Progress callback function
        """
        def progress_monitor(progress: BatchProgress):
            percentage = progress.completion_percentage
            elapsed = progress.elapsed_time
            
            status = f"Progress: {percentage:.1f}% ({progress.completed_items}/{progress.total_items})"
            if progress.failed_items > 0:
                status += f" | Failed: {progress.failed_items}"
            status += f" | Elapsed: {elapsed:.1f}s"
            
            if progress.estimated_completion:
                remaining = (progress.estimated_completion - datetime.now()).total_seconds()
                status += f" | ETA: {remaining:.0f}s"
            
            print(f"\r{status}", end="", flush=True)
            
            if progress.completed_items + progress.failed_items == progress.total_items:
                print()  # New line when complete
        
        return progress_monitor