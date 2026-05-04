@echo off
echo ==========================================
echo    Restarting GreenGrid Project
echo ==========================================

call stop.bat

echo Waiting for processes to clear...
timeout /t 3 /nobreak > nul

call start.bat

echo Restart complete.
