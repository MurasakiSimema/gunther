@echo off
cd /d "%~dp0"
echo Avvio compilazione eseguibile (Solo colore Gunther)...
if exist "%USERPROFILE%\.local\bin\uv.exe" (
    "%USERPROFILE%\.local\bin\uv.exe" run build.py --gunther-only
) else (
    python build.py --gunther-only
)
pause
