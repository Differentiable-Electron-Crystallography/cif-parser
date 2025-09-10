#!/bin/sh
# Install git hooks for the cif-parser project

echo "Installing git hooks..."

# Create symlink from .git/hooks to .githooks
if [ -d ".git" ]; then
    # Make the pre-commit hook executable
    chmod +x .githooks/pre-commit
    
    # Create symlink
    ln -sf ../../.githooks/pre-commit .git/hooks/pre-commit
    
    echo "✅ Git hooks installed successfully!"
    echo "The pre-commit hook will run automatically before each commit."
    echo ""
    echo "To skip the hooks temporarily, use: git commit --no-verify"
else
    echo "❌ Error: Not in a git repository. Please run this from the project root."
    exit 1
fi