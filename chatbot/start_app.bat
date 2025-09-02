@echo off
echo Starting Wolf AI Premium Application...
echo.

REM Check if Python virtual environment exists
if not exist "venv\" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements_fastapi.txt

REM Check if Node.js dependencies are installed
if not exist "react-frontend\node_modules\" (
    echo Installing Node.js dependencies...
    cd react-frontend
    npm install
    cd ..
)

echo.
echo Starting services...
echo.

REM Start FastAPI backend in background
echo Starting FastAPI Backend on http://localhost:8000...
start "FastAPI Backend" cmd /k "venv\Scripts\activate && python fastapi_app.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start React frontend
echo Starting React Frontend on http://localhost:3001...
cd react-frontend
start "React Frontend" cmd /k "npm run dev"

echo.
echo Both services are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3001
echo.
echo Press any key to exit startup script...
pause > nul
