@echo off
rem Start Remus as a UCI engine for Lucas Chess.
rem Run uci_engine.py with the Python in the .venv folder that uv sync built at
rem setup, found by climbing from this folder toward the top of the drive.
cd /d "%~dp0"
set "FOLDER=%~dp0"
:find
if exist "%FOLDER%.venv\Scripts\python.exe" goto found
for %%P in ("%FOLDER%..\") do set "PARENT=%%~fP"
if /i "%PARENT%"=="%FOLDER%" goto missing
set "FOLDER=%PARENT%"
goto find
:found
"%FOLDER%.venv\Scripts\python.exe" uci_engine.py %*
exit /b
:missing
rem No .venv above this folder, such as a copy on a USB drive: let uv build one
uv run python uci_engine.py %*
