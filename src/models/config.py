"""Configuration data models."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from .finding import SeverityLevel


@dataclass
class AnalysisConfig:
    """Configuration for code analysis."""
    
    # Analysis options
    enabled_checks: List[str] = field(default_factory=lambda: ['bug', 'security', 'style'])
    severity_threshold: SeverityLevel = SeverityLevel.LOW
    
    # Language settings
    languages: List[str] = field(default_factory=lambda: ['python', 'javascript', 'java'])
    
    # Style guide
    style_guide: str = "default"
    
    # Custom rules
    custom_rules: Dict[str, Any] = field(default_factory=dict)
    
    # Educational settings
    educational_level: str = "intermediate"  # beginner, intermediate, advanced
    include_examples: bool = True
    include_resources: bool = True
    
    # AI settings
    use_ai: bool = False
    ai_provider: str = "openai"  # openai, claude, local
    ai_model: str = "gpt-4"
    
    # Performance settings
    max_file_size: int = 1000000  # 1MB
    parallel_processing: bool = True
    max_workers: int = 4
    
    # Output settings
    output_format: str = "json"  # json, markdown, html
    verbose: bool = False
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            'enabled_checks': self.enabled_checks,
            'severity_threshold': self.severity_threshold.value,
            'languages': self.languages,
            'style_guide': self.style_guide,
            'custom_rules': self.custom_rules,
            'educational_level': self.educational_level,
            'include_examples': self.include_examples,
            'include_resources': self.include_resources,
            'use_ai': self.use_ai,
            'ai_provider': self.ai_provider,
            'ai_model': self.ai_model,
            'max_file_size': self.max_file_size,
            'parallel_processing': self.parallel_processing,
            'max_workers': self.max_workers,
            'output_format': self.output_format,
            'verbose': self.verbose
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AnalysisConfig':
        """Create config from dictionary."""
        config = cls()
        for key, value in data.items():
            if key == 'severity_threshold':
                value = SeverityLevel(value)
            if hasattr(config, key):
                setattr(config, key, value)
        return config
