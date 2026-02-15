"""Unit tests for core data models."""

import pytest
from src.models import (
    Finding, FindingType, SeverityLevel,
    AnalysisResult, QualityMetrics,
    AnalysisConfig
)


class TestFinding:
    """Test Finding data model."""
    
    def test_create_finding(self):
        """Test creating a finding."""
        finding = Finding(
            id="F001",
            type=FindingType.BUG,
            severity=SeverityLevel.HIGH,
            line_number=42,
            column_number=10,
            message="Potential null pointer",
            code_snippet="x = None\nprint(x.value)",
            suggestion="Check if x is not None before accessing"
        )
        
        assert finding.id == "F001"
        assert finding.type == FindingType.BUG
        assert finding.severity == SeverityLevel.HIGH
        assert finding.line_number == 42
    
    def test_finding_to_dict(self):
        """Test converting finding to dictionary."""
        finding = Finding(
            id="F001",
            type=FindingType.SECURITY,
            severity=SeverityLevel.CRITICAL,
            line_number=10,
            column_number=5,
            message="SQL injection vulnerability",
            code_snippet="query = 'SELECT * FROM users WHERE id=' + user_id"
        )
        
        data = finding.to_dict()
        assert data['id'] == "F001"
        assert data['type'] == "security"
        assert data['severity'] == "critical"


class TestQualityMetrics:
    """Test QualityMetrics data model."""
    
    def test_create_metrics(self):
        """Test creating quality metrics."""
        metrics = QualityMetrics(
            total_issues=10,
            critical_issues=2,
            high_issues=3,
            medium_issues=3,
            low_issues=2,
            code_quality_score=75.5,
            maintainability_index=68.2
        )
        
        assert metrics.total_issues == 10
        assert metrics.critical_issues == 2
        assert metrics.code_quality_score == 75.5
    
    def test_metrics_to_dict(self):
        """Test converting metrics to dictionary."""
        metrics = QualityMetrics(total_issues=5)
        data = metrics.to_dict()
        assert data['total_issues'] == 5
        assert 'code_quality_score' in data


class TestAnalysisResult:
    """Test AnalysisResult data model."""
    
    def test_create_result(self):
        """Test creating analysis result."""
        result = AnalysisResult(
            file_path="test.py",
            language="python",
            success=True
        )
        
        assert result.file_path == "test.py"
        assert result.language == "python"
        assert result.success is True
        assert len(result.findings) == 0
    
    def test_result_with_findings(self):
        """Test result with findings."""
        finding = Finding(
            id="F001",
            type=FindingType.STYLE,
            severity=SeverityLevel.LOW,
            line_number=1,
            column_number=1,
            message="Missing docstring",
            code_snippet="def foo():"
        )
        
        result = AnalysisResult(
            file_path="test.py",
            language="python",
            findings=[finding]
        )
        
        assert len(result.findings) == 1
        assert result.findings[0].id == "F001"


class TestAnalysisConfig:
    """Test AnalysisConfig data model."""
    
    def test_create_default_config(self):
        """Test creating default configuration."""
        config = AnalysisConfig()
        
        assert 'bug' in config.enabled_checks
        assert 'security' in config.enabled_checks
        assert 'style' in config.enabled_checks
        assert config.severity_threshold == SeverityLevel.LOW
        assert config.use_ai is False
    
    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = AnalysisConfig(use_ai=True, ai_model="gpt-4")
        data = config.to_dict()
        
        assert data['use_ai'] is True
        assert data['ai_model'] == "gpt-4"
        assert 'enabled_checks' in data
    
    def test_config_from_dict(self):
        """Test creating config from dictionary."""
        data = {
            'use_ai': True,
            'ai_model': 'claude-3',
            'severity_threshold': 'high',
            'verbose': True
        }
        
        config = AnalysisConfig.from_dict(data)
        assert config.use_ai is True
        assert config.ai_model == 'claude-3'
        assert config.severity_threshold == SeverityLevel.HIGH
        assert config.verbose is True
