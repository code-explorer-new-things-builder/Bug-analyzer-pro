"""JavaScript parser using esprima."""

from typing import Dict, Any, Optional
from .language_parser import BaseParser, ParseResult, ParserError


class JavaScriptParser(BaseParser):
    """Parser for JavaScript code using esprima."""
    
    def __init__(self):
        """Initialize the JavaScript parser."""
        try:
            import esprima
            self.esprima = esprima
        except ImportError:
            raise ParserError(
                "esprima library not installed. Install with: pip install esprima"
            )
    
    def get_language(self) -> str:
        """Return the language this parser handles."""
        return 'javascript'
    
    def parse(self, code: str) -> ParseResult:
        """Parse JavaScript code into AST.
        
        Args:
            code: JavaScript source code string
            
        Returns:
            ParseResult with AST and metadata
        """
        try:
            # Parse with ES6+ support
            tree = self.esprima.parseScript(code, {
                'loc': True,
                'range': True,
                'tolerant': True
            })
            
            structure = self._extract_structure(tree)
            
            return ParseResult(
                language='javascript',
                ast=tree,
                code=code,
                success=True,
                error_message=None,
                line_number=None
            )
        except self.esprima.Error as e:
            return ParseResult(
                language='javascript',
                ast=None,
                code=code,
                success=False,
                error_message=f"Syntax error: {str(e)}",
                line_number=getattr(e, 'lineNumber', None)
            )
        except Exception as e:
            return ParseResult(
                language='javascript',
                ast=None,
                code=code,
                success=False,
                error_message=f"Parse error: {str(e)}",
                line_number=None
            )
    
    def _extract_structure(self, tree: Any) -> Dict[str, Any]:
        """Extract code structure information from AST.
        
        Args:
            tree: JavaScript AST from esprima
            
        Returns:
            Dictionary containing structure information
        """
        structure = {
            'functions': [],
            'classes': [],
            'imports': [],
            'variables': []
        }
        
        self._walk_ast(tree, structure)
        return structure
    
    def _walk_ast(self, node: Any, structure: Dict[str, Any]) -> None:
        """Walk the AST and extract structure information.
        
        Args:
            node: Current AST node
            structure: Structure dictionary to populate
        """
        if not hasattr(node, 'type'):
            return
        
        node_type = node.type
        
        # Extract functions
        if node_type == 'FunctionDeclaration':
            structure['functions'].append({
                'name': node.id.name if hasattr(node, 'id') and node.id else 'anonymous',
                'line': node.loc.start.line if hasattr(node, 'loc') else None,
                'params': [p.name for p in node.params if hasattr(p, 'name')],
                'async': getattr(node, 'async', False)
            })
        
        # Extract arrow functions and function expressions
        elif node_type in ('ArrowFunctionExpression', 'FunctionExpression'):
            structure['functions'].append({
                'name': 'anonymous',
                'line': node.loc.start.line if hasattr(node, 'loc') else None,
                'params': [p.name for p in node.params if hasattr(p, 'name')],
                'async': getattr(node, 'async', False)
            })
        
        # Extract classes
        elif node_type == 'ClassDeclaration':
            methods = []
            if hasattr(node, 'body') and hasattr(node.body, 'body'):
                for item in node.body.body:
                    if item.type == 'MethodDefinition' and hasattr(item, 'key'):
                        methods.append(item.key.name if hasattr(item.key, 'name') else 'unknown')
            
            structure['classes'].append({
                'name': node.id.name if hasattr(node, 'id') and node.id else 'anonymous',
                'line': node.loc.start.line if hasattr(node, 'loc') else None,
                'methods': methods,
                'superClass': node.superClass.name if hasattr(node, 'superClass') and node.superClass and hasattr(node.superClass, 'name') else None
            })
        
        # Extract imports
        elif node_type == 'ImportDeclaration':
            if hasattr(node, 'source') and hasattr(node.source, 'value'):
                structure['imports'].append({
                    'module': node.source.value,
                    'line': node.loc.start.line if hasattr(node, 'loc') else None,
                    'specifiers': [s.local.name for s in node.specifiers if hasattr(s, 'local') and hasattr(s.local, 'name')]
                })
        
        # Extract variable declarations
        elif node_type == 'VariableDeclaration':
            for declarator in node.declarations:
                if hasattr(declarator, 'id') and hasattr(declarator.id, 'name'):
                    structure['variables'].append({
                        'name': declarator.id.name,
                        'line': node.loc.start.line if hasattr(node, 'loc') else None,
                        'kind': node.kind  # const, let, var
                    })
        
        # Recursively walk child nodes
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    self._walk_ast(item, structure)
            elif hasattr(value, 'type'):
                self._walk_ast(value, structure)
