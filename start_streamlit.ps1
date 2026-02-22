# Quick Start Script for Streamlit App
# Run this to test and start the app

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "   🚀 SWIN STREAMLIT APP - QUICK START" -ForegroundColor Cyan
Write-Host "============================================================`n" -ForegroundColor Cyan

# Change to project directory
$projectPath = "d:\AI Agentic Project\SWIN"
Set-Location $projectPath

Write-Host "📂 Working directory: $projectPath`n" -ForegroundColor Yellow

# Step 1: Run pre-flight tests
Write-Host "STEP 1: Running pre-flight tests..." -ForegroundColor Green
Write-Host "------------------------------------------------------------" -ForegroundColor Gray
python test_streamlit_ready.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Pre-flight tests failed!" -ForegroundColor Red
    Write-Host "Please fix the issues before starting streamlit.`n" -ForegroundColor Yellow
    
    $continue = Read-Host "Do you want to start streamlit anyway? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Exiting...`n" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n✅ Pre-flight tests completed!`n" -ForegroundColor Green

# Step 2: Check if streamlit is running
Write-Host "STEP 2: Checking if streamlit is already running..." -ForegroundColor Green
Write-Host "------------------------------------------------------------" -ForegroundColor Gray

$streamlitProcess = Get-Process -Name streamlit -ErrorAction SilentlyContinue

if ($streamlitProcess) {
    Write-Host "⚠️  Streamlit is already running (PID: $($streamlitProcess.Id))" -ForegroundColor Yellow
    $kill = Read-Host "Do you want to kill it and restart? (y/n)"
    
    if ($kill -eq "y") {
        Stop-Process -Id $streamlitProcess.Id -Force
        Write-Host "✅ Killed existing streamlit process`n" -ForegroundColor Green
        Start-Sleep -Seconds 2
    } else {
        Write-Host "Exiting...`n" -ForegroundColor Red
        exit 0
    }
}

# Step 3: Start streamlit
Write-Host "STEP 3: Starting Streamlit app..." -ForegroundColor Green
Write-Host "------------------------------------------------------------" -ForegroundColor Gray
Write-Host "`n🌐 Access the app at: http://localhost:8501`n" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server`n" -ForegroundColor Yellow

try {
    streamlit run streamlit_app.py --server.port 8501
} catch {
    Write-Host "`n❌ Error starting streamlit: $_" -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure streamlit is installed: pip install streamlit" -ForegroundColor Gray
    Write-Host "2. Check if port 8501 is available" -ForegroundColor Gray
    Write-Host "3. Try running: streamlit run streamlit_app.py --server.port 8502" -ForegroundColor Gray
    exit 1
}
