#!/bin/bash

# testme.sh
# A helper script to test the Shiny for Python app locally.
# Run from this folder: ./testme.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python -m shiny run app.py --host 0.0.0.0 --port 8000
