#!/bin/bash
# manifestme.sh
#
# Write a Posit deployment manifest for this Shiny for Python app.
# Run from anywhere: ./manifestme.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing rsconnect-python (if needed)..."
python -m pip install rsconnect-python

echo "Writing manifest.json for Shiny app..."
rsconnect write-manifest shiny .

echo "Done. manifest.json created in: $SCRIPT_DIR"
