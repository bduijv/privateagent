import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from langchain_core.tools import tool


EXECUTOR_BASE_URL = os.getenv("EXECUTOR_BASE_URL")
EXECUTOR_API_TOKEN = os.getenv("EXECUTOR_API_TOKEN")


@tool
def execute_command(
    command: list[str],
    working_directory: str = ".",
) -> str:
    """Execute a command inside the project workspace.

    Use this tool to run Python scripts, inspect files, install packages,
    run tests, and perform other development tasks.

    Commands are executed in the separate executor container,
    not inside the agent container.

    The working directory must be relative to /workspace.
    """

    if not EXECUTOR_BASE_URL or not EXECUTOR_API_TOKEN:
        return "Error: Executor configuration is missing."

    payload = {
        "command": command,
        "working_directory": working_directory,
    }

    request = Request(
        url=f"{EXECUTOR_BASE_URL}/execute",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {EXECUTOR_API_TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=70) as response:
            result = json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        return f"Executor HTTP error {error.code}: {error.read().decode()}"

    except URLError as error:
        return f"Executor connection error: {error.reason}"

    except TimeoutError:
        return "Error: Executor request timed out."

    return (
        f"Exit code: {result['exit_code']}\n"
        f"STDOUT:\n{result['stdout']}\n"
        f"STDERR:\n{result['stderr']}"
    )
