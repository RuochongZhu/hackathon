#!/bin/bash
# deployme.sh
#
# Deploy Shiny for Python from this folder.
# Includes Posit Connect and Connect Cloud options.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python -m pip install rsconnect-python

# Optional: load CONNECT_SERVER and CONNECT_API_KEY from .env
if [ -f ".env" ]; then
  # shellcheck disable=SC1091
  source .env
fi

# Option 1 (active): Posit Connect deployment.
rsconnect deploy shiny . \
  ${CONNECT_SERVER:+--server "$CONNECT_SERVER"} \
  ${CONNECT_API_KEY:+--api-key "$CONNECT_API_KEY"}

# Option 2 (commented): Connect Cloud deployment.
# rsconnect deploy shiny .
