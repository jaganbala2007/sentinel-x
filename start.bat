@echo off
title Sentinel-X Master Launch
echo ==============================================================================
echo                SENTINEL-X DISASTER INTELLIGENCE PLATFORM
echo                     Smart India Hackathon 2026
echo ==============================================================================
echo.

set PYTHON=python
where python >nul 2>nul
if %errorlevel% neq 0 (
    set PYTHON=py -3
)

echo [*] Starting Sentinel-X FastAPI Backend (Port 8080)...
start "Sentinel-X Backend" cmd /k "%PYTHON% -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload --app-dir backend"

echo [*] Waiting 3 seconds for backend initialization...
timeout /t 3 /nobreak >nul

echo [*] Starting Sentinel-X Frontend Server (Port 3000)...
start "Sentinel-X Frontend" cmd /k "cd frontend && node server.js"

echo [*] Launching Mission Cockpit in browser...
start http://localhost:3000

echo.
echo ==============================================================================
echo   Cockpit:     http://localhost:3000
echo   API Docs:    http://localhost:8080/docs
echo   SIH Demo:    http://localhost:8080/api/v1/sih-demo/current
echo ==============================================================================
