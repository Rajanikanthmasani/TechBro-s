@echo off
echo ============================================================
echo    Modern Mestri - AI Construction Planning System
echo ============================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/3] Checking Ollama installation...
ollama list >nul 2>&1
if errorlevel 1 (
    echo WARNING: Ollama is not running or not installed
    echo The application will work with limited AI features
    echo To enable full AI: Install Ollama from https://ollama.ai
    echo Then run: ollama pull granite3.1-dense:2b
    echo.
) else (
    echo Ollama is running!
    echo.
)

echo [2.5/3] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo WARNING: Failed to install dependencies. Check your internet connection.
) else (
    echo Dependencies installed successfully.
)
echo.

echo [3/3] Starting backend server...
echo.
echo ============================================================
echo Server starting...
echo Once the server starts, the browser will open automatically.
echo http://localhost:5000
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd /d "%~dp0"
:: Launch browser in 4 seconds to give server a head start (and time for pip)
start "" "http://localhost:5000"
timeout /t 2 >nul
python backend\app.py

pause
