@echo off
REM Quick Test Script for 3-Tier Priority System

echo.
echo =====================================
echo  HardChews 3-Tier Priority System
echo =====================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate venv
call venv\Scripts\activate.bat

REM Run backend and test in parallel
echo Starting Backend...
echo.

REM Start backend in separate window
start "HardChews Backend" cmd /k "uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

REM Wait for backend to start
timeout /t 3 /nobreak

echo.
echo =====================================
echo  Running Priority System Test Suite
echo =====================================
echo.

REM Run tests
python test_priority_system.py

echo.
echo =====================================
echo  Frontend: Open index_v2.html in Browser
echo =====================================
echo.
echo Backend running at: http://localhost:8000
echo Health check: http://localhost:8000/health
echo.
pause
