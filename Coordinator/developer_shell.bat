@echo off
title AIOS Developer Shell

cd /d C:\AIOS\Coordinator

call .venv\Scripts\activate.bat

echo.
echo ==========================================
echo AIOS Developer Environment
echo ==========================================
python -c "import sys; print('Python :', sys.executable)"
echo ==========================================
echo.

cmd