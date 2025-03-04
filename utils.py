import os
import importlib.util
from typing import Dict, Any, List
import re

# Load configuration from a Python file
def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from a Python file."""
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    return {key: getattr(config, key) for key in dir(config) if not key.startswith("__")}

def extract_file_extension(filename: str) -> str:
    """Extract file extension from a filename."""
    _, ext = os.path.splitext(filename)
    return ext.lstrip('.')

def is_code_file(filename: str) -> bool:
    """Check if a file is a code file based on its extension."""
    code_extensions = {
        'py', 'js', 'ts', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php',
        'scala', 'rs', 'swift', 'kt', 'sh', 'html', 'css', 'sql'
    }
    return extract_file_extension(filename).lower() in code_extensions

def filter_code_files(file_paths: List[str]) -> List[str]:
    """Filter a list of file paths to include only code files."""
    return [path for path in file_paths if is_code_file(path)]

def get_language_from_extension(filename: str) -> str:
    """Get programming language name from file extension."""
    ext_to_lang = {
        'py': 'Python',
        'js': 'JavaScript',
        'ts': 'TypeScript',
        'java': 'Java',
        'c': 'C',
        'cpp': 'Cplus',
        'cs': 'Csharp',
        'go': 'Go',
        'rb': 'Ruby',
        'php': 'PHP',
        'scala': 'Scala',
        'rs': 'Rust',
        'swift': 'Swift',
        'kt': 'Kotlin',
        'sh': 'Shell',
        'html': 'HTML',
        'css': 'CSS',
        'sql': 'SQL'
    }
    ext = extract_file_extension(filename).lower()
    return ext_to_lang.get(ext, 'Unknown')

def is_binary_file(filepath: str) -> bool:
    """Check if a file is binary by reading the first chunk."""
    try:
        with open(filepath, 'rb') as file:
            chunk = file.read(1024)
            return b'\0' in chunk
    except Exception:
        return True

def clean_code(code: str) -> str:
    """Clean code by removing extra whitespace and normalizing line endings."""
    # Normalize line endings
    code = code.replace('\r\n', '\n').replace('\r', '\n')
    
    # Remove trailing whitespace from each line
    code = '\n'.join(line.rstrip() for line in code.split('\n'))
    
    # Remove multiple consecutive blank lines
    code = re.sub(r'\n{3,}', '\n\n', code)
    
    return code.strip()

def ensure_language_folders(base_dir: str, languages: List[str]) -> None:
    """Ensure subdirectories exist for each detected programming language."""
    os.makedirs(base_dir, exist_ok=True)
    for lang in languages:
        lang_folder = os.path.join(base_dir, lang)
        os.makedirs(lang_folder, exist_ok=True)

# # Example Usage:
# config = load_config("config.py")  # Make sure config.py exists
# base_folder = config.get("CODE_FOLDER", "codes")  # Use default "codes" if not specified

# languages = ["Python", "JavaScript", "Java"]  # Example detected languages
# ensure_language_folders(base_folder, languages)
