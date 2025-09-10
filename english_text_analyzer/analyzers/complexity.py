"""Complexity analyzer for English text analysis."""

from typing import List, Dict, Any
import langextract as lx
import math
import re

from ..core.base_analyzer import BaseAnalyzer, AnalysisResult


class ComplexityAnalyzer(BaseAnalyzer):
    """Analyzer for text complexity, readability, and CEFR level estimation.
    
    This analyzer calculates readability scores, estimates CEFR levels,
    measures lexical diversity, and provides text adaptation recommendations.
    """
    
    def __init__(self):
        super().__init__("complexity")
    
    def get_examples(self) -> List[lx.data.ExampleData]:
        """Return example data for complexity analysis."""
        return [
            lx.data.ExampleData(
                text="The cat sat on the mat. It was warm and sunny.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="readability_assessment",
                        extraction_text="The cat sat on the mat. It was warm and sunny.",
                        attributes={
                            "flesch_kincaid_grade": "2.3",
                            "flesch_reading_ease": "92.8",
                            "cefr_level": "A1",
                            "complexity_level": "elementary",
                            "avg_sentence_length": "8.0",
                            "avg_syllables_per_word": "1.2",
                            "educational_note": "매우 간단한 문장 구조와 기초 어휘로 구성된 초급 수준의 텍스트"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="Despite the challenging weather conditions, the expedition team successfully reached their destination after three days of hiking through the mountain trails.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="readability_assessment",
                        extraction_text="Despite the challenging weather conditions, the expedition team successfully reached their destination after three days of hiking through the mountain trails.",
                        attributes={
                            "flesch_kincaid_grade": "12.1",
                            "flesch_reading_ease": "45.2",
                            "cefr_level": "B2",
                            "complexity_level": "intermediate",
                            "avg_sentence_length": "24.0",
                            "avg_syllables_per_word": "1.8",
                            "educational_note": "복잡한 문장 구조와 중급 어휘를 포함한 중상급 수준의 텍스트"
                        }
                    )
                ]
            ),
            lx.data.ExampleData(
                text="The paradigmatic shift in contemporary linguistic theory necessitates a comprehensive reevaluation of traditional syntactic frameworks, particularly in light of recent developments in computational linguistics and corpus-based methodologies.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="readability_assessment",
                        extraction_text="The paradigmatic shift in contemporary linguistic theory necessitates a comprehensive reevaluation of traditional syntactic frameworks, particularly in light of recent developments in computational linguistics and corpus-based methodologies.",
                        attributes={
                            "flesch_kincaid_grade": "18.7",
                            "flesch_reading_ease": "12.4",
                            "cefr_level": "C2",
                            "complexity_level": "advanced",
                            "avg_sentence_length": "31.0",
                            "avg_syllables_per_word": "2.4",
                            "educational_note": "고도로 복잡한 학술적 문체와 전문 용어를 포함한 고급 수준의 텍스트"
                        }
                    )
                ]
            )
        ]
    
    def get_prompt_description(self) -> str:
        """Return the prompt description for complexity analysis."""
        return """
        Analyze the complexity and readability of the given English text. Focus on:
        
        1. **Readability Metrics**: Calculate Flesch-Kincaid Grade Level and Flesch Reading Ease scores
        2. **CEFR Level Estimation**: Estimate the Common European Framework level (A1, A2, B1, B2, C1, C2)
        3. **Sentence Complexity**: Measure average sentence length, clause density, and syntactic complexity
        4. **Lexical Complexity**: Assess vocabulary diversity, word length distribution, and academic word usage
        5. **Text Adaptation Recommendations**: Suggest ways to simplify or enhance the text for different proficiency levels
        
        For each complexity assessment, provide:
        - Specific readability scores with explanations
        - CEFR level justification based on vocabulary and structure
        - Quantitative metrics (sentence length, syllable counts, etc.)
        - Educational recommendations for teachers and learners
        - Suggestions for text adaptation or scaffolding
        
        Focus on educational utility and provide clear explanations that help teachers understand
        why a text is at a particular complexity level and how it can be used effectively in instruction.
        """
    
    def analyze(self, text: str) -> AnalysisResult:
        """Perform complexity analysis on the given text.
        
        Args:
            text: The text to analyze
            
        Returns:
            AnalysisResult containing complexity analysis
        """
        try:
            # Use langextract for analysis
            examples = self.get_examples()
            prompt_description = self.get_prompt_description()
            
            annotated_doc = lx.extract(
                text=text,
                examples=examples,
                prompt_description=prompt_description
            )
            
            # Post-process the results
            return self.post_process_results(annotated_doc)
            
        except Exception as e:
            # Fallback to direct analysis if langextract fails
            return self._fallback_analysis(text)
    
    def calculate_readability_scores(self, text: str) -> Dict[str, float]:
        """Calculate various readability scores for the text."""
        sentences = self._count_sentences(text)
        words = self._count_words(text)
        syllables = self._count_syllables(text)
        
        if sentences == 0 or words == 0:
            return {"flesch_kincaid_grade": 0.0, "flesch_reading_ease": 0.0}
        
        # Flesch-Kincaid Grade Level
        fk_grade = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        
        # Flesch Reading Ease
        fre = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        
        return {
            "flesch_kincaid_grade": round(max(0, fk_grade), 1),
            "flesch_reading_ease": round(max(0, min(100, fre)), 1)
        }
    
    def estimate_cefr_level(self, text: str) -> str:
        """Estimate CEFR level based on text complexity."""
        scores = self.calculate_readability_scores(text)
        fk_grade = scores["flesch_kincaid_grade"]
        
        # CEFR level estimation based on Flesch-Kincaid grade
        if fk_grade <= 3:
            return "A1"
        elif fk_grade <= 6:
            return "A2"
        elif fk_grade <= 9:
            return "B1"
        elif fk_grade <= 12:
            return "B2"
        elif fk_grade <= 16:
            return "C1"
        else:
            return "C2"
    
    def analyze_lexical_diversity(self, text: str) -> Dict[str, float]:
        """Analyze lexical diversity and vocabulary complexity."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        if not words:
            return {"ttr": 0.0, "avg_word_length": 0.0, "long_word_ratio": 0.0}
        
        unique_words = set(words)
        
        # Type-Token Ratio
        ttr = len(unique_words) / len(words)
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Long word ratio (words with 6+ characters)
        long_words = [word for word in words if len(word) >= 6]
        long_word_ratio = len(long_words) / len(words)
        
        return {
            "ttr": round(ttr, 3),
            "avg_word_length": round(avg_word_length, 1),
            "long_word_ratio": round(long_word_ratio, 3)
        }
    
    def analyze_syntactic_complexity(self, text: str) -> Dict[str, float]:
        """Analyze syntactic complexity of the text."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {"avg_clauses_per_sentence": 0.0, "complex_sentence_ratio": 0.0, "syntactic_complexity_score": 0.0}
        
        total_clauses = 0
        complex_sentences = 0
        
        for sentence in sentences:
            # Count clauses by looking for conjunctions and relative pronouns
            clause_indicators = re.findall(r'\b(and|but|or|because|since|although|while|when|if|that|which|who|where)\b', sentence.lower())
            clauses = len(clause_indicators) + 1  # Base sentence + subordinate clauses
            total_clauses += clauses
            
            # Complex sentence if it has subordinate clauses
            if clauses > 1:
                complex_sentences += 1
        
        avg_clauses = total_clauses / len(sentences)
        complex_ratio = complex_sentences / len(sentences)
        
        # Syntactic complexity score (0-10 scale)
        complexity_score = min(10, avg_clauses * 2 + complex_ratio * 3)
        
        return {
            "avg_clauses_per_sentence": round(avg_clauses, 2),
            "complex_sentence_ratio": round(complex_ratio, 3),
            "syntactic_complexity_score": round(complexity_score, 2)
        }
    
    def calculate_information_density(self, text: str) -> Dict[str, float]:
        """Calculate information density metrics."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        sentences = self._count_sentences(text)
        
        if not words or sentences == 0:
            return {"content_word_ratio": 0.0, "information_density": 0.0}
        
        # Function words (articles, prepositions, conjunctions, etc.)
        function_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        content_words = [word for word in words if word not in function_words]
        content_word_ratio = len(content_words) / len(words)
        
        # Information density: content words per sentence
        info_density = len(content_words) / sentences
        
        return {
            "content_word_ratio": round(content_word_ratio, 3),
            "information_density": round(info_density, 2)
        }
    
    def generate_adaptation_recommendations(self, complexity_data: Dict[str, Any]) -> List[str]:
        """Generate text adaptation recommendations based on complexity analysis."""
        recommendations = []
        
        fk_grade = complexity_data.get("readability_scores", {}).get("flesch_kincaid_grade", 0)
        cefr_level = complexity_data.get("cefr_level", "Unknown")
        syntactic_score = complexity_data.get("syntactic_complexity", {}).get("syntactic_complexity_score", 0)
        
        # Recommendations based on readability
        if fk_grade > 12:
            recommendations.extend([
                "문장을 더 짧게 나누어 가독성 향상",
                "복잡한 어휘를 더 간단한 동의어로 대체",
                "수동태를 능동태로 변환하여 명확성 증대"
            ])
        elif fk_grade < 6:
            recommendations.extend([
                "어휘 다양성을 높여 학습 효과 증대",
                "더 복잡한 문장 구조 도입으로 도전 과제 제공",
                "학술적 어휘 점진적 도입"
            ])
        
        # Recommendations based on syntactic complexity
        if syntactic_score > 7:
            recommendations.extend([
                "복잡한 절 구조를 단순화하여 이해도 향상",
                "긴 문장을 여러 개의 짧은 문장으로 분할",
                "접속사 사용을 줄여 문장 구조 단순화"
            ])
        elif syntactic_score < 3:
            recommendations.extend([
                "종속절을 활용한 문장 구조 복잡화",
                "다양한 접속사와 전환어 도입",
                "관계대명사절 활용으로 정보 밀도 증가"
            ])
        
        # CEFR-specific recommendations
        if cefr_level in ["A1", "A2"]:
            recommendations.extend([
                "기본 시제와 문법 구조에 집중",
                "일상적 주제와 친숙한 어휘 활용",
                "반복 학습을 위한 패턴 강화"
            ])
        elif cefr_level in ["C1", "C2"]:
            recommendations.extend([
                "추상적 개념과 복잡한 논증 구조 도입",
                "전문 분야 어휘와 학술적 표현 활용",
                "비판적 사고를 요구하는 내용 구성"
            ])
        
        return recommendations[:8]  # Limit to 8 most relevant recommendations
    
    def _count_sentences(self, text: str) -> int:
        """Count sentences in the text."""
        sentence_endings = re.findall(r'[.!?]+', text)
        return max(1, len(sentence_endings))
    
    def _count_words(self, text: str) -> int:
        """Count words in the text."""
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        return len(words)
    
    def _count_syllables(self, text: str) -> int:
        """Count syllables in the text using a simple heuristic."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        total_syllables = 0
        
        for word in words:
            syllables = self._count_syllables_in_word(word)
            total_syllables += syllables
        
        return total_syllables
    
    def _count_syllables_in_word(self, word: str) -> int:
        """Count syllables in a single word using vowel patterns."""
        word = word.lower()
        vowels = "aeiouy"
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def post_process_results(self, raw_results: lx.data.AnnotatedDocument) -> AnalysisResult:
        """Post-process the raw langextract results into structured complexity analysis."""
        complexity_data = {
            "readability_scores": {},
            "cefr_level": "Unknown",
            "lexical_diversity": {},
            "sentence_metrics": {},
            "syntactic_complexity": {},
            "information_density": {},
            "recommendations": []
        }
        
        text = raw_results.text
        
        # Calculate readability scores
        complexity_data["readability_scores"] = self.calculate_readability_scores(text)
        
        # Estimate CEFR level
        complexity_data["cefr_level"] = self.estimate_cefr_level(text)
        
        # Analyze lexical diversity
        complexity_data["lexical_diversity"] = self.analyze_lexical_diversity(text)
        
        # Calculate sentence metrics
        sentences = self._count_sentences(text)
        words = self._count_words(text)
        complexity_data["sentence_metrics"] = {
            "avg_sentence_length": round(words / sentences, 1) if sentences > 0 else 0,
            "total_sentences": sentences,
            "total_words": words
        }
        
        # Analyze syntactic complexity
        complexity_data["syntactic_complexity"] = self.analyze_syntactic_complexity(text)
        
        # Calculate information density
        complexity_data["information_density"] = self.calculate_information_density(text)
        
        # Generate adaptation recommendations
        complexity_data["recommendations"] = self.generate_adaptation_recommendations(complexity_data)
        
        # Process extractions from langextract
        for extraction in raw_results.extractions:
            if extraction.extraction_class == "readability_assessment":
                # Additional processing can be added here
                pass
        
        result = AnalysisResult(
            analyzer_name="complexity",
            analysis_data={"complexity_analysis": [complexity_data]}
        )
        result.results = complexity_data
        result.confidence_score = 0.85
        result.processing_time = 0.0
        return result
    
    def _fallback_analysis(self, text: str) -> AnalysisResult:
        """Fallback analysis when langextract is not available.
        
        Args:
            text: The text to analyze
            
        Returns:
            AnalysisResult with basic complexity analysis
        """
        complexity_data = {
            "readability_scores": self.calculate_readability_scores(text),
            "cefr_level": self.estimate_cefr_level(text),
            "lexical_diversity": self.analyze_lexical_diversity(text),
            "sentence_metrics": {},
            "syntactic_complexity": self.analyze_syntactic_complexity(text),
            "information_density": self.calculate_information_density(text),
            "recommendations": []
        }
        
        # Calculate sentence metrics
        sentences = self._count_sentences(text)
        words = self._count_words(text)
        complexity_data["sentence_metrics"] = {
            "avg_sentence_length": round(words / sentences, 1) if sentences > 0 else 0,
            "total_sentences": sentences,
            "total_words": words
        }
        
        # Generate recommendations
        complexity_data["recommendations"] = self.generate_adaptation_recommendations(complexity_data)
        
        return AnalysisResult(
            analyzer_name="complexity",
            analysis_data={"complexity_analysis": [complexity_data]}
        )
                      