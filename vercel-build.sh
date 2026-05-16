#!/bin/bash
set -e

# Generate requirements.txt on the fly
curl -LsSf https://astral.sh/uv/install.sh -o install_uv.sh
chmod +x install_uv.sh
./install_uv.sh
export PATH="$HOME/.local/bin:$PATH"
uv pip compile pyproject.toml -o requirements.txt
