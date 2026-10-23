#!/usr/bin/env bash
set -euo pipefail

NETWORK="ai-net"

usage() {
  echo "Usage: $0 [create|reset|delete|inspect]"
  exit 1
}

create_network() {
  if podman network exists "$NETWORK"; then
    echo "Network already exists: $NETWORK"
  else
    echo "Creating internal network: $NETWORK"
    podman network create \
      --internal \
      --driver bridge \
      "$NETWORK"
  fi
}

delete_network() {
  if podman network exists "$NETWORK"; then
    echo "Deleting network: $NETWORK"
    podman network rm "$NETWORK"
  else
    echo "Network does not exist: $NETWORK"
  fi
}

reset_network() {
  echo "Resetting network: $NETWORK"
  podman network rm "$NETWORK" 2>/dev/null || true
  podman network create \
    --internal \
    --driver bridge \
    "$NETWORK"
}

inspect_network() {
  if podman network exists "$NETWORK"; then
    podman network inspect "$NETWORK"
  else
    echo "Network does not exist: $NETWORK"
    exit 1
  fi
}

# ---- CLI handling ----

CMD="${1:-create}"

case "$CMD" in
  create)
    create_network
    ;;
  reset)
    reset_network
    ;;
  delete)
    delete_network
    ;;
  inspect)
    inspect_network
    ;;
  *)
    usage
    ;;
esac

