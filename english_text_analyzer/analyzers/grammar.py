"""Grammar analyzer for English text analysis."""

from typing import List, Dict, Any
import langextract as lx

from ..core.base_analyzer import BaseAnalyzer, AnalysisResult


class GrammarAnalyzer(BaseAnalyzer):
    """Analyzer for grammatical structures, tenses, and syntactic patterns.
    
    This analyzer identifies sentence types, verb tenses, voice usage,
    clause structures, and complex grammatical patterns.
    """
    
    def __init__(self):
        super().__init__("grammar")
    
    def get_examples(self) -> List[lx.data.ExampleData]:
        """Return example data for grammar analysis."""
        return [
            lx.data.ExampleData(
                text="Having completed the research, the team published their findings.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="complex_structure",
                        extraction_text="Having completed the research",
                        attributes={
                            "structure_type": "perfect_participle_clause",
                            "function": "temporal_relationship",
                            "complexity_level": "advanced",
                            "educational_note": "완료된 행동을 나타내는 분사구문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="sentence_type",
                        extraction_text="Having completed the research, the team published their findings.",
                        attributes={
                            "type": "complex",
                            "main_clause": "the team published their findings",
                            "subordinate_clause": "Having completed the research",
                            "educational_note": "주절과 종속절로 구성된 복문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="verb_tense",
                        extraction_text="published",
                        attributes={
                            "tense": "past_simple",
                            "voice": "active",
                            "aspect": "simple",
                            "educational_note": "과거의 완료된 행동을 나타내는 단순과거"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The report will be submitted by the committee before the deadline.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="verb_tense",
                        extraction_text="will be submitted",
                        attributes={
                            "tense": "future_simple",
                            "voice": "passive",
                            "aspect": "simple",
                            "educational_note": "미래에 일어날 수동적 행동"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="sentence_type",
                        extraction_text="The report will be submitted by the committee before the deadline.",
                        attributes={
                            "type": "simple",
                            "voice": "passive",
                            "subject": "The report",
                            "educational_note": "수동태로 표현된 단문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="clause_structure",
                        extraction_text="before the deadline",
                        attributes={
                            "clause_type": "adverbial_clause",
                            "function": "time",
                            "educational_note": "시간을 나타내는 부사절"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="If I had studied harder, I would have passed the exam, but I didn't.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="sentence_type",
                        extraction_text="If I had studied harder, I would have passed the exam, but I didn't.",
                        attributes={
                            "type": "compound_complex",
                            "conditional_type": "third_conditional",
                            "educational_note": "조건절과 대조절이 결합된 복합복문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="complex_structure",
                        extraction_text="If I had studied harder, I would have passed the exam",
                        attributes={
                            "structure_type": "third_conditional",
                            "condition": "If I had studied harder",
                            "result": "I would have passed the exam",
                            "reality": "unreal_past",
                            "educational_note": "과거 사실과 반대되는 가정을 나타내는 3형식 조건문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="verb_tense",
                        extraction_text="had studied",
                        attributes={
                            "tense": "past_perfect",
                            "voice": "active",
                            "aspect": "perfect",
                            "educational_note": "과거완료 - 과거의 어떤 시점보다 더 이전의 행동"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="verb_tense",
                        extraction_text="would have passed",
                        attributes={
                            "tense": "conditional_perfect",
                            "voice": "active",
                            "aspect": "perfect",
                            "educational_note": "조건법 완료 - 실현되지 않은 과거의 가능성"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The students who are studying abroad have been learning new languages.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="sentence_type",
                        extraction_text="The students who are studying abroad have been learning new languages.",
                        attributes={
                            "type": "complex",
                            "main_clause": "The students have been learning new languages",
                            "relative_clause": "who are studying abroad",
                            "educational_note": "관계절이 포함된 복문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="clause_structure",
                        extraction_text="who are studying abroad",
                        attributes={
                            "clause_type": "relative_clause",
                            "relative_pronoun": "who",
                            "function": "defining",
                            "educational_note": "주어를 한정하는 관계절"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="verb_tense",
                        extraction_text="are studying",
                        attributes={
                            "tense": "present_continuous",
                            "voice": "active",
                            "aspect": "continuous",
                            "educational_note": "현재 진행 중인 행동"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="verb_tense",
                        extraction_text="have been learning",
                        attributes={
                            "tense": "present_perfect_continuous",
                            "voice": "active",
                            "aspect": "perfect_continuous",
                            "educational_note": "과거에 시작되어 현재까지 계속되는 행동"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="Being tired from the long journey, she decided to rest before continuing.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="complex_structure",
                        extraction_text="Being tired from the long journey",
                        attributes={
                            "structure_type": "present_participle_clause",
                            "function": "reason",
                            "complexity_level": "intermediate",
                            "educational_note": "이유를 나타내는 현재분사 구문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="sentence_type",
                        extraction_text="Being tired from the long journey, she decided to rest before continuing.",
                        attributes={
                            "type": "complex",
                            "main_clause": "she decided to rest before continuing",
                            "participial_clause": "Being tired from the long journey",
                            "educational_note": "분사구문이 포함된 복문"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The teacher asked what the students had learned and whether they understood the concept.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="complex_structure",
                        extraction_text="what the students had learned and whether they understood the concept",
                        attributes={
                            "structure_type": "reported_speech",
                            "question_type": "indirect_question",
                            "complexity_level": "advanced",
                            "educational_note": "간접의문문이 포함된 보고문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="clause_structure",
                        extraction_text="what the students had learned",
                        attributes={
                            "clause_type": "nominal_clause",
                            "function": "object",
                            "educational_note": "목적어 역할을 하는 명사절"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="clause_structure",
                        extraction_text="whether they understood the concept",
                        attributes={
                            "clause_type": "nominal_clause",
                            "function": "object",
                            "educational_note": "whether로 시작하는 명사절"
                        }
                    )
                ]
            )
        ]
    
    def get_prompt_description(self) -> str:
        """Return the prompt description for grammar analysis."""
        return """
        Analyze the grammatical structures in the given English text and extract the following information:

        1. **Sentence Types**: Classify sentences by structure
           - Simple: one independent clause
           - Compound: two or more independent clauses
           - Complex: one independent clause + one or more dependent clauses
           - Compound-Complex: multiple independent clauses + dependent clauses
           - Include main clause and subordinate clause identification
           - Provide Korean educational notes

        2. **Verb Tenses and Aspects**: Identify all verb forms
           - Tense: present, past, future, conditional
           - Aspect: simple, continuous, perfect, perfect_continuous
           - Voice: active, passive
           - Mood: indicative, subjunctive, imperative
           - Provide Korean explanations of usage

        3. **Clause Structures**: Identify different types of clauses
           - Independent clauses
           - Dependent clauses (adverbial, adjectival, nominal)
           - Relative clauses
           - Conditional clauses
           - Include function and relationship information

        4. **Complex Grammatical Structures**: Identify advanced patterns
           - Participle constructions
           - Infinitive constructions
           - Gerund constructions
           - Conditional sentences (0, 1st, 2nd, 3rd type)
           - Reported speech patterns
           - Include complexity level and educational explanations

        5. **Syntactic Patterns**: Identify sentence patterns and word order
           - Subject-Verb-Object patterns
           - Inversion patterns
           - Ellipsis and substitution
           - Coordination and subordination

        Focus on grammatical structures that are challenging for Korean learners of English.
        Provide detailed Korean explanations to help understand usage and formation rules.
        """
    
    def analyze(self, text: str) -> AnalysisResult:
        """Perform grammar analysis on the given text."""
        if not self.validate_text(text):
            raise ValueError("Text is not suitable for grammar analysis")
        
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
        
        # Add grammar-specific metadata
        result.add_metadata("analysis_type", "grammar")
        
        # Calculate sentence statistics
        sentences = self._split_sentences(text)
        result.add_metadata("total_sentences", len(sentences))
        result.add_metadata("average_sentence_length", 
                          sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0)
        
        # Enhance grammar analysis with additional processing
        self._enhance_tense_analysis(result)
        self._enhance_sentence_complexity_analysis(result)
        self._enhance_complex_structure_detection(result)
        self._analyze_dependency_relationships(result)
        
        return result
    
    def _split_sentences(self, text: str) -> List[str]:
        """Simple sentence splitting (can be enhanced with proper NLP tools)."""
        import re
        # Simple sentence splitting - in real implementation, use proper sentence tokenizer
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _enhance_tense_analysis(self, result: AnalysisResult) -> None:
        """Enhance tense analysis with additional patterns."""
        if "verb_tense" in result.analysis_data:
            tenses = result.analysis_data["verb_tense"]
            
            # Count tense distribution
            tense_counts = {}
            for tense_info in tenses:
                tense = tense_info["attributes"].get("tense", "unknown")
                tense_counts[tense] = tense_counts.get(tense, 0) + 1
            
            result.add_metadata("tense_distribution", tense_counts)
            
            # Add complexity scoring for tenses
            complexity_scores = {
                "present_simple": 1,
                "past_simple": 1,
                "future_simple": 2,
                "present_continuous": 2,
                "past_continuous": 3,
                "present_perfect": 3,
                "past_perfect": 4,
                "present_perfect_continuous": 4,
                "conditional_perfect": 5
            }
            
            total_complexity = sum(complexity_scores.get(tense_info["attributes"].get("tense", ""), 1) 
                                 for tense_info in tenses)
            avg_complexity = total_complexity / len(tenses) if tenses else 0
            result.add_metadata("tense_complexity_score", round(avg_complexity, 2))
    
    def _enhance_sentence_complexity_analysis(self, result: AnalysisResult) -> None:
        """Enhance sentence complexity analysis."""
        if "sentence_type" in result.analysis_data:
            sentence_types = result.analysis_data["sentence_type"]
            
            # Count sentence type distribution
            type_counts = {}
            for sentence_info in sentence_types:
                sentence_type = sentence_info["attributes"].get("type", "unknown")
                type_counts[sentence_type] = type_counts.get(sentence_type, 0) + 1
            
            result.add_metadata("sentence_type_distribution", type_counts)
            
            # Calculate complexity score
            complexity_scores = {
                "simple": 1,
                "compound": 2,
                "complex": 3,
                "compound_complex": 4
            }
            
            total_complexity = sum(complexity_scores.get(sentence_info["attributes"].get("type", ""), 1) 
                                 for sentence_info in sentence_types)
            avg_complexity = total_complexity / len(sentence_types) if sentence_types else 0
            result.add_metadata("sentence_complexity_score", round(avg_complexity, 2))
    
    def _enhance_complex_structure_detection(self, result: AnalysisResult) -> None:
        """Enhance detection of complex grammatical structures."""
        if "complex_structure" not in result.analysis_data:
            result.analysis_data["complex_structure"] = []
        
        complex_structures = result.analysis_data["complex_structure"]
        
        # Add complexity scoring and educational insights
        for structure in complex_structures:
            structure_type = structure["attributes"].get("structure_type", "")
            
            # Add difficulty level for Korean learners
            difficulty_levels = {
                "perfect_participle_clause": "고급",
                "third_conditional": "고급",
                "gerund_construction": "중급",
                "infinitive_construction": "중급",
                "passive_construction": "중급",
                "reported_speech": "고급"
            }
            
            structure["attributes"]["difficulty_for_korean_learners"] = difficulty_levels.get(structure_type, "중급")
            
            # Add common errors for Korean learners
            common_errors = {
                "third_conditional": "시제 일치 오류, would of 대신 would have 사용",
                "perfect_participle_clause": "분사구문의 주어 일치 문제",
                "passive_construction": "by 전치사 생략 오류"
            }
            
            if structure_type in common_errors:
                structure["attributes"]["common_korean_errors"] = common_errors[structure_type]
    
    def _analyze_dependency_relationships(self, result: AnalysisResult) -> None:
        """Analyze dependency relationships between clauses and phrases."""
        # Add dependency analysis metadata
        if "clause_structure" in result.analysis_data:
            clauses = result.analysis_data["clause_structure"]
            
            # Count different types of dependencies
            dependency_counts = {}
            for clause in clauses:
                clause_type = clause["attributes"].get("clause_type", "unknown")
                dependency_counts[clause_type] = dependency_counts.get(clause_type, 0) + 1
            
            result.add_metadata("dependency_distribution", dependency_counts)
            
            # Calculate syntactic complexity based on dependencies
            complexity_weights = {
                "relative_clause": 3,
                "adverbial_clause": 2,
                "nominal_clause": 2,
                "conditional_clause": 4,
                "participial_clause": 3
            }
            
            total_complexity = sum(complexity_weights.get(clause["attributes"].get("clause_type", ""), 1) 
                                 for clause in clauses)
            result.add_metadata("syntactic_complexity_score", total_complexity)
    
    def validate_text(self, text: str) -> bool:
        """Validate if text is suitable for grammar analysis."""
        if not super().validate_text(text):
            return False
        
        # Grammar analysis needs at least one complete sentence
        sentences = self._split_sentences(text)
        return len(sentences) >= 1 and any(len(s.split()) >= 3 for s in sentences)
    
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Return configuration schema for grammar analyzer."""
        base_schema = super().get_configuration_schema()
        
        grammar_schema = {
            "analyze_sentence_types": {
                "type": "boolean",
                "default": True,
                "description": "Analyze sentence structure types"
            },
            "analyze_verb_tenses": {
                "type": "boolean",
                "default": True,
                "description": "Analyze verb tenses and aspects"
            },
            "analyze_clause_structures": {
                "type": "boolean",
                "default": True,
                "description": "Analyze clause structures and relationships"
            },
            "analyze_complex_structures": {
                "type": "boolean",
                "default": True,
                "description": "Analyze complex grammatical patterns"
            },
            "complexity_threshold": {
                "type": "number",
                "default": 2.0,
                "description": "Minimum complexity score to flag structures"
            },
            "include_korean_explanations": {
                "type": "boolean",
                "default": True,
                "description": "Include Korean educational explanations"
            }
        }
        
        base_schema.update(grammar_schema)
        return base_schema