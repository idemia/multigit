#!/bin/bash
set -e

# This script builds the snap, installs it locally, and runs it.
# It should be run from the packaging/snap directory or the project root.

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

echo "--- Building Snap ---"
cd "$PROJECT_ROOT"
# Run snapcraft pointing to the config in packaging/snap
# We use --destructive-mode if you are in a container, but default to standard behavior
snapcraft --project-dir "$SCRIPT_DIR"

# Find the generated snap file
SNAP_FILE=$(ls "$SCRIPT_DIR"/*.snap | head -n 1)

if [ -f "$SNAP_FILE" ]; then
    echo "--- Installing Snap: $SNAP_FILE ---"
    sudo snap install "$SNAP_FILE" --dangerous
    
    echo "--- Running Multigit ---"
    multigit
else
    echo "Error: Snap file not found after build."
    exit 1
fi
