"""Base Language Parser with language detection and parser registry."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import re


class ParserError(Exception):
    """Exception raised when parsing fails."""
    pass


@dataclass
class ParseResult:
    """Result of parsing operation."""
    language: str
    ast: Any
    code: str
    success: bool
    error_message: Optional[str] = None
    line_number: Optional[int] = None


class BaseParser(ABC):
    """Abstract base class for language-specific parsers."""
    
    @abstractmethod
    def parse(self, code: str) -> ParseResult:
        """Parse code into AST."""
        pass
    
    @abstractmethod
    def get_language(self) -> str:
        """Return the language this parser handles."""
        pass


class LanguageParser:
    """Main parser class with language detection and parser registry."""
    
    # File extension to language mapping
    EXTENSION_MAP = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.mjs': 'javascript',
        '.java': 'java',
    }
    
    # Content-based language detection patterns
    CONTENT_PATTERNS = {
        'python': [
            re.compile(r'^\s*def\s+\w+\s*\('),
            re.compile(r'^\s*class\s+\w+\s*[:\(]'),
            re.compile(r'^\s*import\s+\w+'),
            re.compile(r'^\s*from\s+\w+\s+import'),
        ],
        'javascript': [
            re.compile(r'^\s*function\s+\w+\s*\('),
            re.compile(r'^\s*const\s+\w+\s*='),
            re.compile(r'^\s*let\s+\w+\s*='),
            re.compile(r'^\s*var\s+\w+\s*='),
            re.compile(r'^\s*class\s+\w+\s*\{'),
        ],
        'java': [
            re.compile(r'^\s*public\s+class\s+\w+'),
            re.compile(r'^\s*private\s+class\s+\w+'),
            re.compile(r'^\s*package\s+[\w.]+;'),
            re.compile(r'^\s*import\s+[\w.]+;'),
        ],
    }
    
    def __init__(self):
        """Initialize the parser with an empty registry."""
        self._parsers: Dict[str, BaseParser] = {}
    
    def register_parser(self, language: str, parser: BaseParser) -> None:
        """Register a language-specific parser.
        
        Args:
            language: The language identifier (e.g., 'python', 'javascript')
            parser: The parser instance for this language
        """
        self._parsers[language] = parser
    
    def detect_language(self, code: str, filename: str = "") -> str:
        """Detect programming language from file extension or content.
        
        Args:
            code: The source code content
            filename: Optional filename with extension
            
        Returns:
            Detected language identifier
            
        Raises:
            ParserError: If language cannot be detected
        """
        # Try extension-based detection first
        if filename:
            for ext, lang in self.EXTENSION_MAP.items():
                if filename.endswith(ext):
                    return lang
        
        # Fall back to content-based detection
        detected_lang = self._detect_from_content(code)
        if detected_lang:
            return detected_lang
        
        raise ParserError(
            f"Unable to detect language for file: {filename or 'unknown'}. "
            f"Supported extensions: {', '.join(self.EXTENSION_MAP.keys())}"
        )
    
    def _detect_from_content(self, code: str) -> Optional[str]:
        """Detect language from code content patterns.
        
        Args:
            code: The source code content
            
        Returns:
            Detected language or None if no match
        """
        lines = code.split('\n')
        
        # Score each language based on pattern matches
        scores = {lang: 0 for lang in self.CONTENT_PATTERNS.keys()}
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('//'):
                continue
                
            for lang, patterns in self.CONTENT_PATTERNS.items():
                for pattern in patterns:
                    if pattern.search(line):
                        scores[lang] += 1
        
        # Return language with highest score if any matches found
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        
        return None
    
    def parse(self, code: str, language: str) -> ParseResult:
        """Parse code using the appropriate language parser.
        
        Args:
            code: The source code to parse
            language: The programming language
            
        Returns:
            ParseResult containing AST and metadata
            
        Raises:
            ParserError: If parser not found or parsing fails
        """
        if language not in self._parsers:
            raise ParserError(
                f"No parser registered for language: {language}. "
                f"Supported languages: {', '.join(self.get_supported_languages())}"
            )
        
        parser = self._parsers[language]
        return parser.parse(code)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages.
        
        Returns:
            List of language identifiers
        """
        return list(self._parsers.keys())
