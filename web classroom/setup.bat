@echo off
echo ========================================
echo  Online Classroom - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

echo.
echo [2/5] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)

echo.
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [4/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [5/5] Running database migrations...
cd w_classroom
python manage.py migrate

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo To start the development server:
echo   1. Activate virtual environment: .venv\Scripts\activate
echo   2. Navigate to project: cd w_classroom
echo   3. Run server: python manage.py runserver
echo.
echo Or simply run: start_server.bat
echo.
pause
