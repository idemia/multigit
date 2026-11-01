#!/bin/bash
set -e

# This script builds the snap, installs it locally, and runs it.
# It should be run from the packaging/snap directory or the project root.

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P)"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd -P)"
SOURCE_DIR="$SCRIPT_DIR/project-source"

echo "--- Copying project to $SOURCE_DIR ---"
cd "$PROJECT_ROOT"
rm -rf "$SOURCE_DIR"
mkdir -p "$SOURCE_DIR"

tar -C "$PROJECT_ROOT" \
    --exclude='./.git' \
    --exclude='./.env' \
    --exclude='./env' \
    --exclude='./.venv' \
    --exclude='./.idea' \
    --exclude='./.mypy_cache' \
    --exclude='./.pytest_cache' \
    --exclude='./__pycache__' \
    --exclude='./packaging/snap/project-source' \
    --exclude='./packaging/snap/parts' \
    --exclude='./packaging/snap/stage' \
    --exclude='./packaging/snap/prime' \
    --exclude='./packaging/snap/*.snap' \
    -cf - . | tar -C "$SOURCE_DIR" -xf -


echo "--- Building Snap ---"
# Normal snapcraft flow: keep the build self-contained and do not rely on the
# host Python or host venv state.
cd "$SCRIPT_DIR"
rm -rf parts stage prime ./*.snap
snapcraft pack

# Find the generated snap file
SNAP_FILE=$(ls "$SCRIPT_DIR"/*.snap | head -n 1)

if [ -f "$SNAP_FILE" ]; then
    echo "--- Installing Snap: $SNAP_FILE ---"
    sudo snap install "$SNAP_FILE" --dangerous --classic

    echo "--- Running Multigit ---"
    multigit
else
    echo "Error: Snap file not found after build."
    exit 1
fi
