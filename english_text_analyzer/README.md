# English Text Analyzer

A comprehensive tool for analyzing English texts using langextract. This package provides modular analysis capabilities for vocabulary, grammar, structure, content, and complexity analysis of English texts for educational purposes.

## Features

- **Vocabulary Analysis**: CEFR level classification, academic vocabulary identification, collocations, and lexical diversity
- **Grammar Analysis**: Sentence type classification, tense/voice analysis, and complex structure detection
- **Structure Analysis**: Topic sentence identification, transition analysis, and coherence assessment
- **Content Analysis**: Main idea extraction, supporting detail categorization, and argumentation structure
- **Complexity Analysis**: Readability scores, CEFR level estimation, and syntactic complexity metrics
- **Batch Processing**: Analyze multiple texts efficiently with parallel processing
- **Multiple Output Formats**: HTML reports, JSON export, and PDF generation
- **Extensible Architecture**: Plugin system for custom analyzers

## Installation

```bash
pip install english-text-analyzer
```

### Development Installation

```bash
git clone https://github.com/your-org/english-text-analyzer.git
cd english-text-analyzer
pip install -e .[dev]
```

## Quick Start

```python
from english_text_analyzer import EnglishTextAnalyzer

# Initialize analyzer
analyzer = EnglishTextAnalyzer(api_key="your-api-key")

# Analyze text
text = "The comprehensive analysis revealed significant discrepancies in the data."
results = analyzer.analyze_text(text, title="Sample Analysis")

# Generate report
html_report = analyzer.generate_report(results, format="html")
print(html_report)
```

## Configuration

The analyzer can be configured using YAML or JSON files:

```yaml
# english_text_analyzer_config.yaml
enabled_analyzers:
  - vocabulary
  - grammar
  - structure
  - content
  - complexity

parallel_processing: true
max_workers: 4

vocabulary_config:
  enable_cefr_analysis: true
  enable_academic_vocabulary: true
  enable_collocation_detection: true

grammar_config:
  enable_sentence_type_analysis: true
  enable_tense_analysis: true
  enable_clause_analysis: true
```

## API Reference

### EnglishTextAnalyzer

Main class for text analysis.

#### Methods

- `analyze_text(text, title=None, analysis_types=None)`: Analyze a single text
- `batch_analyze(texts, titles=None, analysis_types=None)`: Analyze multiple texts
- `generate_report(results, format="html", output_path=None)`: Generate analysis report

### AnalysisResults

Container for analysis results with methods for accessing and exporting data.

#### Methods

- `get_analyzer_result(analyzer_name)`: Get results from specific analyzer
- `get_all_extractions()`: Get all extractions organized by type
- `to_dict()`: Convert to dictionary format
- `to_json()`: Convert to JSON string

## Analyzers

### Vocabulary Analyzer
- CEFR level classification (A1-C2)
- Academic Word List (AWL) identification
- Collocation and idiom detection
- Lexical diversity metrics

### Grammar Analyzer
- Sentence type classification
- Tense and voice analysis
- Clause structure identification
- Complex grammatical patterns

### Structure Analyzer
- Topic sentence detection
- Transition marker extraction
- Coherence and cohesion analysis
- Paragraph organization

### Content Analyzer
- Main idea identification
- Supporting detail categorization
- Argumentation structure analysis
- Evidence type classification

### Complexity Analyzer
- Readability scores (Flesch-Kincaid, etc.)
- CEFR level estimation
- Syntactic complexity metrics
- Information density analysis

## Examples

### Basic Analysis

```python
from english_text_analyzer import EnglishTextAnalyzer

analyzer = EnglishTextAnalyzer()
text = "Your English text here..."
results = analyzer.analyze_text(text)

# Access vocabulary analysis
vocab_result = results.get_analyzer_result("vocabulary")
print(vocab_result.analysis_data)
```

### Batch Processing

```python
texts = ["Text 1...", "Text 2...", "Text 3..."]
results_list = analyzer.batch_analyze(texts)

for i, results in enumerate(results_list):
    print(f"Analysis {i+1}: {results.word_count} words")
```

### Custom Configuration

```python
from english_text_analyzer import AnalysisConfig, EnglishTextAnalyzer

config = AnalysisConfig(
    enabled_analyzers=["vocabulary", "grammar"],
    parallel_processing=False
)

analyzer = EnglishTextAnalyzer(config=config)
```

## Requirements

- Python 3.8+
- langextract
- pyyaml
- typing-extensions

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## Support

For questions and support, please open an issue on GitHub.