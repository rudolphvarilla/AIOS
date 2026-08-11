@echo off
setlocal
cd /d C:\AIOS\Coordinator

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: C:\AIOS\Coordinator\.venv\Scripts\python.exe was not found.
    exit /b 2
)

if "%~1"=="" (
    echo Usage: run_agent.bat verify ^| regression ^| git-status
    exit /b 2
)

.venv\Scripts\python.exe local_agent\agent.py %*
exit /b %ERRORLEVEL%
