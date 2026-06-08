@echo off
setlocal

cd /d "%~dp0"
set "PYTHONIOENCODING=utf-8"
set "LOG_FILE=%~dp0refresh_dancing_mad_all_specs.log"
set "LOCK_DIR=%TEMP%\mspec_dancing_mad_refresh.lock"

mkdir "%LOCK_DIR%" 2>nul
if errorlevel 1 (
    echo Dancing Mad refresh is already running.
    echo If this is wrong, close the old window or delete:
    echo %LOCK_DIR%
    pause
    exit /b 1
)

if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo Refreshing Dancing Mad all specs with RDPS...
echo Project: %CD%
echo Python: %PYTHON_EXE%
echo Log: %LOG_FILE%
echo.

"%PYTHON_EXE%" scripts\refresh_dancing_mad_all_specs.py --metric rdps --limit 100 2>&1 | powershell -NoProfile -Command "$input | Tee-Object -FilePath '%LOG_FILE%'"

echo.
echo Done. If failed, check refresh_dancing_mad_all_specs.log.
rmdir "%LOCK_DIR%" 2>nul
pause
