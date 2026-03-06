#!/bin/bash

# testme.sh
# A helper script to test the Shiny for R app locally.
# Run from this folder: ./testme.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

Rscript -e "shiny::runApp('app.R', host='0.0.0.0', port=3838)"
