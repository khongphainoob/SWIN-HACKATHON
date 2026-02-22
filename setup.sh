#!/bin/bash
# setup.sh
# Quick setup script for Linux/macOS

set -e

echo "========================================"
echo "  SWIN Sentiment System - Setup"
echo "========================================"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.10+."
    exit 1
fi
python3 --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d ".venv" ]; then
    echo "  Virtual environment already exists."
else
    python3 -m venv .venv
    echo "  Virtual environment created."
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "Install mode? (1=Production, 2=Development, 3=All) [default: 1]"
read -r installChoice
installChoice=${installChoice:-1}

case $installChoice in
    1)
        echo "  Installing production dependencies..."
        pip install -r requirements.txt
        ;;
    2)
        echo "  Installing development dependencies..."
        pip install -r requirements-dev.txt
        ;;
    3)
        echo "  Installing all dependencies..."
        pip install -r requirements-dev.txt
        pip install -e ".[all]"
        ;;
    *)
        echo "  Installing production dependencies..."
        pip install -r requirements.txt
        ;;
esac
echo ""

# Check dependencies
echo "Verifying installation..."
python check_dependencies.py

# Success
echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Run tests: pytest tests/ -v"
echo "  2. Run demo: python demo_langgraph_workflow.py"
echo "  3. Check docs: cat INSTALL.md"
echo ""
echo "Don't forget to activate the environment:"
echo "  source .venv/bin/activate"
echo ""
