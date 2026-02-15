"""Integration tests for parsing and bug detection."""

import pytest
from src.parsers import LanguageParser, PythonParser, JavaScriptParser
from src.analyzers import BugDetector
from src.models import FindingType, SeverityLevel


class TestParsingAndBugDetection:
    """Test integration between parser and bug detector."""
    
    def test_python_parsing_and_bug_detection(self):
        """Test complete flow: parse Python code and detect bugs."""
        # Code with an infinite loop bug
        code = """
def process_data():
    while True:
        print("Processing...")
    return "Done"
"""
        
        # Step 1: Parse the code
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        
        parse_result = parser.parse(code, 'python')
        assert parse_result.success is True
        assert parse_result.ast is not None
        
        # Step 2: Detect bugs
        detector = BugDetector()
        findings = detector.detect_bugs(parse_result.ast, code, 'python')
        
        # Step 3: Verify findings
        assert len(findings) > 0
        assert any(f.type == FindingType.BUG for f in findings)
        assert any('infinite' in f.message.lower() for f in findings)
    
    def test_python_unreachable_code_detection(self):
        """Test detecting unreachable code in Python."""
        code = """
def calculate(x):
    if x > 0:
        return x * 2
        print("This is unreachable")
    return 0
"""
        
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        parse_result = parser.parse(code, 'python')
        
        detector = BugDetector()
        findings = detector.detect_bugs(parse_result.ast, code, 'python')
        
        assert len(findings) > 0
        assert any('unreachable' in f.message.lower() for f in findings)
    
    def test_javascript_parsing_and_bug_detection(self):
        """Test complete flow: parse JavaScript code and detect bugs."""
        code = """
function processData() {
    while(true) {
        console.log("Processing...");
    }
    return "Done";
}
"""
        
        parser = LanguageParser()
        parser.register_parser('javascript', JavaScriptParser())
        
        parse_result = parser.parse(code, 'javascript')
        assert parse_result.success is True
        
        detector = BugDetector()
        findings = detector.detect_bugs(parse_result.ast, code, 'javascript')
        
        # Should detect infinite loop
        assert len(findings) > 0
        assert any('infinite' in f.message.lower() for f in findings)
    
    def test_clean_code_produces_minimal_findings(self):
        """Test that clean code produces no or minimal findings."""
        code = """
def add_numbers(a, b):
    '''Add two numbers and return the result.'''
    if a is None or b is None:
        return 0
    return a + b

result = add_numbers(5, 3)
print(result)
"""
        
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        parse_result = parser.parse(code, 'python')
        
        detector = BugDetector()
        findings = detector.detect_bugs(parse_result.ast, code, 'python')
        
        # Clean code should have no critical bugs
        critical_bugs = [f for f in findings if f.severity == SeverityLevel.CRITICAL]
        assert len(critical_bugs) == 0
    
    def test_syntax_error_handling(self):
        """Test handling of syntax errors in parsing."""
        code = "def invalid syntax here"
        
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        parse_result = parser.parse(code, 'python')
        
        # Should fail gracefully
        assert parse_result.success is False
        assert parse_result.error_message is not None
        assert 'syntax' in parse_result.error_message.lower()
    
    def test_multiple_bugs_detection(self):
        """Test detecting multiple bugs in one file."""
        code = """
def problematic_function():
    while True:
        x = 10
    return x
    print("Unreachable")
"""
        
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        parse_result = parser.parse(code, 'python')
        
        detector = BugDetector()
        findings = detector.detect_bugs(parse_result.ast, code, 'python')
        
        # Should detect both infinite loop and unreachable code
        assert len(findings) >= 2
        bug_types = [f.message.lower() for f in findings]
        assert any('infinite' in msg for msg in bug_types)
        assert any('unreachable' in msg for msg in bug_types)
    
    def test_language_detection_and_analysis(self):
        """Test automatic language detection followed by analysis."""
        code = """
def test():
    while True:
        pass
"""
        
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        
        # Detect language
        language = parser.detect_language(code, "test.py")
        assert language == "python"
        
        # Parse
        parse_result = parser.parse(code, language)
        assert parse_result.success is True
        
        # Analyze
        detector = BugDetector()
        findings = detector.detect_bugs(parse_result.ast, code, language)
        assert len(findings) > 0


class TestEndToEndWorkflow:
    """Test complete end-to-end workflow."""
    
    def test_complete_analysis_workflow(self):
        """Test the complete analysis workflow from code to findings."""
        # Sample code with bugs
        test_code = """
def divide(a, b):
    return a / b  # No zero check

def loop_forever():
    while True:
        print("Running")
    return "Done"  # Unreachable
"""
        
        # Initialize components
        parser = LanguageParser()
        parser.register_parser('python', PythonParser())
        detector = BugDetector()
        
        # Step 1: Detect language
        language = parser.detect_language(test_code, "test.py")
        assert language == "python"
        
        # Step 2: Parse code
        parse_result = parser.parse(test_code, language)
        assert parse_result.success is True
        
        # Step 3: Detect bugs
        findings = detector.detect_bugs(parse_result.ast, test_code, language)
        
        # Step 4: Verify results
        assert len(findings) > 0
        
        # Check finding structure
        for finding in findings:
            assert finding.id is not None
            assert finding.type == FindingType.BUG
            assert finding.severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH, 
                                       SeverityLevel.MEDIUM, SeverityLevel.LOW]
            assert finding.line_number > 0
            assert finding.message != ""
            assert finding.code_snippet != ""
        
        print(f"\n✓ Analysis complete: Found {len(findings)} issues")
        for f in findings:
            print(f"  - Line {f.line_number}: {f.message} [{f.severity.value}]")
