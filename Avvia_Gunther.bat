@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else if exist "%USERPROFILE%\.local\bin\uv.exe" (
    start "" "%USERPROFILE%\.local\bin\uv.exe" run pythonw main.py
) else (
    echo Avvio con python...
    start "" pythonw main.py
)
