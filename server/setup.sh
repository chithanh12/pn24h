#!/bin/bash

# Setup script for CSGT Scraper
# This script helps you set up the project environment

set -e  # Exit on error

echo "=========================================="
echo "CSGT Scraper Setup Script"
echo "=========================================="
echo

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python version: $PYTHON_VERSION"
echo

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo

# Check for Tesseract
echo "Checking for Tesseract-OCR..."
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version 2>&1 | head -n1)
    echo "✓ Tesseract found: $TESSERACT_VERSION"
else
    echo "⚠ Tesseract-OCR not found!"
    echo
    echo "Tesseract is required for automatic captcha solving."
    echo "Please install it:"
    echo
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  macOS: brew install tesseract"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Ubuntu/Debian: sudo apt-get install tesseract-ocr"
        echo "  Fedora: sudo dnf install tesseract"
    fi
    echo
    echo "Or download from: https://github.com/tesseract-ocr/tesseract"
fi
echo

# Create necessary directories
echo "Creating directories..."
mkdir -p captcha_images
mkdir -p logs
echo "✓ Directories created"
echo

# Make example scripts executable
echo "Making example scripts executable..."
chmod +x examples/run_scraper.py
chmod +x examples/batch_scraper.py
echo "✓ Scripts are now executable"
echo

echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo
echo "2. Run the example scraper:"
echo "   python examples/run_scraper.py"
echo
echo "3. Or use Scrapy directly:"
echo "   scrapy crawl csgt -a license_plate=30A12345 -O results.json"
echo
echo "For more information, see:"
echo "  - README.md (detailed documentation)"
echo "  - QUICKSTART.md (quick start guide)"
echo
echo "Happy scraping! 🚗🔍"

