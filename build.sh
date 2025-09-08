#!/usr/bin/env bash
set -euo pipefail

# install uv and sync dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

make install

