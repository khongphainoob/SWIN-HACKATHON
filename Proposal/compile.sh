#!/bin/bash
# Bash script to compile LaTeX proposal
# Usage: chmod +x compile.sh && ./compile.sh

echo "🔧 Compiling IEEE LaTeX Proposal..."

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ pdflatex not found!"
    echo "Please install TeX Live:"
    echo "  Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  macOS: brew install --cask mactex"
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous build files..."
rm -f *.aux *.log *.bbl *.blg *.out *.toc

# First compilation
echo "📄 First pdflatex pass..."
pdflatex -interaction=nonstopmode proposal.tex > /dev/null
if [ $? -ne 0 ]; then
    echo "❌ First compilation failed! Check proposal.log for errors."
    exit 1
fi

# Run BibTeX
if [ -f "proposal.aux" ]; then
    echo "📚 Processing bibliography (BibTeX)..."
    bibtex proposal.aux 2>/dev/null
fi

# Second compilation
echo "📄 Second pdflatex pass..."
pdflatex -interaction=nonstopmode proposal.tex > /dev/null

# Third compilation
echo "📄 Third pdflatex pass (final)..."
pdflatex -interaction=nonstopmode proposal.tex > /dev/null

# Check if PDF was generated
if [ -f "proposal.pdf" ]; then
    echo "✅ Compilation successful!"
    echo ""
    echo "📁 Output file: proposal.pdf"
    
    # Get file size
    filesize=$(du -h proposal.pdf | cut -f1)
    echo "📊 File size: $filesize"
    
    # Count pages
    if command -v pdfinfo &> /dev/null; then
        pages=$(pdfinfo proposal.pdf | grep Pages | awk '{print $2}')
        echo "📄 Pages: $pages"
    fi
    
    echo ""
    echo "🎉 Ready for submission!"
    echo ""
    echo "Next steps:"
    echo "  1. Review proposal.pdf"
    echo "  2. Check for typos and formatting"
    echo "  3. Verify anonymity (no author names)"
    echo "  4. Submit to hackathon portal"
    
    # Ask to open PDF (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        read -p "Open PDF now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            open proposal.pdf
        fi
    fi
    
    # Ask to open PDF (Linux)
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        read -p "Open PDF now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            xdg-open proposal.pdf 2>/dev/null || evince proposal.pdf 2>/dev/null
        fi
    fi
else
    echo "❌ PDF generation failed!"
    echo "Check proposal.log for detailed error messages."
    exit 1
fi

# Optional: Clean auxiliary files
read -p "Clean auxiliary files (.aux, .log, etc.)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning auxiliary files..."
    rm -f *.aux *.log *.bbl *.blg *.out *.toc
    echo "✅ Cleaned!"
fi

echo ""
echo "🚀 All done!"
