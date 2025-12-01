@echo off
echo ===================================================
echo 🧹 ANTI-LUST GUARDIAN: DISK CLEANUP TOOL
echo ===================================================
echo.
echo [1] Purging PIP Cache (Frees space on C: drive)...
python -m pip cache purge
echo.
echo [2] Removing Python Cache files (__pycache__)...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo.
echo [3] Removing Pytest Cache...
if exist ".pytest_cache" rd /s /q ".pytest_cache"
echo.
echo ===================================================
echo ✅ CLEANUP COMPLETE
echo.
echo Please check your C: drive space now.
echo If you still need space, you must manually delete
echo large files (videos, games, downloads) from your C: drive.
echo ===================================================
pause
