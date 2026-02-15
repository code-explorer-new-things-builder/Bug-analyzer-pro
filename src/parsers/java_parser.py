"""Java parser using javalang."""

from typing import Dict, Any, List
from .language_parser import BaseParser, ParseResult, ParserError


class JavaParser(BaseParser):
    """Parser for Java code using javalang."""
    
    def __init__(self):
        """Initialize the Java parser."""
        try:
            import javalang
            self.javalang = javalang
        except ImportError:
            raise ParserError(
                "javalang library not installed. Install with: pip install javalang"
            )
    
    def get_language(self) -> str:
        """Return the language this parser handles."""
        return 'java'
    
    def parse(self, code: str) -> ParseResult:
        """Parse Java code into AST.
        
        Args:
            code: Java source code string
            
        Returns:
            ParseResult with AST and metadata
        """
        try:
            tree = self.javalang.parse.parse(code)
            structure = self._extract_structure(tree)
            
            return ParseResult(
                language='java',
                ast=tree,
                code=code,
                success=True,
                error_message=None,
                line_number=None
            )
        except self.javalang.parser.JavaSyntaxError as e:
            # Extract line number safely from the error
            line_num = None
            if hasattr(e, 'at') and e.at:
                if hasattr(e.at, 'position') and e.at.position:
                    line_num = e.at.position[0] if isinstance(e.at.position, tuple) else None
            
            return ParseResult(
                language='java',
                ast=None,
                code=code,
                success=False,
                error_message=f"Syntax error: {str(e)}",
                line_number=line_num
            )
        except Exception as e:
            return ParseResult(
                language='java',
                ast=None,
                code=code,
                success=False,
                error_message=f"Parse error: {str(e)}",
                line_number=None
            )
    
    def _extract_structure(self, tree: Any) -> Dict[str, Any]:
        """Extract code structure information from AST.
        
        Args:
            tree: Java AST from javalang
            
        Returns:
            Dictionary containing structure information
        """
        structure = {
            'classes': [],
            'methods': [],
            'imports': [],
            'fields': [],
            'package': None
        }
        
        # Extract package declaration
        if hasattr(tree, 'package') and tree.package:
            structure['package'] = tree.package.name
        
        # Extract imports
        if hasattr(tree, 'imports'):
            for imp in tree.imports:
                structure['imports'].append({
                    'path': imp.path,
                    'static': imp.static,
                    'wildcard': imp.wildcard
                })
        
        # Extract classes and their members
        if hasattr(tree, 'types'):
            for type_decl in tree.types:
                self._extract_type_info(type_decl, structure)
        
        return structure
    
    def _extract_type_info(self, type_decl: Any, structure: Dict[str, Any]) -> None:
        """Extract information from a type declaration (class, interface, enum).
        
        Args:
            type_decl: Type declaration node
            structure: Structure dictionary to populate
        """
        if not hasattr(type_decl, 'name'):
            return
        
        class_info = {
            'name': type_decl.name,
            'type': type(type_decl).__name__,
            'methods': [],
            'fields': [],
            'modifiers': list(type_decl.modifiers) if hasattr(type_decl, 'modifiers') else []
        }
        
        # Extract extends/implements
        if hasattr(type_decl, 'extends') and type_decl.extends:
            class_info['extends'] = type_decl.extends.name if hasattr(type_decl.extends, 'name') else str(type_decl.extends)
        
        if hasattr(type_decl, 'implements') and type_decl.implements:
            class_info['implements'] = [
                impl.name if hasattr(impl, 'name') else str(impl) 
                for impl in type_decl.implements
            ]
        
        # Extract methods and fields
        if hasattr(type_decl, 'body'):
            for member in type_decl.body:
                member_type = type(member).__name__
                
                if member_type == 'MethodDeclaration':
                    method_info = {
                        'name': member.name,
                        'return_type': self._get_type_name(member.return_type) if hasattr(member, 'return_type') else 'void',
                        'parameters': self._extract_parameters(member),
                        'modifiers': list(member.modifiers) if hasattr(member, 'modifiers') else []
                    }
                    class_info['methods'].append(method_info)
                    structure['methods'].append(method_info)
                
                elif member_type == 'FieldDeclaration':
                    for declarator in member.declarators:
                        field_info = {
                            'name': declarator.name,
                            'type': self._get_type_name(member.type) if hasattr(member, 'type') else 'unknown',
                            'modifiers': list(member.modifiers) if hasattr(member, 'modifiers') else []
                        }
                        class_info['fields'].append(field_info)
                        structure['fields'].append(field_info)
                
                elif member_type == 'ConstructorDeclaration':
                    constructor_info = {
                        'name': member.name,
                        'return_type': 'constructor',
                        'parameters': self._extract_parameters(member),
                        'modifiers': list(member.modifiers) if hasattr(member, 'modifiers') else []
                    }
                    class_info['methods'].append(constructor_info)
        
        structure['classes'].append(class_info)
    
    def _extract_parameters(self, method: Any) -> List[Dict[str, str]]:
        """Extract parameter information from a method.
        
        Args:
            method: Method declaration node
            
        Returns:
            List of parameter dictionaries
        """
        params = []
        if hasattr(method, 'parameters') and method.parameters:
            for param in method.parameters:
                params.append({
                    'name': param.name,
                    'type': self._get_type_name(param.type) if hasattr(param, 'type') else 'unknown'
                })
        return params
    
    def _get_type_name(self, type_node: Any) -> str:
        """Extract type name from a type node.
        
        Args:
            type_node: Type node from AST
            
        Returns:
            String representation of the type
        """
        if type_node is None:
            return 'void'
        
        if hasattr(type_node, 'name'):
            return type_node.name
        
        if hasattr(type_node, 'dimensions') and type_node.dimensions:
            base_type = self._get_type_name(getattr(type_node, 'sub_type', None))
            return f"{base_type}{'[]' * len(type_node.dimensions)}"
        
        return str(type_node)
