#!/bin/bash
# Install git hooks for the cif-parser project

set -e

echo "Installing git hooks..."

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Check if .githooks directory exists
if [ ! -d ".githooks" ]; then
    echo "❌ Error: .githooks directory not found"
    exit 1
fi

# Check if pre-commit hook exists
if [ ! -f ".githooks/pre-commit" ]; then
    echo "❌ Error: .githooks/pre-commit file not found"
    exit 1
fi

# Make pre-commit hook executable
chmod +x .githooks/pre-commit

# Configure git to use the .githooks directory
git config core.hooksPath .githooks

echo "✅ Git hooks installed successfully!"
echo ""
echo "The pre-commit hook will now run automatically before each commit."
echo "It will check:"
echo "  - Rust: formatting (cargo fmt), linting (clippy), and tests (cargo test)"
echo "  - Python: formatting (black), linting (ruff), type checking (mypy), and tests (pytest)"
echo "  - JavaScript: formatting and linting (biome), and tests (mocha)"
echo ""
echo "To bypass the hooks when needed, use: git commit --no-verify"
