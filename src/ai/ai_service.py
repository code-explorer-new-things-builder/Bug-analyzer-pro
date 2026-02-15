"""AI service for enhanced code analysis using Google Gemini."""

import os
from typing import List, Optional
from src.models import Finding
from src.utils import get_logger


class AIService:
    """AI service for enhancing code analysis with Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI service.
        
        Args:
            api_key: Gemini API key (or use GEMINI_API_KEY env var)
        """
        self.logger = get_logger(__name__)
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                self.logger.info("Gemini AI service initialized successfully")
            except ImportError:
                self.logger.warning("google-generativeai not installed. Install with: pip install google-generativeai")
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini: {e}")
        else:
            self.logger.warning("No Gemini API key provided. AI features disabled.")
    
    def is_available(self) -> bool:
        """Check if AI service is available."""
        return self.model is not None
    
    def enhance_finding(self, finding: Finding, code: str, language: str) -> Finding:
        """Enhance a finding with AI-generated explanation.
        
        Args:
            finding: The finding to enhance
            code: The source code
            language: Programming language
            
        Returns:
            Enhanced finding with AI explanation
        """
        if not self.is_available():
            return finding
        
        try:
            prompt = self._create_enhancement_prompt(finding, code, language)
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Parse AI response
                finding.explanation = self._extract_explanation(response.text)
                finding.examples = self._extract_examples(response.text)
                finding.best_practices = self._extract_best_practices(response.text)
                
                self.logger.info(f"Enhanced finding {finding.id} with AI")
        except Exception as e:
            self.logger.error(f"AI enhancement failed: {e}")
        
        return finding
    
    def analyze_code_context(self, code: str, language: str) -> str:
        """Analyze code context using AI.
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            AI analysis of the code
        """
        if not self.is_available():
            return "AI analysis not available"
        
        try:
            prompt = f"""Analyze this {language} code for potential issues, bugs, and improvements:

```{language}
{code}
```

Provide:
1. Overall code quality assessment
2. Potential bugs or issues
3. Security concerns
4. Best practice recommendations
5. Suggested improvements

Keep the response concise and actionable."""

            response = self.model.generate_content(prompt)
            return response.text if response else "No analysis available"
        except Exception as e:
            self.logger.error(f"AI analysis failed: {e}")
            return f"Analysis failed: {str(e)}"
    
    def generate_fix_suggestion(self, finding: Finding, code: str, language: str) -> str:
        """Generate specific fix suggestion using AI.
        
        Args:
            finding: The finding to fix
            code: Source code
            language: Programming language
            
        Returns:
            AI-generated fix suggestion
        """
        if not self.is_available():
            return finding.suggestion or "No suggestion available"
        
        try:
            prompt = f"""Given this {language} code issue:

Issue: {finding.message}
Location: Line {finding.line_number}
Code snippet:
```{language}
{finding.code_snippet}
```

Provide a specific, actionable fix with:
1. Exact code changes needed
2. Why this fix works
3. Alternative approaches (if any)

Keep it concise and practical."""

            response = self.model.generate_content(prompt)
            return response.text if response else finding.suggestion or "No suggestion available"
        except Exception as e:
            self.logger.error(f"Fix generation failed: {e}")
            return finding.suggestion or "No suggestion available"
    
    def _create_enhancement_prompt(self, finding: Finding, code: str, language: str) -> str:
        """Create prompt for enhancing a finding."""
        return f"""You are a code review expert. Explain this code issue to a developer:

Language: {language}
Issue Type: {finding.type.value}
Severity: {finding.severity.value}
Message: {finding.message}
Line: {finding.line_number}

Code context:
```{language}
{finding.code_snippet}
```

Provide:
1. EXPLANATION: Why is this a problem? What could go wrong?
2. EXAMPLE: Show a before/after code example
3. BEST_PRACTICES: What's the recommended approach?

Format your response with clear sections: EXPLANATION:, EXAMPLE:, BEST_PRACTICES:"""
    
    def _extract_explanation(self, ai_response: str) -> str:
        """Extract explanation from AI response."""
        if "EXPLANATION:" in ai_response:
            parts = ai_response.split("EXPLANATION:")[1].split("EXAMPLE:")[0]
            return parts.strip()
        return ai_response[:500]  # First 500 chars as fallback
    
    def _extract_examples(self, ai_response: str) -> List[str]:
        """Extract code examples from AI response."""
        examples = []
        if "EXAMPLE:" in ai_response:
            example_text = ai_response.split("EXAMPLE:")[1].split("BEST_PRACTICES:")[0]
            examples.append(example_text.strip())
        return examples
    
    def _extract_best_practices(self, ai_response: str) -> List[str]:
        """Extract best practices from AI response."""
        practices = []
        if "BEST_PRACTICES:" in ai_response:
            practices_text = ai_response.split("BEST_PRACTICES:")[1]
            # Split by newlines and filter
            practices = [p.strip() for p in practices_text.split('\n') if p.strip() and len(p.strip()) > 10]
        return practices[:3]  # Top 3 practices
