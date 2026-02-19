@echo off
REM Online Classroom - Log Viewer (Windows)
REM Quick utility to view application logs

echo ========================================
echo  Online Classroom - Log Viewer
echo ========================================
echo.

set LOG_DIR=w_classroom\logs

if not exist "%LOG_DIR%" (
    echo Error: Logs directory not found at %LOG_DIR%
    pause
    exit /b 1
)

echo Available logs:
echo   1. Django (general application logs)
echo   2. Errors (error logs only)
echo   3. WebSocket (connection logs)
echo   4. Code Execution (code execution logs)
echo   5. View all recent logs
echo   6. Clear all logs
echo.
set /p choice="Select option (1-6): "

if "%choice%"=="1" goto django
if "%choice%"=="2" goto errors
if "%choice%"=="3" goto websocket
if "%choice%"=="4" goto execution
if "%choice%"=="5" goto all
if "%choice%"=="6" goto clear
goto invalid

:django
echo.
echo === Django Log (last 50 lines) ===
if exist "%LOG_DIR%\django.log" (
    powershell -Command "Get-Content '%LOG_DIR%\django.log' -Tail 50"
) else (
    echo No django.log found
)
goto end

:errors
echo.
echo === Error Log (last 50 lines) ===
if exist "%LOG_DIR%\errors.log" (
    powershell -Command "Get-Content '%LOG_DIR%\errors.log' -Tail 50"
) else (
    echo No errors.log found
)
goto end

:websocket
echo.
echo === WebSocket Log (last 50 lines) ===
if exist "%LOG_DIR%\websocket.log" (
    powershell -Command "Get-Content '%LOG_DIR%\websocket.log' -Tail 50"
) else (
    echo No websocket.log found
)
goto end

:execution
echo.
echo === Code Execution Log (last 50 lines) ===
if exist "%LOG_DIR%\code_execution.log" (
    powershell -Command "Get-Content '%LOG_DIR%\code_execution.log' -Tail 50"
) else (
    echo No code_execution.log found
)
goto end

:all
echo.
echo === Django Log ===
if exist "%LOG_DIR%\django.log" (
    powershell -Command "Get-Content '%LOG_DIR%\django.log' -Tail 20"
) else (
    echo No django.log found
)
echo.
echo === Error Log ===
if exist "%LOG_DIR%\errors.log" (
    powershell -Command "Get-Content '%LOG_DIR%\errors.log' -Tail 20"
) else (
    echo No errors.log found
)
echo.
echo === WebSocket Log ===
if exist "%LOG_DIR%\websocket.log" (
    powershell -Command "Get-Content '%LOG_DIR%\websocket.log' -Tail 20"
) else (
    echo No websocket.log found
)
echo.
echo === Code Execution Log ===
if exist "%LOG_DIR%\code_execution.log" (
    powershell -Command "Get-Content '%LOG_DIR%\code_execution.log' -Tail 20"
) else (
    echo No code_execution.log found
)
goto end

:clear
echo.
set /p confirm="Are you sure you want to clear all logs? (y/n): "
if /i "%confirm%"=="y" (
    del /q "%LOG_DIR%\*.log" 2>nul
    echo All logs cleared.
) else (
    echo Cancelled.
)
goto end

:invalid
echo Invalid option
goto end

:end
echo.
echo ========================================
echo Log files location: %LOG_DIR%
echo ========================================
echo.
pause
