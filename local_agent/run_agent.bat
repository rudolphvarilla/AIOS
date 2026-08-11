@echo off
setlocal
set "AGENT_DIR=%~dp0"
set "AIOS_ROOT=%AGENT_DIR%..\Coordinator"

if not exist "%AIOS_ROOT%\" (
    echo ERROR: AIOS workspace was not found at "%AIOS_ROOT%".
    exit /b 2
)

if not exist "%AIOS_ROOT%\.venv\Scripts\python.exe" (
    echo ERROR: "%AIOS_ROOT%\.venv\Scripts\python.exe" was not found.
    exit /b 2
)

if "%~1"=="" (
    echo Usage: run_agent.bat verify ^| regression ^| git-status
    exit /b 2
)

"%AIOS_ROOT%\.venv\Scripts\python.exe" "%AGENT_DIR%agent.py" --root "%AIOS_ROOT%" %*
exit /b %ERRORLEVEL%
