@echo off
title AIOS Coordinator

REM Go to AIOS project
cd /d C:\AIOS\Coordinator

REM Launch AIOS using the virtual environment directly
.venv\Scripts\python.exe coordinator.py

echo.
pause