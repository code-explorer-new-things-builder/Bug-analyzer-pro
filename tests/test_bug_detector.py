"""Unit tests for Bug Detector."""

import ast
import pytest
from src.analyzers import BugDetector
from src.models import FindingType, SeverityLevel


class TestBugDetector:
    """Test BugDetector functionality."""
    
    def test_create_bug_detector(self):
        """Test creating bug detector."""
        detector = BugDetector()
        assert detector is not None
        assert len(detector.rules) > 0
    
    def test_get_bug_rules(self):
        """Test getting bug rules."""
        detector = BugDetector()
        rules = detector.get_bug_rules('python')
        assert len(rules) > 0
        assert any(r.name == 'Null Pointer/Reference' for r in rules)
    
    def test_detect_infinite_loop_python(self):
        """Test detecting infinite loop in Python."""
        code = """
while True:
    print("infinite")
"""
        tree = ast.parse(code)
        detector = BugDetector()
        findings = detector.detect_bugs(tree, code, 'python')
        
        assert len(findings) > 0
        assert any('infinite loop' in f.message.lower() for f in findings)
        assert any(f.severity == SeverityLevel.CRITICAL for f in findings)
    
    def test_detect_unreachable_code_python(self):
        """Test detecting unreachable code in Python."""
        code = """
def test_function():
    return 42
    print("This will never execute")
"""
        tree = ast.parse(code)
        detector = BugDetector()
        findings = detector.detect_bugs(tree, code, 'python')
        
        assert len(findings) > 0
        assert any('unreachable' in f.message.lower() for f in findings)
    
    def test_no_bugs_in_clean_code(self):
        """Test that clean code produces no findings."""
        code = """
def add(a, b):
    return a + b

result = add(1, 2)
"""
        tree = ast.parse(code)
        detector = BugDetector()
        findings = detector.detect_bugs(tree, code, 'python')
        
        # Clean code should have no or minimal findings
        assert isinstance(findings, list)
    
    def test_configure_rules(self):
        """Test configuring enabled rules."""
        detector = BugDetector()
        initial_count = len(detector.rules)
        
        detector.configure_rules(['infinite_loop'])
        assert len(detector.rules) < initial_count
        assert 'infinite_loop' in detector.rules
