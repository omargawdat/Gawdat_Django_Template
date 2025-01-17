"""
Script to scan a Python project and list all environment variables used,
excluding those that start with "local_" and those that are already declared in the files.
"""

import ast
import logging
import re
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def extract_env_var(node: ast.AST) -> str | None:
    """Extract environment variable name from an AST node if it's a string constant."""
    if isinstance(node, ast.Constant):
        if (
            isinstance(node.value, str)
            and node.value
            and not node.value.lower().startswith("local_")
        ):
            return node.value
    return None


def find_declared_vars(tree: ast.AST) -> set[str]:
    """Find variables that are declared/assigned in the file."""
    declared_vars: set[str] = set()

    for node in ast.walk(tree):
        # Check for direct assignments (var = value)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    declared_vars.add(target.id)

        # Check for augmented assignments (var += value)
        elif isinstance(node, ast.AugAssign):
            if isinstance(target := node.target, ast.Name):
                declared_vars.add(target.id)

        # Check for function parameters
        elif isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                declared_vars.add(arg.arg)

    return declared_vars


def find_env_vars_in_python(file_path: Path) -> set[str]:
    """Parse a Python file and return a set of environment variable names found."""
    env_vars: set[str] = set()
    declared_vars: set[str] = set()

    try:
        tree = ast.parse(file_path.read_text(encoding="utf-8"))
        declared_vars = find_declared_vars(tree)
    except (SyntaxError, OSError, UnicodeDecodeError) as e:
        logger.warning("Skipping %s: %s", file_path, e)
        return env_vars

    for node in ast.walk(tree):
        var_name = None

        # Check os.environ["KEY"]
        if (
            isinstance(node, ast.Subscript)
            and isinstance(node.value, ast.Attribute)
            and node.value.attr == "environ"
            and isinstance(node.value.value, ast.Name)
            and node.value.value.id == "os"
        ):
            var_name = extract_env_var(getattr(node.slice, "value", node.slice))

        # Check os.getenv("KEY")
        elif (
            (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "getenv"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
                and node.args
            )
            or (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "get"
                and isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "environ"
                and isinstance(node.func.value.value, ast.Name)
                and node.func.value.value.id == "os"
                and node.args
            )
            or (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "env"
                and node.args
            )
        ):
            var_name = extract_env_var(node.args[0])

        if var_name and var_name not in declared_vars:
            env_vars.add(var_name)

    return env_vars


def find_declared_vars_in_shell(content: str) -> set[str]:
    """Find variables that are declared in shell scripts."""
    declared_vars: set[str] = set()

    # Pattern to match variable assignments like VAR=value or export VAR=value
    assignment_pattern = r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)="

    for current_line in content.splitlines():
        stripped_line = current_line.strip()
        match = re.match(assignment_pattern, stripped_line)
        if match:
            declared_vars.add(match.group(1))

    return declared_vars


def find_env_vars_in_shell(file_path: Path) -> set[str]:
    """Parse a shell script and return a set of environment variable names found."""
    env_vars: set[str] = set()

    try:
        content = file_path.read_text(encoding="utf-8")
        declared_vars = find_declared_vars_in_shell(content)

        # Pattern to match ${VAR} or $VAR
        pattern1 = r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}"
        pattern2 = r"\$([A-Za-z_][A-Za-z0-9_]*)"

        # Find all matches and exclude declared variables
        all_vars: set[str] = set()
        all_vars.update(re.findall(pattern1, content))
        all_vars.update(re.findall(pattern2, content))

        # Add only variables that aren't declared in the file
        env_vars.update(var for var in all_vars if var not in declared_vars)

    except (OSError, UnicodeDecodeError) as e:
        logger.warning("Skipping %s: %s", file_path, e)

    return env_vars


def scan_project(start_dir: str = ".") -> set[str]:
    """Scan all Python and shell files in a directory for environment variables."""
    all_env_vars: set[str] = set()

    for file_path in Path(start_dir).rglob("*"):
        if file_path.suffix == ".py":
            all_env_vars.update(find_env_vars_in_python(file_path))
        elif file_path.suffix in [".sh", ""] and file_path.is_file():
            # Check content of files without extension for shell script characteristics
            try:
                content = file_path.read_text(encoding="utf-8")
                if content.startswith(("#!/bin/bash", "#!/bin/sh")):
                    all_env_vars.update(find_env_vars_in_shell(file_path))
            except (OSError, UnicodeDecodeError) as e:
                logger.warning("Skipping %s: %s", file_path, e)

    return all_env_vars


if __name__ == "__main__":
    env_vars = scan_project()
    print(
        "\nEnvironment variables used (excluding those starting with 'local_' and declared in files):"
    )
    for var in sorted(env_vars):
        print(f"  - {var}")
