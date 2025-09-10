"""Vocabulary analyzer for English text analysis."""

from typing import List, Dict, Any
import langextract as lx

from ..core.base_analyzer import BaseAnalyzer, AnalysisResult


class VocabularyAnalyzer(BaseAnalyzer):
    """Analyzer for vocabulary complexity, frequency, and semantic categories.
    
    This analyzer identifies and categorizes vocabulary by difficulty levels,
    extracts word frequency patterns, identifies academic vocabulary,
    collocations, and idiomatic expressions.
    """
    
    def __init__(self):
        super().__init__("vocabulary")
    
    def get_examples(self) -> List[lx.data.ExampleData]:
        """Return example data for vocabulary analysis."""
        return [
            lx.data.ExampleData(
                text="The comprehensive analysis revealed significant discrepancies in the data.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="academic_vocabulary",
                        extraction_text="comprehensive",
                        attributes={
                            "cefr_level": "C1",
                            "awl_sublist": "7",
                            "frequency_band": "3000-5000",
                            "part_of_speech": "adjective",
                            "educational_note": "학술적 글쓰기에서 자주 사용되는 고급 어휘"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="academic_vocabulary", 
                        extraction_text="analysis",
                        attributes={
                            "cefr_level": "B2",
                            "awl_sublist": "1",
                            "frequency_band": "1000-2000",
                            "part_of_speech": "noun",
                            "educational_note": "학술 텍스트의 핵심 어휘"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="academic_vocabulary",
                        extraction_text="significant",
                        attributes={
                            "cefr_level": "B2",
                            "awl_sublist": "1",
                            "frequency_band": "2000-3000",
                            "part_of_speech": "adjective",
                            "educational_note": "중요성을 나타내는 학술 어휘"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="academic_vocabulary",
                        extraction_text="discrepancies",
                        attributes={
                            "cefr_level": "C2",
                            "awl_sublist": "8",
                            "frequency_band": "5000+",
                            "part_of_speech": "noun",
                            "educational_note": "불일치, 차이를 나타내는 고급 학술 어휘"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="Students should take advantage of this opportunity to enhance their learning experience.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="collocation",
                        extraction_text="take advantage of",
                        attributes={
                            "collocation_type": "verb_phrase",
                            "frequency": "high",
                            "cefr_level": "B1",
                            "educational_note": "기회를 활용한다는 의미의 연어 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="academic_vocabulary",
                        extraction_text="enhance",
                        attributes={
                            "cefr_level": "B2",
                            "awl_sublist": "6",
                            "frequency_band": "3000-4000",
                            "part_of_speech": "verb",
                            "educational_note": "향상시키다, 개선하다의 의미"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="basic_vocabulary",
                        extraction_text="students",
                        attributes={
                            "cefr_level": "A1",
                            "frequency_band": "0-1000",
                            "part_of_speech": "noun",
                            "educational_note": "기본 어휘"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="It's raining cats and dogs, so we should call it a day and hit the books tomorrow.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="idiomatic_expression",
                        extraction_text="raining cats and dogs",
                        attributes={
                            "meaning": "비가 매우 많이 오다",
                            "cefr_level": "B2",
                            "usage_context": "informal",
                            "educational_note": "직역하면 안 되는 관용 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="idiomatic_expression",
                        extraction_text="call it a day",
                        attributes={
                            "meaning": "하루 일을 마치다",
                            "cefr_level": "B1",
                            "usage_context": "informal",
                            "educational_note": "일을 끝내고 쉬자는 의미"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="idiomatic_expression",
                        extraction_text="hit the books",
                        attributes={
                            "meaning": "열심히 공부하다",
                            "cefr_level": "B1",
                            "usage_context": "informal",
                            "educational_note": "책을 치는 것이 아니라 공부한다는 의미"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The company made a breakthrough in artificial intelligence research.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="collocation",
                        extraction_text="made a breakthrough",
                        attributes={
                            "collocation_type": "verb_noun",
                            "frequency": "high",
                            "cefr_level": "B2",
                            "educational_note": "돌파구를 마련하다, 획기적 발견을 하다"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="domain_specific",
                        extraction_text="artificial intelligence",
                        attributes={
                            "domain": "technology",
                            "cefr_level": "B2",
                            "part_of_speech": "noun_phrase",
                            "educational_note": "인공지능을 의미하는 기술 용어"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The research methodology employed a mixed-methods approach to investigate the phenomenon.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="domain_specific",
                        extraction_text="methodology",
                        attributes={
                            "domain": "research",
                            "cefr_level": "C1",
                            "part_of_speech": "noun",
                            "educational_note": "연구 방법론을 의미하는 전문 용어"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="domain_specific",
                        extraction_text="mixed-methods approach",
                        attributes={
                            "domain": "research",
                            "cefr_level": "C2",
                            "part_of_speech": "noun_phrase",
                            "educational_note": "질적, 양적 연구를 결합한 연구 방법"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="academic_vocabulary",
                        extraction_text="investigate",
                        attributes={
                            "cefr_level": "B2",
                            "awl_sublist": "4",
                            "frequency_band": "2000-3000",
                            "part_of_speech": "verb",
                            "educational_note": "조사하다, 연구하다의 의미"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="academic_vocabulary",
                        extraction_text="phenomenon",
                        attributes={
                            "cefr_level": "C1",
                            "awl_sublist": "7",
                            "frequency_band": "4000-5000",
                            "part_of_speech": "noun",
                            "educational_note": "현상을 의미하는 학술 어휘"
                        }
                    )
                ]
            )
        ]
    
    def get_prompt_description(self) -> str:
        """Return the prompt description for vocabulary analysis."""
        return """
        Analyze the vocabulary in the given English text and extract the following information:

        1. **Academic Vocabulary**: Identify words from the Academic Word List (AWL) and other academic vocabulary
           - Include CEFR level (A1, A2, B1, B2, C1, C2)
           - Include AWL sublist number if applicable
           - Include frequency band (0-1000, 1000-2000, etc.)
           - Include part of speech
           - Provide educational notes in Korean

        2. **Collocations**: Identify common word combinations and phrases
           - Specify collocation type (verb_phrase, noun_phrase, adjective_noun, etc.)
           - Include frequency level (high, medium, low)
           - Include CEFR level
           - Provide educational notes explaining usage

        3. **Basic Vocabulary**: Identify high-frequency, basic vocabulary (CEFR A1-A2)
           - Include CEFR level
           - Include frequency band
           - Include part of speech

        4. **Domain-Specific Terms**: Identify specialized terminology
           - Specify the domain (research, science, business, etc.)
           - Include CEFR level if applicable
           - Include part of speech
           - Provide educational explanations

        5. **Idiomatic Expressions**: Identify idioms and fixed expressions
           - Include meaning explanation
           - Include usage context
           - Include CEFR level

        Focus on vocabulary that would be educationally valuable for English language learners.
        Provide Korean educational notes to help Korean learners understand usage and meaning.
        """
    
    def analyze(self, text: str) -> AnalysisResult:
        """Perform vocabulary analysis on the given text."""
        if not self.validate_text(text):
            raise ValueError("Text is not suitable for vocabulary analysis")
        
        # Use langextract to perform the analysis
        examples = self.get_examples()
        prompt_description = self.get_prompt_description()
        
        # Create langextract analyzer
        analyzer = lx.Analyzer(
            examples=examples,
            description=prompt_description
        )
        
        # Perform analysis
        raw_results = analyzer.analyze(text)
        
        # Post-process results
        result = self.post_process_results(raw_results)
        
        # Add vocabulary-specific metadata
        result.add_metadata("analysis_type", "vocabulary")
        result.add_metadata("total_words", len(text.split()))
        result.add_metadata("unique_words", len(set(text.lower().split())))
        
        # Calculate vocabulary diversity
        words = text.split()
        unique_words = set(word.lower() for word in words)
        if len(words) > 0:
            lexical_diversity = len(unique_words) / len(words)
            result.add_metadata("lexical_diversity", round(lexical_diversity, 3))
        
        # Add collocation and idiom-specific processing
        self._enhance_collocation_detection(result)
        self._enhance_idiom_detection(result)
        
        return result
    
    def _enhance_collocation_detection(self, result: AnalysisResult) -> None:
        """Enhance collocation detection with additional patterns."""
        if "collocation" in result.analysis_data:
            collocations = result.analysis_data["collocation"]
            
            # Add collocation strength and frequency metadata
            for collocation in collocations:
                # Add collocation strength (placeholder - would use corpus data in real implementation)
                collocation["attributes"]["strength"] = "medium"
                
                # Add usage examples
                if "take advantage of" in collocation["text"]:
                    collocation["attributes"]["usage_examples"] = [
                        "Take advantage of this opportunity",
                        "Students should take advantage of the resources"
                    ]
                elif "mixed-methods approach" in collocation["text"]:
                    collocation["attributes"]["usage_examples"] = [
                        "The study used a mixed-methods approach",
                        "A mixed-methods approach combines qualitative and quantitative data"
                    ]
    
    def _enhance_idiom_detection(self, result: AnalysisResult) -> None:
        """Enhance idiom detection with additional patterns."""
        # Add idiom detection if not already present
        if "idiomatic_expression" not in result.analysis_data:
            result.analysis_data["idiomatic_expression"] = []
        
        # Look for common idiomatic patterns in the text
        # This is a simplified implementation - real implementation would use comprehensive idiom database
        idioms = result.analysis_data["idiomatic_expression"]
        
        # Add metadata for existing idioms
        for idiom in idioms:
            idiom["attributes"]["figurative_meaning"] = True
            idiom["attributes"]["literal_translation_warning"] = "이 표현은 직역하면 안 됩니다"
    
    def validate_text(self, text: str) -> bool:
        """Validate if text is suitable for vocabulary analysis."""
        if not super().validate_text(text):
            return False
        
        # Vocabulary analysis needs at least 5 words
        words = text.split()
        return len(words) >= 5
    
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Return configuration schema for vocabulary analyzer."""
        base_schema = super().get_configuration_schema()
        
        vocabulary_schema = {
            "min_word_frequency": {
                "type": "integer",
                "default": 1,
                "description": "Minimum word frequency to include in analysis"
            },
            "include_basic_vocabulary": {
                "type": "boolean", 
                "default": True,
                "description": "Include basic vocabulary (A1-A2) in analysis"
            },
            "include_academic_vocabulary": {
                "type": "boolean",
                "default": True,
                "description": "Include academic vocabulary in analysis"
            },
            "include_collocations": {
                "type": "boolean",
                "default": True,
                "description": "Include collocation analysis"
            },
            "include_domain_specific": {
                "type": "boolean",
                "default": True,
                "description": "Include domain-specific terminology"
            },
            "cefr_levels": {
                "type": "array",
                "default": ["A1", "A2", "B1", "B2", "C1", "C2"],
                "description": "CEFR levels to include in analysis"
            }
        }
        
        base_schema.update(vocabulary_schema)
        return base_schema