@echo off
cd /d "%~dp0"
echo Avvio compilazione eseguibile (Tutti i colori)...
if exist "%USERPROFILE%\.local\bin\uv.exe" (
    "%USERPROFILE%\.local\bin\uv.exe" run build.py
) else (
    python build.py
)
pause
