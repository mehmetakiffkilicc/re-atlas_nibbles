@echo off
echo ==========================================
echo    Starting GreenGrid Project (RE-Atlas)
echo ==========================================

echo [1/2] Starting Backend...
start "GreenGrid Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8000"

echo [2/2] Starting Frontend...
start "GreenGrid Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================
echo    Project is starting in separate windows.
echo    Backend: http://localhost:8000
echo    Frontend: http://localhost:5173
echo ==========================================
pause
