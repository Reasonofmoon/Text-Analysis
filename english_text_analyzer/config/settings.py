"""Configuration classes for the English text analyzer."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
import yaml
from pathlib import Path


@dataclass
class VocabularyConfig:
    """Configuration for vocabulary analysis."""
    
    # CEFR level analysis
    enable_cefr_analysis: bool = True
    cefr_levels: List[str] = field(default_factory=lambda: ["A1", "A2", "B1", "B2", "C1", "C2"])
    
    # Academic vocabulary
    enable_academic_vocabulary: bool = True
    awl_sublists: List[int] = field(default_factory=lambda: list(range(1, 11)))
    
    # Collocations and idioms
    enable_collocation_detection: bool = True
    min_collocation_frequency: int = 2
    enable_idiom_detection: bool = True
    
    # Word frequency analysis
    frequency_bands: List[str] = field(default_factory=lambda: [
        "1-1000", "1000-2000", "2000-3000", "3000-5000", "5000+"
    ])
    
    # Lexical diversity
    calculate_lexical_diversity: bool = True
    diversity_metrics: List[str] = field(default_factory=lambda: [
        "ttr", "msttr", "mtld", "hdd"
    ])


@dataclass
class GrammarConfig:
    """Configuration for grammar analysis."""
    
    # Sentence type analysis
    enable_sentence_type_analysis: bool = True
    sentence_types: List[str] = field(default_factory=lambda: [
        "simple", "compound", "complex", "compound_complex"
    ])
    
    # Tense and voice analysis
    enable_tense_analysis: bool = True
    enable_voice_analysis: bool = True
    
    # Clause structure analysis
    enable_clause_analysis: bool = True
    max_clause_depth: int = 5
    
    # Complex structure detection
    enable_complex_structure_detection: bool = True
    complexity_threshold: float = 0.7


@dataclass
class StructureConfig:
    """Configuration for structure analysis."""
    
    # Topic sentence identification
    enable_topic_sentence_detection: bool = True
    topic_sentence_confidence_threshold: float = 0.6
    
    # Transition analysis
    enable_transition_analysis: bool = True
    transition_categories: List[str] = field(default_factory=lambda: [
        "addition", "contrast", "cause_effect", "sequence", "emphasis"
    ])
    
    # Coherence analysis
    enable_coherence_analysis: bool = True
    coherence_window_size: int = 3
    
    # Paragraph structure
    enable_paragraph_analysis: bool = True
    min_paragraph_sentences: int = 2


@dataclass
class ContentConfig:
    """Configuration for content analysis."""
    
    # Main idea identification
    enable_main_idea_detection: bool = True
    main_idea_confidence_threshold: float = 0.7
    
    # Supporting details
    enable_supporting_details: bool = True
    evidence_types: List[str] = field(default_factory=lambda: [
        "example", "statistic", "expert_opinion", "analogy", "definition"
    ])
    
    # Argumentation analysis
    enable_argumentation_analysis: bool = True
    argument_components: List[str] = field(default_factory=lambda: [
        "claim", "warrant", "backing", "qualifier", "rebuttal"
    ])
    
    # Hierarchical outline
    enable_outline_generation: bool = True
    max_outline_levels: int = 4


@dataclass
class ComplexityConfig:
    """Configuration for complexity analysis."""
    
    # Readability metrics
    enable_readability_scores: bool = True
    readability_metrics: List[str] = field(default_factory=lambda: [
        "flesch_kincaid", "flesch_reading_ease", "gunning_fog", 
        "coleman_liau", "automated_readability"
    ])
    
    # CEFR level estimation
    enable_cefr_estimation: bool = True
    cefr_estimation_method: str = "combined"  # "lexical", "syntactic", "combined"
    
    # Syntactic complexity
    enable_syntactic_complexity: bool = True
    syntactic_metrics: List[str] = field(default_factory=lambda: [
        "mean_length_utterance", "clause_density", "dependent_clause_ratio"
    ])
    
    # Information density
    enable_information_density: bool = True
    density_calculation_method: str = "content_words"  # "content_words", "semantic_density"


@dataclass
class OutputConfig:
    """Configuration for output formatting and reporting."""
    
    # Report formats
    enable_html_reports: bool = True
    enable_json_export: bool = True
    enable_pdf_reports: bool = False
    
    # HTML report settings
    html_template: str = "default"
    include_visualizations: bool = True
    interactive_elements: bool = True
    
    # JSON export settings
    json_pretty_print: bool = True
    include_raw_data: bool = False
    
    # Educational annotations
    include_educational_notes: bool = True
    difficulty_level: str = "intermediate"  # "beginner", "intermediate", "advanced"
    language: str = "en"  # "en", "ko", etc.


@dataclass
class AnalysisConfig:
    """Main configuration class for English text analysis."""
    
    # Enabled analyzers
    enabled_analyzers: List[str] = field(default_factory=lambda: [
        "vocabulary", "grammar", "structure", "content", "complexity"
    ])
    
    # Processing settings
    parallel_processing: bool = True
    max_workers: int = 4
    timeout_seconds: int = 300
    
    # API settings
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    max_retries: int = 3
    retry_delay: float = 1.0
    
    # Text preprocessing
    enable_preprocessing: bool = True
    min_text_length: int = 10
    max_text_length: int = 50000
    
    # Analyzer-specific configurations
    vocabulary_config: VocabularyConfig = field(default_factory=VocabularyConfig)
    grammar_config: GrammarConfig = field(default_factory=GrammarConfig)
    structure_config: StructureConfig = field(default_factory=StructureConfig)
    content_config: ContentConfig = field(default_factory=ContentConfig)
    complexity_config: ComplexityConfig = field(default_factory=ComplexityConfig)
    output_config: OutputConfig = field(default_factory=OutputConfig)
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        def _convert_dataclass(obj):
            if hasattr(obj, '__dataclass_fields__'):
                return {k: _convert_dataclass(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [_convert_dataclass(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: _convert_dataclass(v) for k, v in obj.items()}
            else:
                return obj
        
        return _convert_dataclass(self)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AnalysisConfig':
        """Create configuration from dictionary."""
        # Extract nested configurations
        vocab_config = VocabularyConfig(**config_dict.get('vocabulary_config', {}))
        grammar_config = GrammarConfig(**config_dict.get('grammar_config', {}))
        structure_config = StructureConfig(**config_dict.get('structure_config', {}))
        content_config = ContentConfig(**config_dict.get('content_config', {}))
        complexity_config = ComplexityConfig(**config_dict.get('complexity_config', {}))
        output_config = OutputConfig(**config_dict.get('output_config', {}))
        
        # Remove nested configs from main dict
        main_config = {k: v for k, v in config_dict.items() 
                      if not k.endswith('_config')}
        
        return cls(
            vocabulary_config=vocab_config,
            grammar_config=grammar_config,
            structure_config=structure_config,
            content_config=content_config,
            complexity_config=complexity_config,
            output_config=output_config,
            **main_config
        )
    
    def save_to_file(self, file_path: str) -> None:
        """Save configuration to file (JSON or YAML)."""
        path = Path(file_path)
        config_dict = self.to_dict()
        
        if path.suffix.lower() == '.yaml' or path.suffix.lower() == '.yml':
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'AnalysisConfig':
        """Load configuration from file (JSON or YAML)."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        if path.suffix.lower() == '.yaml' or path.suffix.lower() == '.yml':
            with open(path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f)
        else:
            with open(path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
        
        return cls.from_dict(config_dict)
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Check enabled analyzers
        valid_analyzers = {"vocabulary", "grammar", "structure", "content", "complexity"}
        for analyzer in self.enabled_analyzers:
            if analyzer not in valid_analyzers:
                errors.append(f"Invalid analyzer: {analyzer}")
        
        # Check processing settings
        if self.max_workers < 1:
            errors.append("max_workers must be at least 1")
        
        if self.timeout_seconds < 1:
            errors.append("timeout_seconds must be at least 1")
        
        # Check text length limits
        if self.min_text_length < 1:
            errors.append("min_text_length must be at least 1")
        
        if self.max_text_length < self.min_text_length:
            errors.append("max_text_length must be greater than min_text_length")
        
        # Check log level
        valid_log_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if self.log_level not in valid_log_levels:
            errors.append(f"Invalid log_level: {self.log_level}")
        
        return errors