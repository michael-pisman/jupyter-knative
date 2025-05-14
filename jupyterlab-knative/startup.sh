#!/usr/bin/env bash
set -euo pipefail

# Optional: allow overriding port via $JUPYTER_PORT (default 8888)
PORT="${JUPYTER_PORT:-8888}"

# Ensure we bind to all interfaces
IP="0.0.0.0"

# Token for simple auth (comes from your Knative Service env var)
TOKEN="${JUPYTER_TOKEN:-}"

# Any extra flags you want
EXTRA_ARGS=(
  --NotebookApp.allow_origin='*'
  --NotebookApp.allow_remote_access=True
  --NotebookApp.iopub_data_rate_limit=10000000000
)

echo "Starting JupyterLab on ${IP}:${PORT} with token=${TOKEN:-<none>}"
exec jupyter lab \
     --ip="${IP}" \
     --port="${PORT}" \
     --no-browser \
     --NotebookApp.token="${TOKEN}" \
     "${EXTRA_ARGS[@]}"
