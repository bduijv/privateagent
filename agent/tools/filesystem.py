from pathlib import Path
from langchain_core.tools import tool

WORKSPACE = Path("/workspace").resolve()

@tool
def list_files(path: str = ".") -> str:
    """List files and directories inside the project workspace.

    Use this tool to inspect the structure of a Python project.
    The path must be relative to the workspace root.
    """

    requested_path = (WORKSPACE / path).resolve()

    # Prevent access outside the workspace.
    if not requested_path.is_relative_to(WORKSPACE):
        return "Error: Access outside the workspace is not allowed."

    if not requested_path.exists():
        return f"Error: Path does not exist: {path}"

    if not requested_path.is_dir():
        return f"Error: Not a directory: {path}"

    try:
        entries = sorted(
            requested_path.iterdir(),
            key=lambda entry: (not entry.is_dir(), entry.name.lower()),
        )

        if not entries:
            return "Directory is empty."

        results = []

        for entry in entries:
            entry_type = "DIR " if entry.is_dir() else "FILE"
            results.append(f"{entry_type} {entry.name}")

        return "\n".join(results)

    except PermissionError:
        return "Error: Permission denied."
