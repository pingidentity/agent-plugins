#!/usr/bin/env bash
# Install shared Git hooks for this repo.
# Run once after cloning: bash scripts/install-hooks.sh
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
git -C "$REPO_ROOT" config core.hooksPath .githooks
chmod +x "$REPO_ROOT/.githooks/pre-commit"
echo "✅ Git hooks installed. Pre-commit checks will run on every commit."
