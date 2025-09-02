# Wolf AI Premium Application Startup Script
Write-Host "Starting Wolf AI Premium Application..." -ForegroundColor Cyan
Write-Host ""

# Check if Python virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Install Python dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
pip install -r requirements_fastapi.txt

# Check if Node.js dependencies are installed
if (-not (Test-Path "react-frontend\node_modules")) {
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Green
    Set-Location react-frontend
    npm install
    Set-Location ..
}

Write-Host ""
Write-Host "Starting services..." -ForegroundColor Cyan
Write-Host ""

# Start FastAPI backend in background
Write-Host "Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {& 'venv\Scripts\Activate.ps1'; python fastapi_app.py}" -WindowStyle Normal

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start React frontend
Write-Host "Starting React Frontend on http://localhost:3001..." -ForegroundColor Green
Set-Location react-frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev" -WindowStyle Normal
Set-Location ..

Write-Host ""
Write-Host "Both services are starting..." -ForegroundColor Cyan
Write-Host "Backend: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3001" -ForegroundColor Yellow
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit startup script..." -ForegroundColor White
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
