#!/usr/bin/env bash

podman run -it --rm \
  --name ollama-dev \
  --userns=keep-id \
  --network=none \
  -v ~/ai-infra/ollama/models:/models:Z \
  -v ~/dev/ai-projects:/workspace:Z \
  -w /workspace \
  local-ollama
