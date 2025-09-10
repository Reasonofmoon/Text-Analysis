"""Structure analyzer for English text analysis."""

from typing import List, Dict, Any
import langextract as lx

from ..core.base_analyzer import BaseAnalyzer, AnalysisResult


class StructureAnalyzer(BaseAnalyzer):
    """Analyzer for text structure, coherence, and organizational patterns.
    
    This analyzer identifies topic sentences, paragraph organization,
    transition markers, discourse patterns, and coherence relationships.
    """
    
    def __init__(self):
        super().__init__("structure")
    
    def get_examples(self) -> List[lx.data.ExampleData]:
        """Return example data for structure analysis."""
        return [
            lx.data.ExampleData(
                text="Climate change is one of the most pressing issues of our time. First, rising temperatures are causing ice caps to melt. Second, this leads to rising sea levels. Finally, coastal communities face increasing flood risks.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="topic_sentence",
                        extraction_text="Climate change is one of the most pressing issues of our time.",
                        attributes={
                            "position": "opening",
                            "function": "thesis_statement",
                            "paragraph_number": 1,
                            "educational_note": "주제를 제시하는 주제문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="First",
                        attributes={
                            "type": "sequence",
                            "function": "enumeration",
                            "position": "sentence_initial",
                            "educational_note": "순서를 나타내는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="Second",
                        attributes={
                            "type": "sequence",
                            "function": "enumeration",
                            "position": "sentence_initial",
                            "educational_note": "두 번째 요점을 나타내는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="Finally",
                        attributes={
                            "type": "conclusion",
                            "function": "final_point",
                            "position": "sentence_initial",
                            "educational_note": "마지막 요점을 나타내는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="paragraph_structure",
                        extraction_text="Climate change is one of the most pressing issues of our time. First, rising temperatures are causing ice caps to melt. Second, this leads to rising sea levels. Finally, coastal communities face increasing flood risks.",
                        attributes={
                            "pattern": "topic_sentence_plus_supporting_details",
                            "organization": "chronological_sequence",
                            "coherence_score": "high",
                            "educational_note": "주제문과 뒷받침 문장으로 구성된 단락"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="However, some researchers disagree with this conclusion. On the other hand, the evidence suggests otherwise. Nevertheless, the debate continues in academic circles.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="However",
                        attributes={
                            "type": "contrast",
                            "function": "opposition",
                            "position": "sentence_initial",
                            "educational_note": "대조를 나타내는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="On the other hand",
                        attributes={
                            "type": "contrast",
                            "function": "alternative_viewpoint",
                            "position": "sentence_initial",
                            "educational_note": "다른 관점을 제시하는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="Nevertheless",
                        attributes={
                            "type": "concession",
                            "function": "despite_opposition",
                            "position": "sentence_initial",
                            "educational_note": "양보를 나타내는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="discourse_pattern",
                        extraction_text="However, some researchers disagree with this conclusion. On the other hand, the evidence suggests otherwise. Nevertheless, the debate continues in academic circles.",
                        attributes={
                            "pattern": "argument_counterargument",
                            "rhetorical_function": "presenting_multiple_perspectives",
                            "educational_note": "여러 관점을 제시하는 논증 패턴"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The study examined three main factors. These factors included economic conditions, social influences, and political changes. Each of these elements played a crucial role in the outcome.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="cohesion_device",
                        extraction_text="These factors",
                        attributes={
                            "type": "demonstrative_reference",
                            "refers_to": "three main factors",
                            "cohesion_type": "reference",
                            "educational_note": "앞서 언급한 내용을 가리키는 지시 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="cohesion_device",
                        extraction_text="Each of these elements",
                        attributes={
                            "type": "demonstrative_reference",
                            "refers_to": "economic conditions, social influences, and political changes",
                            "cohesion_type": "reference",
                            "educational_note": "앞서 언급한 요소들을 가리키는 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="paragraph_structure",
                        extraction_text="The study examined three main factors. These factors included economic conditions, social influences, and political changes. Each of these elements played a crucial role in the outcome.",
                        attributes={
                            "pattern": "general_to_specific",
                            "organization": "enumeration_with_elaboration",
                            "coherence_score": "high",
                            "educational_note": "일반적 진술에서 구체적 설명으로 이어지는 구조"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="In conclusion, the research demonstrates clear benefits. As a result, we recommend implementing these changes. Therefore, organizations should consider adopting this approach.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="In conclusion",
                        attributes={
                            "type": "conclusion",
                            "function": "summary_introduction",
                            "position": "sentence_initial",
                            "educational_note": "결론을 도입하는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="As a result",
                        attributes={
                            "type": "cause_effect",
                            "function": "consequence",
                            "position": "sentence_initial",
                            "educational_note": "결과를 나타내는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="transition_marker",
                        extraction_text="Therefore",
                        attributes={
                            "type": "cause_effect",
                            "function": "logical_conclusion",
                            "position": "sentence_initial",
                            "educational_note": "논리적 결론을 나타내는 전환 표현"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="discourse_pattern",
                        extraction_text="In conclusion, the research demonstrates clear benefits. As a result, we recommend implementing these changes. Therefore, organizations should consider adopting this approach.",
                        attributes={
                            "pattern": "conclusion_recommendation",
                            "rhetorical_function": "persuasive_conclusion",
                            "educational_note": "결론에서 권고사항으로 이어지는 설득적 구조"
                        }
                    )
                ]
            )
        ]
    
    def get_prompt_description(self) -> str:
        """Return the prompt description for structure analysis."""
        return """
        Analyze the structural and organizational patterns in the given English text and extract the following information:

        1. **Topic Sentences**: Identify sentences that introduce main ideas
           - Position: opening, middle, closing
           - Function: thesis_statement, topic_introduction, summary
           - Paragraph number
           - Provide Korean educational notes

        2. **Transition Markers**: Identify words and phrases that connect ideas
           - Type: sequence, contrast, cause_effect, addition, conclusion, concession
           - Function: specific purpose (enumeration, opposition, consequence, etc.)
           - Position: sentence_initial, sentence_medial, sentence_final
           - Include Korean explanations of usage

        3. **Paragraph Structure**: Analyze organizational patterns
           - Pattern: topic_sentence_plus_supporting_details, general_to_specific, specific_to_general, chronological, spatial
           - Organization: enumeration, comparison_contrast, cause_effect, problem_solution
           - Coherence score: high, medium, low
           - Provide structural analysis in Korean

        4. **Cohesion Devices**: Identify elements that create text unity
           - Type: reference (pronouns, demonstratives), substitution, ellipsis, lexical_cohesion
           - Refers_to: what the cohesive device points back to
           - Cohesion_type: reference, substitution, conjunction, lexical
           - Include Korean explanations

        5. **Discourse Patterns**: Identify larger rhetorical structures
           - Pattern: argument_counterargument, problem_solution, cause_effect_chain, comparison_contrast
           - Rhetorical_function: persuasive, explanatory, descriptive, narrative
           - Include analysis of effectiveness

        Focus on structural elements that help Korean learners understand how English texts are organized.
        Provide detailed Korean explanations to help understand text flow and logical connections.
        """
    
    def analyze(self, text: str) -> AnalysisResult:
        """Perform structure analysis on the given text."""
        if not self.validate_text(text):
            raise ValueError("Text is not suitable for structure analysis")
        
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
        
        # Add structure-specific metadata
        result.add_metadata("analysis_type", "structure")
        
        # Calculate structural statistics
        paragraphs = self._split_paragraphs(text)
        sentences = self._split_sentences(text)
        
        result.add_metadata("total_paragraphs", len(paragraphs))
        result.add_metadata("total_sentences", len(sentences))
        result.add_metadata("average_sentences_per_paragraph", 
                          len(sentences) / len(paragraphs) if paragraphs else 0)
        
        # Enhance structure analysis
        self._enhance_coherence_analysis(result)
        self._enhance_transition_analysis(result)
        self._analyze_paragraph_patterns(result, paragraphs)
        
        return result
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        paragraphs = text.split('\n\n')
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _split_sentences(self, text: str) -> List[str]:
        """Simple sentence splitting."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _enhance_coherence_analysis(self, result: AnalysisResult) -> None:
        """Enhance coherence analysis with additional metrics."""
        if "cohesion_device" in result.analysis_data:
            cohesion_devices = result.analysis_data["cohesion_device"]
            
            # Count types of cohesion devices
            cohesion_counts = {}
            for device in cohesion_devices:
                device_type = device["attributes"].get("type", "unknown")
                cohesion_counts[device_type] = cohesion_counts.get(device_type, 0) + 1
            
            result.add_metadata("cohesion_device_distribution", cohesion_counts)
            
            # Calculate coherence score based on cohesion devices
            total_devices = len(cohesion_devices)
            sentences_count = result.metadata.get("total_sentences", 1)
            coherence_ratio = total_devices / sentences_count if sentences_count > 0 else 0
            
            result.add_metadata("coherence_ratio", round(coherence_ratio, 3))
    
    def _enhance_transition_analysis(self, result: AnalysisResult) -> None:
        """Enhance transition marker analysis."""
        if "transition_marker" in result.analysis_data:
            transitions = result.analysis_data["transition_marker"]
            
            # Count transition types
            transition_counts = {}
            for transition in transitions:
                transition_type = transition["attributes"].get("type", "unknown")
                transition_counts[transition_type] = transition_counts.get(transition_type, 0) + 1
            
            result.add_metadata("transition_type_distribution", transition_counts)
            
            # Calculate transition density
            total_transitions = len(transitions)
            sentences_count = result.metadata.get("total_sentences", 1)
            transition_density = total_transitions / sentences_count if sentences_count > 0 else 0
            
            result.add_metadata("transition_density", round(transition_density, 3))
            
            # Analyze transition variety
            unique_types = len(transition_counts)
            result.add_metadata("transition_variety_score", unique_types)
    
    def _analyze_paragraph_patterns(self, result: AnalysisResult, paragraphs: List[str]) -> None:
        """Analyze paragraph organization patterns."""
        if "paragraph_structure" in result.analysis_data:
            structures = result.analysis_data["paragraph_structure"]
            
            # Count paragraph patterns
            pattern_counts = {}
            for structure in structures:
                pattern = structure["attributes"].get("pattern", "unknown")
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
            
            result.add_metadata("paragraph_pattern_distribution", pattern_counts)
            
            # Calculate average paragraph length
            if paragraphs:
                avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
                result.add_metadata("average_paragraph_length", round(avg_paragraph_length, 1))
                
                # Analyze paragraph length variation
                lengths = [len(p.split()) for p in paragraphs]
                if len(lengths) > 1:
                    import statistics
                    length_std = statistics.stdev(lengths)
                    result.add_metadata("paragraph_length_variation", round(length_std, 1))
    
    def validate_text(self, text: str) -> bool:
        """Validate if text is suitable for structure analysis."""
        if not super().validate_text(text):
            return False
        
        # Structure analysis needs at least 2 sentences
        sentences = self._split_sentences(text)
        return len(sentences) >= 2
    
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Return configuration schema for structure analyzer."""
        base_schema = super().get_configuration_schema()
        
        structure_schema = {
            "analyze_topic_sentences": {
                "type": "boolean",
                "default": True,
                "description": "Identify topic sentences and main ideas"
            },
            "analyze_transitions": {
                "type": "boolean",
                "default": True,
                "description": "Analyze transition markers and connectors"
            },
            "analyze_paragraph_structure": {
                "type": "boolean",
                "default": True,
                "description": "Analyze paragraph organization patterns"
            },
            "analyze_cohesion": {
                "type": "boolean",
                "default": True,
                "description": "Analyze cohesion devices and text unity"
            },
            "analyze_discourse_patterns": {
                "type": "boolean",
                "default": True,
                "description": "Analyze larger rhetorical structures"
            },
            "coherence_threshold": {
                "type": "number",
                "default": 0.3,
                "description": "Minimum coherence ratio for well-structured text"
            },
            "include_korean_explanations": {
                "type": "boolean",
                "default": True,
                "description": "Include Korean educational explanations"
            }
        }
        
        base_schema.update(structure_schema)
        return base_schema