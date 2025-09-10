"""Text preprocessing and validation utilities."""

import re
from typing import List, Dict, Any, Optional
import unicodedata


class TextPreprocessor:
    """Utility class for text preprocessing and validation."""
    
    def __init__(self):
        # Common patterns for text cleaning
        self.url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.extra_whitespace_pattern = re.compile(r'\s+')
    
    def clean_text(self, text: str, remove_urls: bool = False, remove_emails: bool = False) -> str:
        """Clean and normalize text.
        
        Args:
            text: Input text to clean
            remove_urls: Whether to remove URLs
            remove_emails: Whether to remove email addresses
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Normalize unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        # Remove URLs if requested
        if remove_urls:
            text = self.url_pattern.sub('', text)
        
        # Remove emails if requested
        if remove_emails:
            text = self.email_pattern.sub('', text)
        
        # Normalize whitespace
        text = self.extra_whitespace_pattern.sub(' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def validate_text(self, text: str, min_length: int = 10, max_length: int = 50000) -> Dict[str, Any]:
        """Validate text for analysis suitability.
        
        Args:
            text: Text to validate
            min_length: Minimum required length
            max_length: Maximum allowed length
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "statistics": {}
        }
        
        if not text:
            validation_result["is_valid"] = False
            validation_result["errors"].append("Text is empty")
            return validation_result
        
        # Calculate basic statistics
        char_count = len(text)
        word_count = len(text.split())
        sentence_count = len(re.findall(r'[.!?]+', text))
        
        validation_result["statistics"] = {
            "char_count": char_count,
            "word_count": word_count,
            "sentence_count": sentence_count
        }
        
        # Length validation
        if char_count < min_length:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Text too short (minimum {min_length} characters)")
        
        if char_count > max_length:
            validation_result["is_valid"] = False
            validation_result["errors"].append(f"Text too long (maximum {max_length} characters)")
        
        # Content validation
        if word_count < 3:
            validation_result["warnings"].append("Text has very few words")
        
        if sentence_count == 0:
            validation_result["warnings"].append("No sentence-ending punctuation found")
        
        # Language detection (basic heuristic)
        english_char_ratio = self._calculate_english_ratio(text)
        if english_char_ratio < 0.7:
            validation_result["warnings"].append("Text may not be primarily in English")
        
        validation_result["statistics"]["english_char_ratio"] = english_char_ratio
        
        return validation_result
    
    def _calculate_english_ratio(self, text: str) -> float:
        """Calculate ratio of English characters in text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Ratio of English characters (0.0 to 1.0)
        """
        if not text:
            return 0.0
        
        # Count ASCII letters and common punctuation
        english_chars = sum(1 for char in text if char.isascii() and (char.isalpha() or char in '.,!?;:()[]{}"\'-'))
        total_chars = len([char for char in text if not char.isspace()])
        
        if total_chars == 0:
            return 0.0
        
        return english_chars / total_chars
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using simple heuristics.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        if not text:
            return []
        
        # Simple sentence splitting pattern
        sentence_pattern = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
        sentences = sentence_pattern.split(text)
        
        # Clean up sentences
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        
        return sentences
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs.
        
        Args:
            text: Text to split
            
        Returns:
            List of paragraphs
        """
        if not text:
            return []
        
        # Split on double newlines
        paragraphs = text.split('\n\n')
        
        # Clean up paragraphs
        paragraphs = [para.strip().replace('\n', ' ') for para in paragraphs if para.strip()]
        
        return paragraphs
    
    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """Extract metadata from text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with text metadata
        """
        metadata = {}
        
        # Basic statistics
        metadata["char_count"] = len(text)
        metadata["word_count"] = len(text.split())
        metadata["sentence_count"] = len(self.split_into_sentences(text))
        metadata["paragraph_count"] = len(self.split_into_paragraphs(text))
        
        # Average lengths
        words = text.split()
        if words:
            metadata["avg_word_length"] = sum(len(word.strip('.,!?;:()[]{}"\'-')) for word in words) / len(words)
        else:
            metadata["avg_word_length"] = 0
        
        sentences = self.split_into_sentences(text)
        if sentences:
            metadata["avg_sentence_length"] = sum(len(sentence.split()) for sentence in sentences) / len(sentences)
        else:
            metadata["avg_sentence_length"] = 0
        
        # Language characteristics
        metadata["english_char_ratio"] = self._calculate_english_ratio(text)
        
        # Complexity indicators
        metadata["unique_word_ratio"] = len(set(word.lower() for word in words)) / len(words) if words else 0
        
        return metadata