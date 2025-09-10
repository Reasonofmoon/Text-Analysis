"""Data models for analysis results."""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from ..core.base_analyzer import AnalysisResult


@dataclass
class VocabularyResult:
    """Results from vocabulary analysis."""
    difficulty_distribution: Dict[str, List[str]] = field(default_factory=dict)  # CEFR levels
    academic_vocabulary: List[str] = field(default_factory=list)
    collocations: List[Dict[str, Any]] = field(default_factory=list)
    idiomatic_expressions: List[str] = field(default_factory=list)
    word_frequency: Dict[str, int] = field(default_factory=dict)
    lexical_diversity_score: float = 0.0
    domain_specific_terms: List[str] = field(default_factory=list)


@dataclass
class GrammarResult:
    """Results from grammar analysis."""
    sentence_type_distribution: Dict[str, int] = field(default_factory=dict)
    tense_usage: Dict[str, List[str]] = field(default_factory=dict)
    voice_distribution: Dict[str, float] = field(default_factory=dict)
    clause_analysis: Dict[str, Any] = field(default_factory=dict)
    complex_structures: List[Dict[str, Any]] = field(default_factory=list)
    syntactic_complexity_score: float = 0.0


@dataclass
class StructureResult:
    """Results from structure analysis."""
    topic_sentences: List[Dict[str, Any]] = field(default_factory=list)
    paragraph_organization: Dict[str, Any] = field(default_factory=dict)
    transition_markers: List[Dict[str, Any]] = field(default_factory=list)
    discourse_markers: List[Dict[str, Any]] = field(default_factory=list)
    coherence_patterns: Dict[str, Any] = field(default_factory=dict)
    cohesion_score: float = 0.0


@dataclass
class ContentResult:
    """Results from content analysis."""
    main_ideas: List[Dict[str, Any]] = field(default_factory=list)
    thesis_statements: List[Dict[str, Any]] = field(default_factory=list)
    supporting_details: List[Dict[str, Any]] = field(default_factory=list)
    evidence_types: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    argument_structure: Dict[str, Any] = field(default_factory=dict)
    hierarchical_outline: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplexityResult:
    """Results from complexity analysis."""
    readability_scores: Dict[str, float] = field(default_factory=dict)
    cefr_level: str = "Unknown"
    lexical_diversity: Dict[str, float] = field(default_factory=dict)
    sentence_metrics: Dict[str, float] = field(default_factory=dict)
    syntactic_complexity: Dict[str, float] = field(default_factory=dict)
    information_density: Dict[str, float] = field(default_factory=dict)
    adaptation_recommendations: List[str] = field(default_factory=list)


@dataclass
class OverallSummary:
    """Overall summary of all analysis results."""
    text_level: str = "Unknown"  # A1, A2, B1, B2, C1, C2
    dominant_themes: List[str] = field(default_factory=list)
    key_linguistic_features: List[str] = field(default_factory=list)
    educational_recommendations: List[str] = field(default_factory=list)
    complexity_score: float = 0.0
    confidence_score: float = 0.0


