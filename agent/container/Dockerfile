FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install only essential system tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        ripgrep \
        fd-find \
        tree \
    && ln -s /usr/bin/fdfind /usr/local/bin/fd \
    && rm -rf /var/lib/apt/lists/*

# Create a dedicated, unprivileged agent user
RUN groupadd --gid 1001 agentuser \
    && useradd --uid 1001 --gid 1001 --create-home agentuser \
    && mkdir -p /workspace \
    && chown agentuser:agentuser /workspace

# Install the initial Python dependencies
RUN pip install --no-cache-dir \
    ollama \
    langgraph \
    langchain-core \
    langchain-ollama \
    pytest \
    ruff

USER agentuser
WORKDIR /workspace

CMD ["bash"]
