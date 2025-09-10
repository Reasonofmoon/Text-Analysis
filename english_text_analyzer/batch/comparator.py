"""Comparative analysis features for batch processing results."""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import statistics
import numpy as np

from ..models.results import AnalysisResults
from .processor import BatchResults


@dataclass
class ComparisonMetrics:
    """Metrics for comparing multiple texts."""
    metric_name: str
    values: List[float]
    mean: float = 0.0
    median: float = 0.0
    std_dev: float = 0.0
    min_value: float = 0.0
    max_value: float = 0.0
    range_value: float = 0.0
    
    def __post_init__(self):
        if self.values:
            self.mean = statistics.mean(self.values)
            self.median = statistics.median(self.values)
            self.std_dev = statistics.stdev(self.values) if len(self.values) > 1 else 0.0
            self.min_value = min(self.values)
            self.max_value = max(self.values)
            self.range_value = self.max_value - self.min_value


@dataclass
class CollectionSummary:
    """Summary statistics for a collection of texts."""
    total_texts: int
    level_distribution: Dict[str, int] = field(default_factory=dict)
    complexity_metrics: Dict[str, ComparisonMetrics] = field(default_factory=dict)
    vocabulary_patterns: Dict[str, Any] = field(default_factory=dict)
    grammar_patterns: Dict[str, Any] = field(default_factory=dict)
    common_features: List[str] = field(default_factory=list)
    outliers: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class BatchComparator:
    """Comparative analysis engine for batch processing results."""
    
    def __init__(self):
        self.outlier_threshold = 2.0  # Standard deviations for outlier detection
    
    def compare_batch_results(self, batch_results: BatchResults) -> CollectionSummary:
        """Perform comprehensive comparative analysis on batch results.
        
        Args:
            batch_results: Results from batch processing
            
        Returns:
            CollectionSummary with comparative analysis
        """
        results = batch_results.successful_results
        
        if not results:
            return CollectionSummary(total_texts=0)
        
        summary = CollectionSummary(total_texts=len(results))
        
        # Analyze level distribution
        summary.level_distribution = self._analyze_level_distribution(results)
        
        # Calculate complexity metrics
        summary.complexity_metrics = self._calculate_complexity_metrics(results)
        
        # Analyze vocabulary patterns
        summary.vocabulary_patterns = self._analyze_vocabulary_patterns(results)
        
        # Analyze grammar patterns
        summary.grammar_patterns = self._analyze_grammar_patterns(results)
        
        # Identify common features
        summary.common_features = self._identify_common_features(results)
        
        # Detect outliers
        summary.outliers = self._detect_outliers(results, summary.complexity_metrics)
        
        # Generate collection-level recommendations
        summary.recommendations = self._generate_collection_recommendations(summary)
        
        return summary
    
    def _analyze_level_distribution(self, results: List[AnalysisResults]) -> Dict[str, int]:
        """Analyze CEFR level distribution across texts."""
        level_counts = Counter()
        
        for result in results:
            if result.overall_summary:
                level = result.overall_summary.text_level
                level_counts[level] += 1
        
        return dict(level_counts)
    
    def _calculate_complexity_metrics(self, results: List[AnalysisResults]) -> Dict[str, ComparisonMetrics]:
        """Calculate comparative complexity metrics."""
        metrics = {}
        
        # Collect complexity scores
        complexity_scores = []
        word_counts = []
        sentence_lengths = []
        readability_scores = []
        
        for result in results:
            if result.overall_summary:
                complexity_scores.append(result.overall_summary.complexity_score)
            
            word_counts.append(result.word_count)
            
            if result.complexity_analysis:
                sentence_len = result.complexity_analysis.sentence_metrics.get('avg_sentence_length', 0)
                sentence_lengths.append(sentence_len)
                
                fk_grade = result.complexity_analysis.readability_scores.get('flesch_kincaid_grade', 0)
                readability_scores.append(fk_grade)
        
        # Create comparison metrics
        if complexity_scores:
            metrics['complexity_score'] = ComparisonMetrics('Complexity Score', complexity_scores)
        
        if word_counts:
            metrics['word_count'] = ComparisonMetrics('Word Count', word_counts)
        
        if sentence_lengths:
            metrics['sentence_length'] = ComparisonMetrics('Average Sentence Length', sentence_lengths)
        
        if readability_scores:
            metrics['readability'] = ComparisonMetrics('Flesch-Kincaid Grade', readability_scores)
        
        return metrics
    
    def _analyze_vocabulary_patterns(self, results: List[AnalysisResults]) -> Dict[str, Any]:
        """Analyze vocabulary patterns across texts."""
        patterns = {
            'common_academic_words': [],
            'average_diversity': 0.0,
            'difficulty_trends': {},
            'domain_overlap': []
        }
        
        all_academic_words = []
        diversity_scores = []
        difficulty_distributions = defaultdict(list)
        
        for result in results:
            if result.vocabulary_analysis:
                vocab = result.vocabulary_analysis
                
                # Collect academic vocabulary
                all_academic_words.extend(vocab.academic_vocabulary)
                
                # Collect diversity scores
                diversity_scores.append(vocab.lexical_diversity_score)
                
                # Collect difficulty distributions
                for level, words in vocab.difficulty_distribution.items():
                    difficulty_distributions[level].append(len(words))
        
        # Find common academic words (appearing in multiple texts)
        word_counts = Counter(all_academic_words)
        common_words = [word for word, count in word_counts.most_common(20) if count > 1]
        patterns['common_academic_words'] = common_words
        
        # Calculate average diversity
        if diversity_scores:
            patterns['average_diversity'] = statistics.mean(diversity_scores)
        
        # Analyze difficulty trends
        for level, counts in difficulty_distributions.items():
            if counts:
                patterns['difficulty_trends'][level] = {
                    'average_count': statistics.mean(counts),
                    'range': (min(counts), max(counts))
                }
        
        return patterns
    
    def _analyze_grammar_patterns(self, results: List[AnalysisResults]) -> Dict[str, Any]:
        """Analyze grammar patterns across texts."""
        patterns = {
            'sentence_type_trends': {},
            'average_complexity': 0.0,
            'common_structures': [],
            'tense_patterns': {}
        }
        
        sentence_type_totals = defaultdict(list)
        complexity_scores = []
        all_structures = []
        tense_usage_totals = defaultdict(list)
        
        for result in results:
            if result.grammar_analysis:
                grammar = result.grammar_analysis
                
                # Collect sentence type distributions
                for sent_type, count in grammar.sentence_type_distribution.items():
                    sentence_type_totals[sent_type].append(count)
                
                # Collect complexity scores
                complexity_scores.append(grammar.syntactic_complexity_score)
                
                # Collect complex structures
                for structure in grammar.complex_structures:
                    structure_type = structure.get('type', 'unknown')
                    all_structures.append(structure_type)
                
                # Collect tense usage
                for tense, examples in grammar.tense_usage.items():
                    tense_usage_totals[tense].append(len(examples))
        
        # Analyze sentence type trends
        for sent_type, counts in sentence_type_totals.items():
            if counts:
                patterns['sentence_type_trends'][sent_type] = {
                    'average_count': statistics.mean(counts),
                    'total_usage': sum(counts)
                }
        
        # Calculate average complexity
        if complexity_scores:
            patterns['average_complexity'] = statistics.mean(complexity_scores)
        
        # Find common structures
        structure_counts = Counter(all_structures)
        patterns['common_structures'] = [
            struct for struct, count in structure_counts.most_common(10) if count > 1
        ]
        
        # Analyze tense patterns
        for tense, counts in tense_usage_totals.items():
            if counts:
                patterns['tense_patterns'][tense] = {
                    'average_usage': statistics.mean(counts),
                    'frequency_rank': sum(counts)
                }
        
        return patterns
    
    def _identify_common_features(self, results: List[AnalysisResults]) -> List[str]:
        """Identify features common across multiple texts."""
        feature_counts = Counter()
        
        for result in results:
            if result.overall_summary and result.overall_summary.key_linguistic_features:
                for feature in result.overall_summary.key_linguistic_features:
                    feature_counts[feature] += 1
        
        # Return features that appear in at least 25% of texts
        threshold = max(1, len(results) * 0.25)
        common_features = [
            feature for feature, count in feature_counts.items() 
            if count >= threshold
        ]
        
        return common_features
    
    def _detect_outliers(self, results: List[AnalysisResults], 
                        metrics: Dict[str, ComparisonMetrics]) -> List[Dict[str, Any]]:
        """Detect outlier texts based on complexity metrics."""
        outliers = []
        
        for i, result in enumerate(results):
            outlier_info = {
                'text_index': i,
                'title': result.title or f'Text {i+1}',
                'outlier_reasons': []
            }
            
            is_outlier = False
            
            # Check each metric for outliers
            for metric_name, metric in metrics.items():
                if len(metric.values) > 2 and metric.std_dev > 0:
                    z_score = abs((metric.values[i] - metric.mean) / metric.std_dev)
                    
                    if z_score > self.outlier_threshold:
                        is_outlier = True
                        outlier_info['outlier_reasons'].append({
                            'metric': metric_name,
                            'value': metric.values[i],
                            'z_score': z_score,
                            'deviation': 'high' if metric.values[i] > metric.mean else 'low'
                        })
            
            if is_outlier:
                outliers.append(outlier_info)
        
        return outliers
    
    def _generate_collection_recommendations(self, summary: CollectionSummary) -> List[str]:
        """Generate recommendations for the entire collection."""
        recommendations = []
        
        # Level distribution recommendations
        if summary.level_distribution:
            dominant_level = max(summary.level_distribution.items(), key=lambda x: x[1])[0]
            recommendations.append(f"컬렉션의 주요 수준은 {dominant_level}입니다.")
            
            level_variety = len(summary.level_distribution)
            if level_variety >= 4:
                recommendations.append("다양한 수준의 텍스트가 포함되어 있어 단계적 학습에 적합합니다.")
            elif level_variety <= 2:
                recommendations.append("비슷한 수준의 텍스트들로 구성되어 있어 특정 레벨 집중 학습에 적합합니다.")
        
        # Complexity recommendations
        if 'complexity_score' in summary.complexity_metrics:
            complexity_metric = summary.complexity_metrics['complexity_score']
            if complexity_metric.std_dev > 2.0:
                recommendations.append("텍스트 간 복잡도 차이가 크므로 학습자 수준에 맞는 선별적 사용을 권장합니다.")
            else:
                recommendations.append("텍스트들의 복잡도가 일관되어 체계적인 학습 진행에 적합합니다.")
        
        # Vocabulary recommendations
        if summary.vocabulary_patterns.get('common_academic_words'):
            common_count = len(summary.vocabulary_patterns['common_academic_words'])
            recommendations.append(f"{common_count}개의 공통 학술 어휘가 발견되어 어휘 학습 효과가 높을 것으로 예상됩니다.")
        
        # Grammar recommendations
        if summary.grammar_patterns.get('common_structures'):
            structure_count = len(summary.grammar_patterns['common_structures'])
            recommendations.append(f"{structure_count}개의 공통 문법 구조가 반복되어 문법 학습 강화에 도움이 됩니다.")
        
        # Outlier recommendations
        if summary.outliers:
            outlier_count = len(summary.outliers)
            recommendations.append(f"{outlier_count}개의 특이한 텍스트가 발견되었습니다. 이들은 고급 학습자나 특별 학습 목적으로 활용하세요.")
        
        return recommendations
    
    def generate_comparison_report(self, summary: CollectionSummary) -> str:
        """Generate a text report of the comparative analysis.
        
        Args:
            summary: CollectionSummary to report on
            
        Returns:
            Formatted text report
        """
        report_lines = []
        
        report_lines.append("=" * 60)
        report_lines.append("텍스트 컬렉션 비교 분석 보고서")
        report_lines.append("=" * 60)
        report_lines.append(f"총 텍스트 수: {summary.total_texts}")
        report_lines.append("")
        
        # Level distribution
        if summary.level_distribution:
            report_lines.append("CEFR 레벨 분포:")
            for level, count in sorted(summary.level_distribution.items()):
                percentage = (count / summary.total_texts) * 100
                report_lines.append(f"  {level}: {count}개 ({percentage:.1f}%)")
            report_lines.append("")
        
        # Complexity metrics
        if summary.complexity_metrics:
            report_lines.append("복잡도 지표:")
            for metric_name, metric in summary.complexity_metrics.items():
                report_lines.append(f"  {metric.metric_name}:")
                report_lines.append(f"    평균: {metric.mean:.2f}")
                report_lines.append(f"    범위: {metric.min_value:.2f} - {metric.max_value:.2f}")
                report_lines.append(f"    표준편차: {metric.std_dev:.2f}")
            report_lines.append("")
        
        # Common features
        if summary.common_features:
            report_lines.append("공통 언어적 특징:")
            for feature in summary.common_features:
                report_lines.append(f"  • {feature}")
            report_lines.append("")
        
        # Outliers
        if summary.outliers:
            report_lines.append("특이 텍스트:")
            for outlier in summary.outliers[:5]:  # Show top 5
                report_lines.append(f"  • {outlier['title']}")
                for reason in outlier['outlier_reasons'][:2]:  # Show top 2 reasons
                    report_lines.append(f"    - {reason['metric']}: {reason['deviation']} deviation")
            report_lines.append("")
        
        # Recommendations
        if summary.recommendations:
            report_lines.append("권장사항:")
            for i, rec in enumerate(summary.recommendations, 1):
                report_lines.append(f"  {i}. {rec}")
        
        return "\n".join(report_lines)
    
    def export_comparison_data(self, summary: CollectionSummary) -> Dict[str, Any]:
        """Export comparison data in structured format.
        
        Args:
            summary: CollectionSummary to export
            
        Returns:
            Dictionary with structured comparison data
        """
        export_data = {
            "collection_info": {
                "total_texts": summary.total_texts,
                "level_distribution": summary.level_distribution
            },
            "complexity_analysis": {},
            "patterns": {
                "vocabulary": summary.vocabulary_patterns,
                "grammar": summary.grammar_patterns,
                "common_features": summary.common_features
            },
            "outliers": summary.outliers,
            "recommendations": summary.recommendations
        }
        
        # Convert metrics to exportable format
        for metric_name, metric in summary.complexity_metrics.items():
            export_data["complexity_analysis"][metric_name] = {
                "mean": metric.mean,
                "median": metric.median,
                "std_dev": metric.std_dev,
                "min": metric.min_value,
                "max": metric.max_value,
                "range": metric.range_value
            }
        
        return export_data