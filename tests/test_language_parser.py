"""Unit tests for Language Parser component."""

import pytest
from src.parsers import (
    LanguageParser, 
    PythonParser, 
    JavaScriptParser, 
    JavaParser,
    ParserError
)


class TestLanguageDetection:
    """Test language detection functionality."""
    
    def test_detect_python_by_extension(self):
        """Test Python detection from .py extension."""
        parser = LanguageParser()
        code = "print('hello')"
        lang = parser.detect_language(code, "test.py")
        assert lang == "python"
    
    def test_detect_javascript_by_extension(self):
        """Test JavaScript detection from .js extension."""
        parser = LanguageParser()
        code = "console.log('hello');"
        lang = parser.detect_language(code, "test.js")
        assert lang == "javascript"
    
    def test_detect_java_by_extension(self):
        """Test Java detection from .java extension."""
        parser = LanguageParser()
        code = "public class Test {}"
        lang = parser.detect_language(code, "Test.java")
        assert lang == "java"
    
    def test_detect_python_by_content(self):
        """Test Python detection from code content."""
        parser = LanguageParser()
        code = """
def hello():
    print('world')
"""
        lang = parser.detect_language(code, "")
        assert lang == "python"
    
    def test_detect_javascript_by_content(self):
        """Test JavaScript detection from code content."""
        parser = LanguageParser()
        code = """
function hello() {
    console.log('world');
}
"""
        lang = parser.detect_language(code, "")
        assert lang == "javascript"
    
    def test_detect_java_by_content(self):
        """Test Java detection from code content."""
        parser = LanguageParser()
        code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
"""
        lang = parser.detect_language(code, "")
        assert lang == "java"
    
    def test_unsupported_language_raises_error(self):
        """Test that unsupported language raises ParserError."""
        parser = LanguageParser()
        code = "some random text"
        with pytest.raises(ParserError) as exc_info:
            parser.detect_language(code, "test.txt")
        assert "Unable to detect language" in str(exc_info.value)


class TestPythonParser:
    """Test Python parser functionality."""
    
    def test_parse_valid_python_code(self):
        """Test parsing valid Python code."""
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        
        code = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
"""
        result = parser.parse(code, 'python')
        assert result.success is True
        assert result.language == 'python'
        assert result.ast is not None
        assert result.error_message is None
    
    def test_parse_invalid_python_code(self):
        """Test parsing invalid Python code returns error."""
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        
        code = "def invalid syntax here"
        result = parser.parse(code, 'python')
        assert result.success is False
        assert result.error_message is not None
        assert "Syntax error" in result.error_message
        assert result.line_number is not None


class TestJavaScriptParser:
    """Test JavaScript parser functionality."""
    
    def test_parse_valid_javascript_code(self):
        """Test parsing valid JavaScript code."""
        parser = LanguageParser()
        parser.register_parser('javascript', JavaScriptParser())
        
        code = """
function add(a, b) {
    return a + b;
}

const multiply = (x, y) => x * y;
"""
        result = parser.parse(code, 'javascript')
        assert result.success is True
        assert result.language == 'javascript'
        assert result.ast is not None
        assert result.error_message is None
    
    def test_parse_invalid_javascript_code(self):
        """Test parsing invalid JavaScript code returns error."""
        parser = LanguageParser()
        parser.register_parser('javascript', JavaScriptParser())
        
        code = "function invalid { syntax"
        result = parser.parse(code, 'javascript')
        assert result.success is False
        assert result.error_message is not None


class TestJavaParser:
    """Test Java parser functionality."""
    
    def test_parse_valid_java_code(self):
        """Test parsing valid Java code."""
        parser = LanguageParser()
        parser.register_parser('java', JavaParser())
        
        code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
"""
        result = parser.parse(code, 'java')
        assert result.success is True
        assert result.language == 'java'
        assert result.ast is not None
        assert result.error_message is None
    
    def test_parse_invalid_java_code(self):
        """Test parsing invalid Java code returns error."""
        parser = LanguageParser()
        parser.register_parser('java', JavaParser())
        
        code = "public class Invalid { syntax error"
        result = parser.parse(code, 'java')
        assert result.success is False
        assert result.error_message is not None


class TestParserRegistry:
    """Test parser registration and retrieval."""
    
    def test_register_and_use_parser(self):
        """Test registering a parser and using it."""
        parser = LanguageParser()
        python_parser = PythonParser()
        parser.register_parser('python', python_parser)
        
        assert 'python' in parser.get_supported_languages()
    
    def test_parse_without_registered_parser_raises_error(self):
        """Test parsing without registered parser raises error."""
        parser = LanguageParser()
        code = "print('hello')"
        
        with pytest.raises(ParserError) as exc_info:
            parser.parse(code, 'python')
        assert "No parser registered" in str(exc_info.value)
    
    def test_get_supported_languages(self):
        """Test getting list of supported languages."""
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        parser.register_parser('javascript', JavaScriptParser())
        
        languages = parser.get_supported_languages()
        assert 'python' in languages
        assert 'javascript' in languages
        assert len(languages) == 2
