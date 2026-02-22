# PowerShell script to compile LaTeX proposal
# Usage: .\compile.ps1

Write-Host "🔧 Compiling IEEE LaTeX Proposal..." -ForegroundColor Cyan

# Check if pdflatex is installed
if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Host "❌ pdflatex not found!" -ForegroundColor Red
    Write-Host "Please install MiKTeX or TeX Live:" -ForegroundColor Yellow
    Write-Host "  - MiKTeX: https://miktex.org/download" -ForegroundColor Yellow
    Write-Host "  - TeX Live: https://www.tug.org/texlive/" -ForegroundColor Yellow
    exit 1
}

# Clean previous builds
Write-Host "🧹 Cleaning previous build files..." -ForegroundColor Yellow
Remove-Item -Path "*.aux", "*.log", "*.bbl", "*.blg", "*.out", "*.toc" -ErrorAction SilentlyContinue

# First compilation (to generate .aux file)
Write-Host "📄 First pdflatex pass..." -ForegroundColor Green
pdflatex -interaction=nonstopmode proposal.tex
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ First compilation failed! Check proposal.log for errors." -ForegroundColor Red
    exit 1
}

# Run BibTeX (if bibliography exists)
if (Test-Path "proposal.aux") {
    Write-Host "📚 Processing bibliography (BibTeX)..." -ForegroundColor Green
    bibtex proposal.aux 2>$null
}

# Second compilation (to resolve citations)
Write-Host "📄 Second pdflatex pass..." -ForegroundColor Green
pdflatex -interaction=nonstopmode proposal.tex | Out-Null

# Third compilation (to resolve all references)
Write-Host "📄 Third pdflatex pass (final)..." -ForegroundColor Green
pdflatex -interaction=nonstopmode proposal.tex | Out-Null

# Check if PDF was generated
if (Test-Path "proposal.pdf") {
    Write-Host "✅ Compilation successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Output file: proposal.pdf" -ForegroundColor Cyan
    
    # Get file size
    $fileSize = (Get-Item "proposal.pdf").Length / 1KB
    Write-Host "📊 File size: $([math]::Round($fileSize, 2)) KB" -ForegroundColor Cyan
    
    # Count pages (requires pdfinfo or similar tool)
    Write-Host ""
    Write-Host "🎉 Ready for submission!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Review proposal.pdf" -ForegroundColor White
    Write-Host "  2. Check for typos and formatting" -ForegroundColor White
    Write-Host "  3. Verify anonymity (no author names)" -ForegroundColor White
    Write-Host "  4. Submit to hackathon portal" -ForegroundColor White
    
    # Ask to open PDF
    $openPdf = Read-Host "`nOpen PDF now? (y/n)"
    if ($openPdf -eq "y" -or $openPdf -eq "Y") {
        Start-Process "proposal.pdf"
    }
} else {
    Write-Host "❌ PDF generation failed!" -ForegroundColor Red
    Write-Host "Check proposal.log for detailed error messages." -ForegroundColor Yellow
    exit 1
}

# Optional: Clean auxiliary files
$cleanAux = Read-Host "`nClean auxiliary files (.aux, .log, etc.)? (y/n)"
if ($cleanAux -eq "y" -or $cleanAux -eq "Y") {
    Write-Host "🧹 Cleaning auxiliary files..." -ForegroundColor Yellow
    Remove-Item -Path "*.aux", "*.log", "*.bbl", "*.blg", "*.out", "*.toc" -ErrorAction SilentlyContinue
    Write-Host "✅ Cleaned!" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 All done!" -ForegroundColor Cyan
