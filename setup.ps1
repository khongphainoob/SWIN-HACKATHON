#!/usr/bin/env pwsh
# setup.ps1
# Quick setup script for Windows PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SWIN Sentiment System - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.10+." -ForegroundColor Red
    exit 1
}
Write-Host "  $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "  Virtual environment already exists." -ForegroundColor Yellow
} else {
    python -m venv .venv
    Write-Host "  Virtual environment created." -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
$installChoice = Read-Host "Install mode? (1=Production, 2=Development, 3=All) [default: 1]"
if ([string]::IsNullOrWhiteSpace($installChoice)) {
    $installChoice = "1"
}

switch ($installChoice) {
    "1" {
        Write-Host "  Installing production dependencies..." -ForegroundColor Cyan
        pip install -r requirements.txt
    }
    "2" {
        Write-Host "  Installing development dependencies..." -ForegroundColor Cyan
        pip install -r requirements-dev.txt
    }
    "3" {
        Write-Host "  Installing all dependencies..." -ForegroundColor Cyan
        pip install -r requirements-dev.txt
        pip install ".[all]"
    }
    default {
        Write-Host "  Installing production dependencies..." -ForegroundColor Cyan
        pip install -r requirements.txt
    }
}

# Check dependencies
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
python check_dependencies.py

# Success
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run tests: pytest tests/ -v" -ForegroundColor White
Write-Host "  2. Run demo: python demo_langgraph_workflow.py" -ForegroundColor White
Write-Host "  3. Check docs: cat INSTALL.md" -ForegroundColor White
Write-Host ""
