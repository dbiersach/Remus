@echo off
rem Start Remus as a UCI engine for En Croissant.
cd /d "%~dp0"
uv run python uci_engine.py %*
