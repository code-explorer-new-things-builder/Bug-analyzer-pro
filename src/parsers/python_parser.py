"""Python parser using the ast module."""

import ast
from typing import Dict, Any
from .language_parser import BaseParser, ParseResult, ParserError


class PythonParser(BaseParser):
    """Parser for Python code using the built-in ast module."""
    
    def get_language(self) -> str:
        """Return the language this parser handles."""
        return 'python'
    
    def parse(self, code: str) -> ParseResult:
        """Parse Python code into AST.
        
        Args:
            code: Python source code string
            
        Returns:
            ParseResult with AST and metadata
        """
        try:
            tree = ast.parse(code)
            structure = self._extract_structure(tree)
            
            return ParseResult(
                language='python',
                ast=tree,
                code=code,
                success=True,
                error_message=None,
                line_number=None
            )
        except SyntaxError as e:
            return ParseResult(
                language='python',
                ast=None,
                code=code,
                success=False,
                error_message=f"Syntax error: {e.msg}",
                line_number=e.lineno
            )
        except Exception as e:
            return ParseResult(
                language='python',
                ast=None,
                code=code,
                success=False,
                error_message=f"Parse error: {str(e)}",
                line_number=None
            )
    
    def _extract_structure(self, tree: ast.AST) -> Dict[str, Any]:
        """Extract code structure information from AST.
        
        Args:
            tree: Python AST
            
        Returns:
            Dictionary containing structure information
        """
        structure = {
            'functions': [],
            'classes': [],
            'imports': [],
            'variables': []
        }
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                structure['functions'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
                })
            elif isinstance(node, ast.ClassDef):
                structure['classes'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'bases': [self._get_name(base) for base in node.bases],
                    'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure['imports'].append({
                            'module': alias.name,
                            'alias': alias.asname,
                            'line': node.lineno
                        })
                else:
                    module = node.module or ''
                    for alias in node.names:
                        structure['imports'].append({
                            'module': f"{module}.{alias.name}" if module else alias.name,
                            'alias': alias.asname,
                            'line': node.lineno
                        })
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        structure['variables'].append({
                            'name': target.id,
                            'line': node.lineno
                        })
        
        return structure
    
    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Extract decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self._get_name(decorator.func)
        return 'unknown'
    
    def _get_name(self, node: ast.expr) -> str:
        """Extract name from various AST node types."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return 'unknown'
