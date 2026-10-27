#!/bin/sh
# Start Remus as a UCI engine for a chess app on macOS or Linux.
# A desktop app does not read the shell PATH, so uv is called by its full path.
cd "$(dirname "$0")" || exit 1
exec "$HOME/.local/bin/uv" run python uci_engine.py "$@"
