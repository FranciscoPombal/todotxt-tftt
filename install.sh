#!/usr/bin/env bash
set -e -o pipefail -u

# 1. Make sure we are in the repository directory first
SCRIPT_PATH=$(readlink -f "${BASH_SOURCE[0]}")
THIS_DIR=$(dirname "${SCRIPT_PATH}")
cd "${THIS_DIR}"

# 2. Make sure uv is available and create virtual environment.
if ! command -v uv &> /dev/null; then
    printf "Error: 'uv' is not installed, please install uv and try again.\n"
    exit 1
fi
uv --quiet sync

# 3. Ensure the target script is executable
chmod +x tftt

printf "Installed! To use the tftt frontend, run: todo.sh tftt\n"
