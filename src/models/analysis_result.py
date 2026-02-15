"""Analysis result data models."""

from dataclasses import dataclass, field
from typing import List
from .finding import Finding


@dataclass
class QualityMetrics:
    """Code quality metrics."""
    
    total_issues: int = 0
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0
    code_quality_score: float = 0.0
    maintainability_index: float = 0.0
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary."""
        return {
            'total_issues': self.total_issues,
            'critical_issues': self.critical_issues,
            'high_issues': self.high_issues,
            'medium_issues': self.medium_issues,
            'low_issues': self.low_issues,
            'code_quality_score': self.code_quality_score,
            'maintainability_index': self.maintainability_index
        }


@dataclass
class AnalysisResult:
    """Result of code analysis."""
    
    file_path: str
    language: str
    findings: List[Finding] = field(default_factory=list)
    metrics: QualityMetrics = field(default_factory=QualityMetrics)
    analysis_time: float = 0.0
    success: bool = True
    error_message: str = ""
    
    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        return {
            'file_path': self.file_path,
            'language': self.language,
            'findings': [f.to_dict() for f in self.findings],
            'metrics': self.metrics.to_dict(),
            'analysis_time': self.analysis_time,
            'success': self.success,
            'error_message': self.error_message
        }
