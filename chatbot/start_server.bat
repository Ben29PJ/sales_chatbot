@echo off
echo 🐺 Wolf AI RAG-Enhanced Chatbot Server
echo =========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

echo ✅ Python found
echo 🔄 Using server manager for better control...
echo.

REM Use the server manager for better process control
python server_manager.py start

echo.
echo 👋 Use 'python server_manager.py stop' to stop the server
echo 📊 Use 'python server_manager.py status' to check server status  
echo.
pause