@dataclass
class AnalysisResults:
    """Container for aggregated analysis results from multiple analyzers."""
    
    # Input text information
    text: str
    title: Optional[str] = None
    analysis_date: datetime = field(default_factory=datetime.now)
    
    # Text statistics
    word_count: int = 0
    char_count: int = 0
    sentence_count: int = 0
    paragraph_count: int = 0
    
    # Structured analysis results
    vocabulary_analysis: Optional[VocabularyResult] = None
    grammar_analysis: Optional[GrammarResult] = None
    structure_analysis: Optional[StructureResult] = None
    content_analysis: Optional[ContentResult] = None
    complexity_analysis: Optional[ComplexityResult] = None
    overall_summary: Optional[OverallSummary] = None
    
    # Raw analyzer results for backward compatibility
    analyzer_results: Dict[str, AnalysisResult] = field(default_factory=dict)
    
    # Processing metadata
    analysis_time: float = 0.0
    analyzers_used: List[str] = field(default_factory=list)
    
    def add_analyzer_result(self, result: AnalysisResult) -> None:
        """Add result from an individual analyzer.
        
        Args:
            result: AnalysisResult from an analyzer
        """
        self.analyzer_results[result.analyzer_name] = result
        if result.analyzer_name not in self.analyzers_used:
            self.analyzers_used.append(result.analyzer_name)
        
        # Convert to structured result types
        self._convert_to_structured_results(result)
    
    def _convert_to_structured_results(self, result: AnalysisResult) -> None:
        """Convert raw analyzer result to structured result types."""
        if result.analyzer_name == "vocabulary":
            self.vocabulary_analysis = self._create_vocabulary_result(result)
        elif result.analyzer_name == "grammar":
            self.grammar_analysis = self._create_grammar_result(result)
        elif result.analyzer_name == "structure":
            self.structure_analysis = self._create_structure_result(result)
        elif result.analyzer_name == "content":
            self.content_analysis = self._create_content_result(result)
        elif result.analyzer_name == "complexity":
            self.complexity_analysis = self._create_complexity_result(result)
    
    def _create_vocabulary_result(self, result: AnalysisResult) -> VocabularyResult:
        """Create VocabularyResult from raw analyzer result."""
        data = result.results if hasattr(result, 'results') else result.analysis_data
        return VocabularyResult(
            difficulty_distribution=data.get("difficulty_distribution", {}),
            academic_vocabulary=data.get("academic_vocabulary", []),
            collocations=data.get("collocations", []),
            idiomatic_expressions=data.get("idiomatic_expressions", []),
            word_frequency=data.get("word_frequency", {}),
            lexical_diversity_score=data.get("lexical_diversity_score", 0.0),
            domain_specific_terms=data.get("domain_specific_terms", [])
        )
    
    def _create_grammar_result(self, result: AnalysisResult) -> GrammarResult:
        """Create GrammarResult from raw analyzer result."""
        data = result.results if hasattr(result, 'results') else result.analysis_data
        return GrammarResult(
            sentence_type_distribution=data.get("sentence_type_distribution", {}),
            tense_usage=data.get("tense_usage", {}),
            voice_distribution=data.get("voice_distribution", {}),
            clause_analysis=data.get("clause_analysis", {}),
            complex_structures=data.get("complex_structures", []),
            syntactic_complexity_score=data.get("syntactic_complexity_score", 0.0)
        )
    
    def _create_structure_result(self, result: AnalysisResult) -> StructureResult:
        """Create StructureResult from raw analyzer result."""
        data = result.results if hasattr(result, 'results') else result.analysis_data
        return StructureResult(
            topic_sentences=data.get("topic_sentences", []),
            paragraph_organization=data.get("paragraph_organization", {}),
            transition_markers=data.get("transition_markers", []),
            discourse_markers=data.get("discourse_markers", []),
            coherence_patterns=data.get("coherence_patterns", {}),
            cohesion_score=data.get("cohesion_score", 0.0)
        )
    
    def _create_content_result(self, result: AnalysisResult) -> ContentResult:
        """Create ContentResult from raw analyzer result."""
        data = result.results if hasattr(result, 'results') else result.analysis_data
        return ContentResult(
            main_ideas=data.get("main_ideas", []),
            thesis_statements=data.get("thesis_statements", []),
            supporting_details=data.get("supporting_details", []),
            evidence_types=data.get("evidence_types", {}),
            argument_structure=data.get("argument_structure", {}),
            hierarchical_outline=data.get("hierarchical_outline", {})
        )
    
    def _create_complexity_result(self, result: AnalysisResult) -> ComplexityResult:
        """Create ComplexityResult from raw analyzer result."""
        data = result.results if hasattr(result, 'results') else result.analysis_data
        return ComplexityResult(
            readability_scores=data.get("readability_scores", {}),
            cefr_level=data.get("cefr_level", "Unknown"),
            lexical_diversity=data.get("lexical_diversity", {}),
            sentence_metrics=data.get("sentence_metrics", {}),
            syntactic_complexity=data.get("syntactic_complexity", {}),
            information_density=data.get("information_density", {}),
            adaptation_recommendations=data.get("recommendations", [])
        )
    
    def get_analyzer_result(self, analyzer_name: str) -> Optional[AnalysisResult]:
        """Get result from a specific analyzer.
        
        Args:
            analyzer_name: Name of the analyzer
            
        Returns:
            AnalysisResult if found, None otherwise
        """
        return self.analyzer_results.get(analyzer_name)
    
    def has_analyzer_result(self, analyzer_name: str) -> bool:
        """Check if results from a specific analyzer are available.
        
        Args:
            analyzer_name: Name of the analyzer
            
        Returns:
            True if results are available, False otherwise
        """
        return analyzer_name in self.analyzer_results
    
    def get_all_extractions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all extractions from all analyzers organized by extraction class.
        
        Returns:
            Dictionary mapping extraction classes to lists of extractions
        """
        all_extractions = {}
        
        for analyzer_name, result in self.analyzer_results.items():
            for extraction_class, extractions in result.analysis_data.items():
                if extraction_class not in all_extractions:
                    all_extractions[extraction_class] = []
                
                # Add analyzer name to each extraction for tracking
                for extraction in extractions:
                    extraction_with_source = extraction.copy()
                    extraction_with_source['source_analyzer'] = analyzer_name
                    all_extractions[extraction_class].append(extraction_with_source)
        
        return all_extractions
    
    def get_extractions_by_class(self, extraction_class: str) -> List[Dict[str, Any]]:
        """Get all extractions of a specific class from all analyzers.
        
        Args:
            extraction_class: The extraction class to retrieve
            
        Returns:
            List of extractions of the specified class
        """
        extractions = []
        
        for analyzer_name, result in self.analyzer_results.items():
            if extraction_class in result.analysis_data:
                for extraction in result.analysis_data[extraction_class]:
                    extraction_with_source = extraction.copy()
                    extraction_with_source['source_analyzer'] = analyzer_name
                    extractions.append(extraction_with_source)
        
        return extractions
    
    def calculate_text_statistics(self) -> None:
        """Calculate basic text statistics."""
        if not self.text:
            return
        
        self.char_count = len(self.text)
        self.word_count = len(self.text.split())
        
        # Count sentences (simple heuristic)
        sentence_endings = ['.', '!', '?']
        self.sentence_count = sum(1 for char in self.text if char in sentence_endings)
        
        # Count paragraphs
        self.paragraph_count = len([p for p in self.text.split('\n\n') if p.strip()])
        if self.paragraph_count == 0:
            self.paragraph_count = 1
    
    def generate_summary(self) -> OverallSummary:
        """Generate overall summary of analysis results.
        
        Returns:
            OverallSummary containing comprehensive analysis insights
        """
        # Determine overall text level from complexity analysis
        text_level = "Unknown"
        complexity_score = 0.0
        
        if self.complexity_analysis:
            text_level = self.complexity_analysis.cefr_level
            # Calculate overall complexity score (0-10 scale)
            fk_grade = self.complexity_analysis.readability_scores.get("flesch_kincaid_grade", 0)
            complexity_score = min(10, max(0, fk_grade / 2))
        
        # Extract dominant themes from content analysis
        dominant_themes = []
        if self.content_analysis and self.content_analysis.main_ideas:
            dominant_themes = [idea.get("theme", "Unknown") for idea in self.content_analysis.main_ideas[:3]]
        
        # Identify key linguistic features
        key_features = []
        if self.grammar_analysis:
            if self.grammar_analysis.complex_structures:
                key_features.append("복잡한 문법 구조")
            if self.grammar_analysis.syntactic_complexity_score > 5:
                key_features.append("높은 구문 복잡도")
        
        if self.vocabulary_analysis:
            if self.vocabulary_analysis.academic_vocabulary:
                key_features.append("학술 어휘 포함")
            if self.vocabulary_analysis.lexical_diversity_score > 0.7:
                key_features.append("높은 어휘 다양성")
        
        if self.structure_analysis:
            if self.structure_analysis.transition_markers:
                key_features.append("명확한 전환 표현")
            if self.structure_analysis.cohesion_score > 0.7:
                key_features.append("높은 응집성")
        
        # Generate educational recommendations
        educational_recommendations = []
        
        if text_level in ["A1", "A2"]:
            educational_recommendations.extend([
                "기초 어휘 학습에 적합",
                "기본 문법 구조 연습용",
                "읽기 유창성 향상에 도움"
            ])
        elif text_level in ["B1", "B2"]:
            educational_recommendations.extend([
                "중급 학습자에게 적절한 도전",
                "복잡한 문법 구조 학습",
                "학술적 읽기 준비"
            ])
        elif text_level in ["C1", "C2"]:
            educational_recommendations.extend([
                "고급 학습자 또는 원어민 수준",
                "비판적 사고 능력 개발",
                "전문 분야 학습에 활용"
            ])
        
        # Add specific recommendations from complexity analysis
        if self.complexity_analysis and self.complexity_analysis.adaptation_recommendations:
            educational_recommendations.extend(self.complexity_analysis.adaptation_recommendations[:3])
        
        # Calculate confidence score based on available analyses
        confidence_score = len(self.analyzers_used) / 5.0  # Assuming 5 total analyzers
        
        summary = OverallSummary(
            text_level=text_level,
            dominant_themes=dominant_themes,
            key_linguistic_features=key_features,
            educational_recommendations=educational_recommendations[:8],  # Limit to 8
            complexity_score=complexity_score,
            confidence_score=confidence_score
        )
        
        self.overall_summary = summary
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert results to dictionary format.
        
        Returns:
            Dictionary representation of the results
        """
        # Convert analyzer results to dictionaries
        analyzer_results_dict = {}
        for name, result in self.analyzer_results.items():
            analyzer_results_dict[name] = result.to_dict()
        
        # Convert structured results to dictionaries
        def dataclass_to_dict(obj):
            if obj is None:
                return None
            return {k: v for k, v in obj.__dict__.items()}
        
        return {
            "text": self.text,
            "title": self.title,
            "analysis_date": self.analysis_date.isoformat(),
            "word_count": self.word_count,
            "char_count": self.char_count,
            "sentence_count": self.sentence_count,
            "paragraph_count": self.paragraph_count,
            "vocabulary_analysis": dataclass_to_dict(self.vocabulary_analysis),
            "grammar_analysis": dataclass_to_dict(self.grammar_analysis),
            "structure_analysis": dataclass_to_dict(self.structure_analysis),
            "content_analysis": dataclass_to_dict(self.content_analysis),
            "complexity_analysis": dataclass_to_dict(self.complexity_analysis),
            "overall_summary": dataclass_to_dict(self.overall_summary),
            "analyzer_results": analyzer_results_dict,
            "analysis_time": self.analysis_time,
            "analyzers_used": self.analyzers_used
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Convert results to JSON string.
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalysisResults':
        """Create AnalysisResults from dictionary.
        
        Args:
            data: Dictionary containing results data
            
        Returns:
            AnalysisResults instance
        """
        # Convert analyzer results back to AnalysisResult objects
        analyzer_results = {}
        for name, result_dict in data.get("analyzer_results", {}).items():
            analyzer_results[name] = AnalysisResult(
                analyzer_name=result_dict["analyzer_name"],
                analysis_data=result_dict["analysis_data"]
            )
            analyzer_results[name].metadata = result_dict.get("metadata", {})
        
        return cls(
            text=data["text"],
            title=data.get("title"),
            analysis_date=datetime.fromisoformat(data["analysis_date"]),
            word_count=data.get("word_count", 0),
            char_count=data.get("char_count", 0),
            sentence_count=data.get("sentence_count", 0),
            paragraph_count=data.get("paragraph_count", 0),
            analyzer_results=analyzer_results,
            analysis_time=data.get("analysis_time", 0.0),
            analyzers_used=data.get("analyzers_used", []),
            overall_summary=data.get("overall_summary")
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AnalysisResults':
        """Create AnalysisResults from JSON string.
        
        Args:
            json_str: JSON string containing results data
            
        Returns:
            AnalysisResults instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)