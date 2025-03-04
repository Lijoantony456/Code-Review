import re
import ast
from typing import List, Dict, Any

def parse_python_file(content: str) -> List[Dict[str, Any]]:
    """Parse a Python file using AST to extract functions, classes, and methods."""
    elements = []
    tree = ast.parse(content)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_content = ast.get_source_segment(content, node)
            elements.append({"type": "class", "name": node.name, "content": class_content})
            
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_content = ast.get_source_segment(content, child)
                    elements.append({
                        "type": "method", "name": child.name, "content": method_content, "class": node.name
                    })
        
        elif isinstance(node, ast.FunctionDef):
            function_content = ast.get_source_segment(content, node)
            elements.append({"type": "function", "name": node.name, "content": function_content})
    
    elements.append({"type": "file", "name": "whole_file", "content": content})
    return elements

def extract_blocks_with_braces(content: str, start_index: int) -> int:
    """Find the closing brace that matches the opening brace."""
    brace_count = 0
    for i in range(start_index, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return i + 1
    return len(content)

def parse_javascript_file(content: str) -> List[Dict[str, Any]]:
    """Parse a JavaScript file using regex and improved brace matching."""
    elements = []
    class_pattern = re.compile(r'class\s+(\w+)\s*(?:extends\s+\w+)?\s*{')
    function_pattern = re.compile(r'(?:function\s+(\w+)|const\s+(\w+)|let\s+(\w+))\s*=\s*(?:async\s*)?\([^)]*\)\s*=>')
    method_pattern = re.compile(r'(\w+)\s*\([^)]*\)\s*{')
    
    for match in class_pattern.finditer(content):
        class_name = match.group(1)
        class_start = match.start()
        class_end = extract_blocks_with_braces(content, class_start)
        class_content = content[class_start:class_end]
        elements.append({"type": "class", "name": class_name, "content": class_content})
        
        for method_match in method_pattern.finditer(class_content):
            method_name = method_match.group(1)
            method_start = method_match.start()
            method_end = extract_blocks_with_braces(class_content, method_start)
            method_content = class_content[method_start:method_end]
            elements.append({"type": "method", "name": method_name, "content": method_content, "class": class_name})
    
    for function_match in function_pattern.finditer(content):
        function_name = next(g for g in function_match.groups() if g)
        function_start = function_match.start()
        function_end = extract_blocks_with_braces(content, function_start)
        function_content = content[function_start:function_end]
        elements.append({"type": "function", "name": function_name, "content": function_content})
    
    elements.append({"type": "file", "name": "whole_file", "content": content})
    return elements

def parse_java_file(content: str) -> List[Dict[str, Any]]:
    """Parse a Java file using regex and brace matching."""
    elements = []
    class_pattern = re.compile(r'\bclass\s+(\w+)\s*(?:extends\s+\w+)?\s*{')
    method_pattern = re.compile(r'(public|private|protected)?\s*(static|final)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*{')
    
    for match in class_pattern.finditer(content):
        class_name = match.group(1)
        class_start = match.start()
        class_end = extract_blocks_with_braces(content, class_start)
        class_content = content[class_start:class_end]
        elements.append({"type": "class", "name": class_name, "content": class_content})
        
        for method_match in method_pattern.finditer(class_content):
            method_name = method_match.group(3)
            method_start = method_match.start()
            method_end = extract_blocks_with_braces(class_content, method_start)
            method_content = class_content[method_start:method_end]
            elements.append({"type": "method", "name": method_name, "content": method_content, "class": class_name})
    
    elements.append({"type": "file", "name": "whole_file", "content": content})
    return elements

def parse_generic_file(content: str) -> List[Dict[str, Any]]:
    """Parse a generic file without language-specific parsing."""
    return [{"type": "file", "name": "whole_file", "content": content}]

def parse_code_file(file_path: str, content: str, language: str) -> List[Dict[str, Any]]:
    """Parse a code file based on its language."""
    if language == "Python":
        return parse_python_file(content)
    elif language in ["JavaScript", "TypeScript"]:
        return parse_javascript_file(content)
    elif language == "Java":
        return parse_java_file(content)
    else:
        return parse_generic_file(content)
