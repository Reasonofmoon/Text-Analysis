"""Custom exceptions for the English text analyzer."""


class EnglishTextAnalysisError(Exception):
    """Base exception for English text analysis errors."""
    pass


class AnalyzerNotFoundError(EnglishTextAnalysisError):
    """Raised when a requested analyzer is not available."""
    
    def __init__(self, analyzer_name: str):
        self.analyzer_name = analyzer_name
        super().__init__(f"Analyzer not found: {analyzer_name}")


class TextValidationError(EnglishTextAnalysisError):
    """Raised when text validation fails."""
    
    def __init__(self, message: str, validation_errors: list = None):
        self.validation_errors = validation_errors or []
        super().__init__(message)


class TextTooShortError(TextValidationError):
    """Raised when text is too short for meaningful analysis."""
    
    def __init__(self, text_length: int, min_length: int):
        self.text_length = text_length
        self.min_length = min_length
        super().__init__(f"Text too short: {text_length} characters (minimum: {min_length})")


class TextTooLongError(TextValidationError):
    """Raised when text exceeds maximum length limit."""
    
    def __init__(self, text_length: int, max_length: int):
        self.text_length = text_length
        self.max_length = max_length
        super().__init__(f"Text too long: {text_length} characters (maximum: {max_length})")


class APIQuotaExceededError(EnglishTextAnalysisError):
    """Raised when API quota is exceeded."""
    
    def __init__(self, message: str = "API quota exceeded"):
        super().__init__(message)


class APIConnectionError(EnglishTextAnalysisError):
    """Raised when API connection fails."""
    
    def __init__(self, message: str = "Failed to connect to API"):
        super().__init__(message)


class InvalidConfigurationError(EnglishTextAnalysisError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, config_errors: list = None):
        self.config_errors = config_errors or []
        super().__init__(message)


class AnalysisTimeoutError(EnglishTextAnalysisError):
    """Raised when analysis times out."""
    
    def __init__(self, timeout_seconds: int):
        self.timeout_seconds = timeout_seconds
        super().__init__(f"Analysis timed out after {timeout_seconds} seconds")


class AnalysisFailedError(EnglishTextAnalysisError):
    """Raised when analysis fails for an unknown reason."""
    
    def __init__(self, analyzer_name: str, original_error: Exception = None):
        self.analyzer_name = analyzer_name
        self.original_error = original_error
        message = f"Analysis failed for {analyzer_name}"
        if original_error:
            message += f": {str(original_error)}"
        super().__init__(message)


class UnsupportedFormatError(EnglishTextAnalysisError):
    """Raised when an unsupported format is requested."""
    
    def __init__(self, format_name: str, supported_formats: list = None):
        self.format_name = format_name
        self.supported_formats = supported_formats or []
        message = f"Unsupported format: {format_name}"
        if supported_formats:
            message += f". Supported formats: {', '.join(supported_formats)}"
        super().__init__(message)