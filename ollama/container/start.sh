#!/usr/bin/env bash
set -euo pipefail

echo "Starting Ollama..."

exec ollama serve
