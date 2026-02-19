@echo off
echo Starting Online Classroom Server...
echo.

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Navigate to project directory
cd w_classroom

REM Start server
echo Server starting at http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver

pause
