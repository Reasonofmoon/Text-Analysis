"""Content analyzer for English text analysis."""

from typing import List, Dict, Any
import langextract as lx

from ..core.base_analyzer import BaseAnalyzer, AnalysisResult


class ContentAnalyzer(BaseAnalyzer):
    """Analyzer for content structure, main ideas, and argumentation patterns.
    
    This analyzer identifies main ideas, supporting details, evidence types,
    argument structures, and hierarchical content organization.
    """
    
    def __init__(self):
        super().__init__("content")
    
    def get_examples(self) -> List[lx.data.ExampleData]:
        """Return example data for content analysis."""
        return [
            lx.data.ExampleData(
                text="Education is the foundation of personal and societal development. It provides individuals with knowledge and skills necessary for success. Furthermore, education promotes critical thinking and creativity. For example, students who receive quality education are more likely to become innovative leaders.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="main_idea",
                        extraction_text="Education is the foundation of personal and societal development.",
                        attributes={
                            "type": "thesis_statement",
                            "position": "opening",
                            "scope": "general_claim",
                            "educational_note": "교육의 중요성을 주장하는 주제문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="supporting_detail",
                        extraction_text="It provides individuals with knowledge and skills necessary for success.",
                        attributes={
                            "type": "explanation",
                            "support_type": "elaboration",
                            "relates_to": "Education is the foundation of personal and societal development",
                            "educational_note": "주제문을 뒷받침하는 설명"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="supporting_detail",
                        extraction_text="Furthermore, education promotes critical thinking and creativity.",
                        attributes={
                            "type": "additional_benefit",
                            "support_type": "elaboration",
                            "relates_to": "Education is the foundation of personal and societal development",
                            "educational_note": "교육의 추가적 이점을 제시"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="evidence",
                        extraction_text="For example, students who receive quality education are more likely to become innovative leaders.",
                        attributes={
                            "evidence_type": "example",
                            "strength": "moderate",
                            "supports": "education promotes critical thinking and creativity",
                            "educational_note": "구체적 예시를 통한 뒷받침"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="Climate change poses significant threats to global ecosystems. According to NASA data, global temperatures have risen by 1.1°C since 1880. Dr. Smith, a leading climatologist, argues that immediate action is required. This evidence clearly demonstrates the urgency of addressing climate change.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="main_idea",
                        extraction_text="Climate change poses significant threats to global ecosystems.",
                        attributes={
                            "type": "problem_statement",
                            "position": "opening",
                            "scope": "global_issue",
                            "educational_note": "문제를 제기하는 주제문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="evidence",
                        extraction_text="According to NASA data, global temperatures have risen by 1.1°C since 1880.",
                        attributes={
                            "evidence_type": "statistical_data",
                            "source": "NASA",
                            "strength": "strong",
                            "supports": "Climate change poses significant threats",
                            "educational_note": "권위 있는 기관의 통계 자료"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="evidence",
                        extraction_text="Dr. Smith, a leading climatologist, argues that immediate action is required.",
                        attributes={
                            "evidence_type": "expert_opinion",
                            "source": "Dr. Smith",
                            "expertise": "climatologist",
                            "strength": "strong",
                            "supports": "urgency of addressing climate change",
                            "educational_note": "전문가 의견을 통한 뒷받침"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="supporting_detail",
                        extraction_text="This evidence clearly demonstrates the urgency of addressing climate change.",
                        attributes={
                            "type": "conclusion_statement",
                            "support_type": "synthesis",
                            "relates_to": "Climate change poses significant threats",
                            "educational_note": "증거를 종합한 결론"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="Some critics argue that technology harms social interaction. However, research shows that technology can actually enhance communication. While face-to-face interaction remains important, digital tools provide new opportunities for connection.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="argument_structure",
                        extraction_text="Some critics argue that technology harms social interaction.",
                        attributes={
                            "component": "opposing_claim",
                            "argument_type": "counterargument_acknowledgment",
                            "position": "opposing_viewpoint",
                            "educational_note": "반대 의견을 인정하는 주장"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="argument_structure",
                        extraction_text="However, research shows that technology can actually enhance communication.",
                        attributes={
                            "component": "main_claim",
                            "argument_type": "refutation",
                            "position": "author_viewpoint",
                            "educational_note": "반박을 통한 주장 제시"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="argument_structure",
                        extraction_text="While face-to-face interaction remains important, digital tools provide new opportunities for connection.",
                        attributes={
                            "component": "warrant",
                            "argument_type": "balanced_perspective",
                            "position": "qualifying_statement",
                            "educational_note": "균형잡힌 관점을 제시하는 근거"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="evidence",
                        extraction_text="research shows that technology can actually enhance communication",
                        attributes={
                            "evidence_type": "research_findings",
                            "source": "research",
                            "strength": "moderate",
                            "supports": "technology can enhance communication",
                            "educational_note": "연구 결과를 통한 뒷받침"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The study examined three key factors affecting student performance. First, socioeconomic background significantly influences academic achievement. Second, teacher quality plays a crucial role in learning outcomes. Third, school resources determine educational opportunities. These findings suggest that multiple interventions are necessary.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="main_idea",
                        extraction_text="The study examined three key factors affecting student performance.",
                        attributes={
                            "type": "research_overview",
                            "position": "opening",
                            "scope": "study_summary",
                            "educational_note": "연구 개요를 제시하는 주제문"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="supporting_detail",
                        extraction_text="First, socioeconomic background significantly influences academic achievement.",
                        attributes={
                            "type": "finding",
                            "support_type": "research_result",
                            "sequence": "first",
                            "relates_to": "factors affecting student performance",
                            "educational_note": "첫 번째 연구 결과"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="supporting_detail",
                        extraction_text="Second, teacher quality plays a crucial role in learning outcomes.",
                        attributes={
                            "type": "finding",
                            "support_type": "research_result",
                            "sequence": "second",
                            "relates_to": "factors affecting student performance",
                            "educational_note": "두 번째 연구 결과"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="supporting_detail",
                        extraction_text="Third, school resources determine educational opportunities.",
                        attributes={
                            "type": "finding",
                            "support_type": "research_result",
                            "sequence": "third",
                            "relates_to": "factors affecting student performance",
                            "educational_note": "세 번째 연구 결과"
                        }
                    ),
                    lx.data.Extraction(
                        extraction_class="main_idea",
                        extraction_text="These findings suggest that multiple interventions are necessary.",
                        attributes={
                            "type": "conclusion",
                            "position": "closing",
                            "scope": "implication",
                            "educational_note": "연구 결과의 함의를 제시하는 결론"
                        }
                    )
                ]
            )
        ]
    
    def get_prompt_description(self) -> str:
        """Return the prompt description for content analysis."""
        return """
        Analyze the content structure and argumentation in the given English text and extract the following information:

        1. **Main Ideas**: Identify central themes and key points
           - Type: thesis_statement, problem_statement, research_overview, conclusion
           - Position: opening, middle, closing
           - Scope: general_claim, specific_point, global_issue, study_summary, implication
           - Provide Korean educational notes

        2. **Supporting Details**: Identify information that supports main ideas
           - Type: explanation, example, finding, additional_benefit, conclusion_statement
           - Support_type: elaboration, research_result, synthesis, specification
           - Sequence: first, second, third (if applicable)
           - Relates_to: which main idea this detail supports
           - Include Korean explanations

        3. **Evidence**: Identify different types of supporting evidence
           - Evidence_type: example, statistical_data, expert_opinion, research_findings, analogy, case_study
           - Source: where the evidence comes from
           - Strength: strong, moderate, weak
           - Supports: what claim or idea the evidence supports
           - Provide Korean analysis of evidence quality

        4. **Argument Structure**: Identify components of argumentation
           - Component: main_claim, opposing_claim, warrant, backing, qualifier, rebuttal
           - Argument_type: assertion, counterargument_acknowledgment, refutation, balanced_perspective
           - Position: author_viewpoint, opposing_viewpoint, qualifying_statement
           - Include Korean explanations of argument logic

        5. **Content Hierarchy**: Identify the organizational structure
           - Level: primary, secondary, tertiary
           - Relationship: supports, contradicts, elaborates, exemplifies
           - Function: introduce, develop, conclude, transition

        Focus on content elements that help Korean learners understand how English texts present and develop ideas.
        Provide detailed Korean explanations to help understand argument structure and evidence evaluation.
        """
    
    def analyze(self, text: str) -> AnalysisResult:
        """Perform content analysis on the given text."""
        if not self.validate_text(text):
            raise ValueError("Text is not suitable for content analysis")
        
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
        
        # Add content-specific metadata
        result.add_metadata("analysis_type", "content")
        
        # Calculate content statistics
        sentences = self._split_sentences(text)
        result.add_metadata("total_sentences", len(sentences))
        
        # Enhance content analysis
        self._enhance_main_idea_analysis(result)
        self._enhance_evidence_analysis(result)
        self._enhance_argument_analysis(result)
        self._create_content_hierarchy(result)
        
        return result
    
    def _split_sentences(self, text: str) -> List[str]:
        """Simple sentence splitting."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _enhance_main_idea_analysis(self, result: AnalysisResult) -> None:
        """Enhance main idea analysis with additional insights."""
        if "main_idea" in result.analysis_data:
            main_ideas = result.analysis_data["main_idea"]
            
            # Count main idea types
            idea_types = {}
            for idea in main_ideas:
                idea_type = idea["attributes"].get("type", "unknown")
                idea_types[idea_type] = idea_types.get(idea_type, 0) + 1
            
            result.add_metadata("main_idea_distribution", idea_types)
            
            # Analyze main idea positions
            positions = {}
            for idea in main_ideas:
                position = idea["attributes"].get("position", "unknown")
                positions[position] = positions.get(position, 0) + 1
            
            result.add_metadata("main_idea_positions", positions)
            
            # Calculate idea density
            total_ideas = len(main_ideas)
            sentences_count = result.metadata.get("total_sentences", 1)
            idea_density = total_ideas / sentences_count if sentences_count > 0 else 0
            result.add_metadata("main_idea_density", round(idea_density, 3))
    
    def _enhance_evidence_analysis(self, result: AnalysisResult) -> None:
        """Enhance evidence analysis with quality assessment."""
        if "evidence" in result.analysis_data:
            evidence_items = result.analysis_data["evidence"]
            
            # Count evidence types
            evidence_types = {}
            for evidence in evidence_items:
                evidence_type = evidence["attributes"].get("evidence_type", "unknown")
                evidence_types[evidence_type] = evidence_types.get(evidence_type, 0) + 1
            
            result.add_metadata("evidence_type_distribution", evidence_types)
            
            # Analyze evidence strength
            strength_counts = {}
            for evidence in evidence_items:
                strength = evidence["attributes"].get("strength", "unknown")
                strength_counts[strength] = strength_counts.get(strength, 0) + 1
            
            result.add_metadata("evidence_strength_distribution", strength_counts)
            
            # Calculate evidence quality score
            strength_scores = {"strong": 3, "moderate": 2, "weak": 1}
            total_score = sum(strength_scores.get(evidence["attributes"].get("strength", ""), 1) 
                            for evidence in evidence_items)
            avg_evidence_quality = total_score / len(evidence_items) if evidence_items else 0
            result.add_metadata("average_evidence_quality", round(avg_evidence_quality, 2))
    
    def _enhance_argument_analysis(self, result: AnalysisResult) -> None:
        """Enhance argument structure analysis."""
        if "argument_structure" in result.analysis_data:
            arguments = result.analysis_data["argument_structure"]
            
            # Count argument components
            component_counts = {}
            for arg in arguments:
                component = arg["attributes"].get("component", "unknown")
                component_counts[component] = component_counts.get(component, 0) + 1
            
            result.add_metadata("argument_component_distribution", component_counts)
            
            # Analyze argument types
            arg_types = {}
            for arg in arguments:
                arg_type = arg["attributes"].get("argument_type", "unknown")
                arg_types[arg_type] = arg_types.get(arg_type, 0) + 1
            
            result.add_metadata("argument_type_distribution", arg_types)
            
            # Calculate argument complexity
            complexity_scores = {
                "assertion": 1,
                "counterargument_acknowledgment": 3,
                "refutation": 4,
                "balanced_perspective": 4
            }
            
            total_complexity = sum(complexity_scores.get(arg["attributes"].get("argument_type", ""), 1) 
                                 for arg in arguments)
            avg_complexity = total_complexity / len(arguments) if arguments else 0
            result.add_metadata("argument_complexity_score", round(avg_complexity, 2))
    
    def _create_content_hierarchy(self, result: AnalysisResult) -> None:
        """Create hierarchical outline of content structure."""
        hierarchy = {
            "primary_ideas": [],
            "secondary_details": [],
            "supporting_evidence": []
        }
        
        # Organize main ideas
        if "main_idea" in result.analysis_data:
            for idea in result.analysis_data["main_idea"]:
                hierarchy["primary_ideas"].append({
                    "text": idea["text"],
                    "type": idea["attributes"].get("type", ""),
                    "position": idea["attributes"].get("position", "")
                })
        
        # Organize supporting details
        if "supporting_detail" in result.analysis_data:
            for detail in result.analysis_data["supporting_detail"]:
                hierarchy["secondary_details"].append({
                    "text": detail["text"],
                    "type": detail["attributes"].get("type", ""),
                    "relates_to": detail["attributes"].get("relates_to", "")
                })
        
        # Organize evidence
        if "evidence" in result.analysis_data:
            for evidence in result.analysis_data["evidence"]:
                hierarchy["supporting_evidence"].append({
                    "text": evidence["text"],
                    "type": evidence["attributes"].get("evidence_type", ""),
                    "strength": evidence["attributes"].get("strength", ""),
                    "supports": evidence["attributes"].get("supports", "")
                })
        
        result.add_metadata("content_hierarchy", hierarchy)
    
    def validate_text(self, text: str) -> bool:
        """Validate if text is suitable for content analysis."""
        if not super().validate_text(text):
            return False
        
        # Content analysis needs at least 2 sentences with substantial content
        sentences = self._split_sentences(text)
        return len(sentences) >= 2 and sum(len(s.split()) for s in sentences) >= 20
    
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Return configuration schema for content analyzer."""
        base_schema = super().get_configuration_schema()
        
        content_schema = {
            "analyze_main_ideas": {
                "type": "boolean",
                "default": True,
                "description": "Identify main ideas and central themes"
            },
            "analyze_supporting_details": {
                "type": "boolean",
                "default": True,
                "description": "Analyze supporting details and elaboration"
            },
            "analyze_evidence": {
                "type": "boolean",
                "default": True,
                "description": "Identify and evaluate evidence types"
            },
            "analyze_argument_structure": {
                "type": "boolean",
                "default": True,
                "description": "Analyze argumentation patterns"
            },
            "create_content_hierarchy": {
                "type": "boolean",
                "default": True,
                "description": "Create hierarchical content outline"
            },
            "evidence_quality_threshold": {
                "type": "number",
                "default": 2.0,
                "description": "Minimum evidence quality score for strong arguments"
            },
            "include_korean_explanations": {
                "type": "boolean",
                "default": True,
                "description": "Include Korean educational explanations"
            }
        }
        
        base_schema.update(content_schema)
        return base_schema