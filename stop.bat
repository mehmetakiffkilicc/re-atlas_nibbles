@echo off
echo ==========================================
echo    Stopping GreenGrid Project
echo ==========================================

echo Checking for Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING 2^>nul') do (
    echo Killing Backend process with PID: %%a
    taskkill /F /PID %%a /T 2>nul
)

echo Checking for Frontend (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173 ^| findstr LISTENING 2^>nul') do (
    echo Killing Frontend process with PID: %%a
    taskkill /F /PID %%a /T 2>nul
)

echo Checking for Frontend Alternative (Port 5174)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5174 ^| findstr LISTENING 2^>nul') do (
    echo Killing Frontend process with PID: %%a
    taskkill /F /PID %%a /T 2>nul
)

echo.
echo GreenGrid stopped.
echo ==========================================
pause
