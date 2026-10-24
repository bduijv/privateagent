import os
import sys

from ollama import Client

OLLAMA_HOST = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
MODEL = "qwen2.5-coder:7b"


def main() -> None:
    client = Client(host=OLLAMA_HOST)

    prompt = (
        "You are a local coding assistant. "
        "Reply briefly to confirm that you are running and ready to help "
        "with Python projects."
    )

    print(f"Connecting to Ollama at {OLLAMA_HOST}...")
    print(f"Using model: {MODEL}\n")

    try:
        response = client.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as exc:
        print(f"Could not get a response from Ollama: {exc}", file=sys.stderr)
        sys.exit(1)

    print(response.message.content)


if __name__ == "__main__":
    main()
