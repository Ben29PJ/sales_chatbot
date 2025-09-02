@echo off
echo Setting up Wolf AI React Frontend...

cd frontend

echo Installing dependencies...
npm install

echo Creating static directories...
if not exist "../static" mkdir "../static"
if not exist "../static/dist" mkdir "../static/dist"

echo Building React app...
npm run build

echo Setup complete!
echo.
echo To run in development mode:
echo   1. Start Flask backend: python app_updated.py
echo   2. Start React frontend: cd frontend && npm run dev
echo.
echo React dev server will be at: http://localhost:3001
echo Flask backend will be at: http://localhost:3000
echo.
pause
