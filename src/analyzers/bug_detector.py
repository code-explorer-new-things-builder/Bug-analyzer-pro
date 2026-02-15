"""Bug detector for identifying potential bugs in code."""

import ast
from typing import List, Any, Dict
from src.models import Finding, FindingType, SeverityLevel
from src.utils import get_logger


class BugRule:
    """Represents a bug detection rule."""
    
    def __init__(self, rule_id: str, name: str, severity: SeverityLevel, description: str):
        self.rule_id = rule_id
        self.name = name
        self.severity = severity
        self.description = description


class BugDetector:
    """Detects potential bugs in code using AST analysis."""
    
    def __init__(self):
        """Initialize bug detector with rules."""
        self.logger = get_logger(__name__)
        self.rules = self._load_rules()
        self.findings: List[Finding] = []
    
    def _load_rules(self) -> Dict[str, BugRule]:
        """Load bug detection rules."""
        return {
            'null_pointer': BugRule(
                'B001',
                'Null Pointer/Reference',
                SeverityLevel.HIGH,
                'Variable may be None/null when accessed'
            ),
            'infinite_loop': BugRule(
                'B002',
                'Infinite Loop',
                SeverityLevel.CRITICAL,
                'Loop may run infinitely'
            ),
            'unreachable_code': BugRule(
                'B003',
                'Unreachable Code',
                SeverityLevel.MEDIUM,
                'Code will never be executed'
            ),
            'logic_error': BugRule(
                'B004',
                'Logic Error',
                SeverityLevel.HIGH,
                'Potential logical error in code'
            )
        }
    
    def detect_bugs(self, tree: Any, code: str, language: str) -> List[Finding]:
        """Detect bugs in parsed code.
        
        Args:
            tree: AST of the code
            code: Original source code
            language: Programming language
            
        Returns:
            List of bug findings
        """
        self.findings = []
        self.code_lines = code.split('\n')
        
        if language == 'python':
            self._analyze_python(tree)
        elif language == 'javascript':
            self._analyze_javascript(tree)
        elif language == 'java':
            self._analyze_java(tree)
        
        self.logger.info(f"Found {len(self.findings)} potential bugs")
        return self.findings
    
    def _analyze_python(self, tree: ast.AST) -> None:
        """Analyze Python AST for bugs."""
        for node in ast.walk(tree):
            self._check_null_pointer_python(node)
            self._check_infinite_loop_python(node)
            self._check_unreachable_code_python(node)
            self._check_logic_errors_python(node)
    
    def _analyze_javascript(self, tree: Any) -> None:
        """Analyze JavaScript AST for bugs."""
        self._walk_js_ast(tree)
    
    def _analyze_java(self, tree: Any) -> None:
        """Analyze Java AST for bugs."""
        self._walk_java_ast(tree)
    
    def _walk_js_ast(self, node: Any) -> None:
        """Walk JavaScript AST recursively."""
        if not hasattr(node, 'type'):
            return
        
        self._check_null_pointer_js(node)
        self._check_infinite_loop_js(node)
        self._check_unreachable_code_js(node)
        
        # Recursively walk child nodes
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    self._walk_js_ast(item)
            elif hasattr(value, 'type'):
                self._walk_js_ast(value)
    
    def _walk_java_ast(self, tree: Any) -> None:
        """Walk Java AST recursively."""
        if tree is None:
            return
        
        # Check for bugs in current node
        self._check_infinite_loop_java(tree)
        self._check_unreachable_code_java(tree)
        self._check_null_pointer_java(tree)
        self._check_logic_errors_java(tree)
        
        # Recursively walk child nodes
        if hasattr(tree, 'types'):
            for type_decl in tree.types:
                self._walk_java_type(type_decl)
    
    def _walk_java_type(self, type_decl: Any) -> None:
        """Walk Java type declaration (class, interface, etc)."""
        if not hasattr(type_decl, 'body'):
            return
        
        for member in type_decl.body:
            member_type = type(member).__name__
            
            if member_type == 'MethodDeclaration' or member_type == 'ConstructorDeclaration':
                self._check_method_for_bugs(member)
            elif member_type == 'FieldDeclaration':
                self._check_field_for_bugs(member)
    
    def _check_method_for_bugs(self, method: Any) -> None:
        """Check a Java method for bugs."""
        if not hasattr(method, 'body') or method.body is None:
            return
        
        # Get method line number
        line = method.position[0] if hasattr(method, 'position') and method.position else 0
        
        # Check for infinite loops
        self._check_java_infinite_loops(method.body, line)
        
        # Check for unreachable code
        self._check_java_unreachable_code(method.body, line)
        
        # Check for null pointer issues
        self._check_java_null_pointers(method.body, line)
    
    def _check_field_for_bugs(self, field: Any) -> None:
        """Check a Java field for bugs."""
        line = field.position[0] if hasattr(field, 'position') and field.position else 0
        
        # Check for hardcoded credentials
        if hasattr(field, 'declarators'):
            for declarator in field.declarators:
                if hasattr(declarator, 'initializer') and declarator.initializer:
                    self._check_hardcoded_credentials(declarator, line)
    
    def _check_java_infinite_loops(self, body: Any, method_line: int) -> None:
        """Check for infinite loops in Java method body."""
        if not hasattr(body, 'statements'):
            return
        
        for stmt in body.statements:
            stmt_type = type(stmt).__name__
            
            if stmt_type == 'WhileStatement':
                line = stmt.position[0] if hasattr(stmt, 'position') and stmt.position else method_line
                
                # Check for while(true)
                if hasattr(stmt, 'condition'):
                    condition_str = str(stmt.condition)
                    if 'true' in condition_str.lower():
                        # Check if there's a break statement
                        if not self._has_java_break(stmt):
                            self._add_finding(
                                'infinite_loop',
                                line,
                                0,
                                "Infinite loop detected: while(true) without break statement",
                                self._get_code_snippet(line),
                                "Add a break condition or use a conditional while loop"
                            )
            
            elif stmt_type == 'ForStatement':
                line = stmt.position[0] if hasattr(stmt, 'position') and stmt.position else method_line
                # Check for for loops with problematic conditions
                if hasattr(stmt, 'update') and stmt.update is None:
                    self._add_finding(
                        'infinite_loop',
                        line,
                        0,
                        "Potential infinite loop: for loop without update expression",
                        self._get_code_snippet(line),
                        "Add an update expression to the for loop"
                    )
    
    def _check_java_unreachable_code(self, body: Any, method_line: int) -> None:
        """Check for unreachable code in Java method body."""
        if not hasattr(body, 'statements'):
            return
        
        statements = body.statements
        for i, stmt in enumerate(statements):
            stmt_type = type(stmt).__name__
            
            if stmt_type == 'ReturnStatement':
                # Check if there's code after return
                if i < len(statements) - 1:
                    next_stmt = statements[i + 1]
                    line = next_stmt.position[0] if hasattr(next_stmt, 'position') and next_stmt.position else method_line
                    self._add_finding(
                        'unreachable_code',
                        line,
                        0,
                        "Unreachable code after return statement",
                        self._get_code_snippet(line),
                        "Remove unreachable code or restructure logic"
                    )
                    break
    
    def _check_java_null_pointers(self, body: Any, method_line: int) -> None:
        """Check for null pointer issues in Java method body."""
        if not hasattr(body, 'statements'):
            return
        
        for stmt in body.statements:
            stmt_type = type(stmt).__name__
            
            # Check for method calls on potentially null objects
            if stmt_type == 'StatementExpression':
                if hasattr(stmt, 'expression'):
                    expr_str = str(stmt.expression)
                    # Simple heuristic: check for .get() calls without null check
                    if '.get(' in expr_str and 'null' not in expr_str.lower():
                        line = stmt.position[0] if hasattr(stmt, 'position') and stmt.position else method_line
                        self._add_finding(
                            'null_pointer',
                            line,
                            0,
                            "Potential null pointer: method call without null check",
                            self._get_code_snippet(line),
                            "Add null check before calling methods"
                        )
    
    def _check_logic_errors_java(self, tree: Any) -> None:
        """Check for logic errors in Java code."""
        # Check for string comparison using == instead of .equals()
        code_str = '\n'.join(self.code_lines)
        
        # Look for patterns like: if (string == "value")
        import re
        pattern = r'if\s*\(\s*\w+\s*==\s*["\']'
        matches = re.finditer(pattern, code_str)
        
        for match in matches:
            # Find line number
            line_num = code_str[:match.start()].count('\n') + 1
            self._add_finding(
                'logic_error',
                line_num,
                0,
                "Logic error: String comparison using == instead of .equals()",
                self._get_code_snippet(line_num),
                "Use .equals() method for string comparison: if (string.equals(\"value\"))"
            )
    
    def _check_hardcoded_credentials(self, declarator: Any, line: int) -> None:
        """Check for hardcoded credentials in Java code."""
        var_name = declarator.name if hasattr(declarator, 'name') else ''
        
        # Check if variable name suggests credentials
        if any(keyword in var_name.lower() for keyword in ['password', 'secret', 'key', 'token', 'apikey']):
            self._add_finding(
                'logic_error',
                line,
                0,
                f"Security issue: Hardcoded credential in variable '{var_name}'",
                self._get_code_snippet(line),
                "Move credentials to environment variables or configuration files"
            )
    
    def _has_java_break(self, node: Any) -> bool:
        """Check if a Java node contains a break statement."""
        if node is None:
            return False
        
        node_type = type(node).__name__
        
        if node_type == 'BreakStatement':
            return True
        
        # Check in body
        if hasattr(node, 'body'):
            if hasattr(node.body, 'statements'):
                for stmt in node.body.statements:
                    if self._has_java_break(stmt):
                        return True
        
        return False
    
    def _check_null_pointer_python(self, node: ast.AST) -> None:
        """Check for potential null pointer issues in Python."""
        # Check for attribute access on potentially None values
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                # Simple heuristic: check if variable name suggests it could be None
                var_name = node.value.id
                if 'none' in var_name.lower() or var_name.startswith('maybe_'):
                    self._add_finding(
                        'null_pointer',
                        node.lineno if hasattr(node, 'lineno') else 0,
                        node.col_offset if hasattr(node, 'col_offset') else 0,
                        f"Potential None access on variable '{var_name}'",
                        self._get_code_snippet(node.lineno if hasattr(node, 'lineno') else 0),
                        f"Add None check: if {var_name} is not None:"
                    )
    
    def _check_infinite_loop_python(self, node: ast.AST) -> None:
        """Check for infinite loops in Python."""
        if isinstance(node, ast.While):
            # Check for while True without break
            if isinstance(node.test, ast.Constant) and node.test.value is True:
                has_break = self._has_break_statement(node)
                if not has_break:
                    self._add_finding(
                        'infinite_loop',
                        node.lineno,
                        node.col_offset,
                        "Infinite loop detected: while True without break statement",
                        self._get_code_snippet(node.lineno),
                        "Add a break condition or use a conditional while loop"
                    )
    
    def _check_unreachable_code_python(self, node: ast.AST) -> None:
        """Check for unreachable code in Python."""
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for i, stmt in enumerate(node.body):
                if isinstance(stmt, ast.Return):
                    # Check if there's code after return
                    if i < len(node.body) - 1:
                        next_stmt = node.body[i + 1]
                        self._add_finding(
                            'unreachable_code',
                            next_stmt.lineno if hasattr(next_stmt, 'lineno') else 0,
                            next_stmt.col_offset if hasattr(next_stmt, 'col_offset') else 0,
                            "Unreachable code after return statement",
                            self._get_code_snippet(next_stmt.lineno if hasattr(next_stmt, 'lineno') else 0),
                            "Remove unreachable code or restructure logic"
                        )
                        break
                # Check for unreachable code in if/else blocks
                elif isinstance(stmt, ast.If):
                    self._check_unreachable_in_block(stmt.body)
                    self._check_unreachable_in_block(stmt.orelse)
    
    def _check_unreachable_in_block(self, block: list) -> None:
        """Check for unreachable code in a block of statements."""
        for i, stmt in enumerate(block):
            if isinstance(stmt, ast.Return):
                if i < len(block) - 1:
                    next_stmt = block[i + 1]
                    self._add_finding(
                        'unreachable_code',
                        next_stmt.lineno if hasattr(next_stmt, 'lineno') else 0,
                        next_stmt.col_offset if hasattr(next_stmt, 'col_offset') else 0,
                        "Unreachable code after return statement",
                        self._get_code_snippet(next_stmt.lineno if hasattr(next_stmt, 'lineno') else 0),
                        "Remove unreachable code or restructure logic"
                    )
                    break
    
    def _check_logic_errors_python(self, node: ast.AST) -> None:
        """Check for common logic errors in Python."""
        # Check for comparison with assignment (= instead of ==)
        if isinstance(node, ast.Compare):
            # Check for suspicious comparisons
            pass
    
    def _check_null_pointer_js(self, node: Any) -> None:
        """Check for null/undefined access in JavaScript."""
        if node.type == 'MemberExpression':
            # Check for potential null/undefined access
            pass
    
    def _check_infinite_loop_js(self, node: Any) -> None:
        """Check for infinite loops in JavaScript."""
        if node.type == 'WhileStatement':
            # Check for while(true) without break
            if hasattr(node, 'test') and hasattr(node.test, 'value'):
                if node.test.value is True:
                    line = node.loc.start.line if hasattr(node, 'loc') else 0
                    self._add_finding(
                        'infinite_loop',
                        line,
                        0,
                        "Infinite loop detected: while(true) without break",
                        self._get_code_snippet(line),
                        "Add a break condition"
                    )
    
    def _check_unreachable_code_js(self, node: Any) -> None:
        """Check for unreachable code in JavaScript."""
        if node.type == 'FunctionDeclaration' or node.type == 'FunctionExpression':
            if hasattr(node, 'body') and hasattr(node.body, 'body'):
                statements = node.body.body
                for i, stmt in enumerate(statements):
                    if stmt.type == 'ReturnStatement':
                        if i < len(statements) - 1:
                            next_stmt = statements[i + 1]
                            line = next_stmt.loc.start.line if hasattr(next_stmt, 'loc') else 0
                            self._add_finding(
                                'unreachable_code',
                                line,
                                0,
                                "Unreachable code after return statement",
                                self._get_code_snippet(line),
                                "Remove unreachable code"
                            )
                            break
    
    def _has_break_statement(self, node: ast.AST) -> bool:
        """Check if a node contains a break statement."""
        for child in ast.walk(node):
            if isinstance(child, ast.Break):
                return True
        return False
    
    def _get_code_snippet(self, line_number: int, context: int = 2) -> str:
        """Get code snippet around the line."""
        if not self.code_lines or line_number <= 0:
            return ""
        
        start = max(0, line_number - context - 1)
        end = min(len(self.code_lines), line_number + context)
        return '\n'.join(self.code_lines[start:end])
    
    def _add_finding(
        self,
        rule_key: str,
        line: int,
        column: int,
        message: str,
        snippet: str,
        suggestion: str
    ) -> None:
        """Add a bug finding."""
        rule = self.rules.get(rule_key)
        if not rule:
            return
        
        finding = Finding(
            id=f"{rule.rule_id}-{len(self.findings) + 1}",
            type=FindingType.BUG,
            severity=rule.severity,
            line_number=line,
            column_number=column,
            message=message,
            code_snippet=snippet,
            suggestion=suggestion
        )
        
        self.findings.append(finding)
    
    def get_bug_rules(self, language: str) -> List[BugRule]:
        """Get available bug detection rules for a language."""
        return list(self.rules.values())
    
    def configure_rules(self, enabled_rules: List[str]) -> None:
        """Configure which rules are enabled."""
        # Filter rules based on enabled list
        if enabled_rules:
            self.rules = {k: v for k, v in self.rules.items() if k in enabled_rules}
