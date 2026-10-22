@echo off
title SkillBridge AI
echo ========================================================
echo   Launching SkillBridge AI on http://localhost:8000
echo ========================================================
python run.py
if errorlevel 1 (
    echo.
    echo Something went wrong while launching. Press any key to exit.
    pause >nul
)
