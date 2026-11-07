import asyncio
import os
import signal
import hmac
from pathlib import Path

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field


app = FastAPI(title="Local AI Executor")

WORKSPACE = Path("/workspace").resolve()

API_TOKEN = os.environ.get("EXECUTOR_API_TOKEN")

if not API_TOKEN:
    raise RuntimeError("EXECUTOR_API_TOKEN is not configured")

COMMAND_TIMEOUT = 60
MAX_OUTPUT_SIZE = 10_000
MAX_CONCURRENT_COMMANDS = 2

semaphore = asyncio.Semaphore(MAX_CONCURRENT_COMMANDS)


class ExecuteRequest(BaseModel):
    command: list[str] = Field(min_length=1, max_length=20)
    working_directory: str = "."


class ExecuteResponse(BaseModel):
    exit_code: int
    stdout: str
    stderr: str


async def read_limited(stream, limit):
    """Read all output, but only retain a limited amount."""
    output = bytearray()

    while True:
        chunk = await stream.read(4096)

        if not chunk:
            break

        remaining = limit - len(output)

        if remaining > 0:
            output.extend(chunk[:remaining])

    return output.decode(errors="replace")


@app.post("/execute", response_model=ExecuteResponse)
async def execute_command(
    request: ExecuteRequest,
    authorization: str | None = Header(default=None),
):
    expected_token = f"Bearer {API_TOKEN}"

    if not authorization or not hmac.compare_digest(
        authorization, expected_token
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API token",
        )

    working_directory = (
        WORKSPACE / request.working_directory
    ).resolve()

    if not working_directory.is_relative_to(WORKSPACE):
        raise HTTPException(
            status_code=403,
            detail="Access outside workspace is not allowed",
        )

    if not working_directory.is_dir():
        raise HTTPException(
            status_code=400,
            detail="Working directory does not exist",
        )

    if not all(arg and "\x00" not in arg for arg in request.command):
        raise HTTPException(
            status_code=400,
            detail="Invalid command arguments",
        )

    async with semaphore:
        try:
            command_env = os.environ.copy()
            command_env.pop("EXECUTOR_API_TOKEN", None)
            process = await asyncio.create_subprocess_exec(
                *request.command,
                cwd=working_directory,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=True,
                env=command_env,
            )

            stdout_task = asyncio.create_task(
                read_limited(process.stdout, MAX_OUTPUT_SIZE)
            )

            stderr_task = asyncio.create_task(
                read_limited(process.stderr, MAX_OUTPUT_SIZE)
            )

            try:
                await asyncio.wait_for(
                    process.wait(),
                    timeout=COMMAND_TIMEOUT,
                )

            except asyncio.TimeoutError:
                os.killpg(process.pid, signal.SIGKILL)
                await process.wait()

                raise HTTPException(
                    status_code=408,
                    detail="Command execution timed out",
                )

            stdout, stderr = await asyncio.gather(
                stdout_task,
                stderr_task,
            )

        except HTTPException:
            raise

        except OSError as error:
            raise HTTPException(
                status_code=500,
                detail=f"Could not execute command: {error}",
            )

    return ExecuteResponse(
        exit_code=process.returncode,
        stdout=stdout,
        stderr=stderr,
    )
