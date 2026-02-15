"""Finding data model for code analysis results."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class FindingType(Enum):
    """Type of finding."""
    BUG = "bug"
    SECURITY = "security"
    STYLE = "style"


class SeverityLevel(Enum):
    """Severity level of a finding."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Finding:
    """Represents a single code analysis finding."""
    
    id: str
    type: FindingType
    severity: SeverityLevel
    line_number: int
    column_number: int
    message: str
    code_snippet: str
    suggestion: Optional[str] = None
    explanation: Optional[str] = None
    examples: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    best_practices: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert finding to dictionary."""
        return {
            'id': self.id,
            'type': self.type.value,
            'severity': self.severity.value,
            'line_number': self.line_number,
            'column_number': self.column_number,
            'message': self.message,
            'code_snippet': self.code_snippet,
            'suggestion': self.suggestion,
            'explanation': self.explanation,
            'examples': self.examples,
            'resources': self.resources,
            'best_practices': self.best_practices
        }
