@echo off
cd /d "%~dp0"
echo ===================================================
echo 🚀 STARTING ANTI-LUST GUARDIAN BRAIN INSTALLER
echo ===================================================
echo.
echo Switching to project directory...
echo Current location: %CD%
echo.
echo Launching Python Downloader...
python download_all_brains.py
echo.
echo ===================================================
echo ✅ INSTALLATION FINISHED
echo ===================================================
pause
