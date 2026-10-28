@echo off
rem Start Remus as a UCI engine for Lucas Chess.
cd /d "%~dp0"
uv run python uci_engine.py %*
