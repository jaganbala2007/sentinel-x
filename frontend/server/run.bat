@echo off
TITLE Sentinel-X AI Safety OS
COLOR 0B
echo ==========================================================
echo    INITIALIZING SENTINEL-X AI COGNITIVE SAFETY OS
echo ==========================================================
echo Starting internal development server on port 8000...
echo.

:: Launch the browser after a 2-second delay to ensure the server is up
start /b cmd /c "ping localhost -n 2 > nul & start http://localhost:8000"

:: Start the PowerShell Web Server
powershell -ExecutionPolicy Bypass -File dev-server.ps1

pause
