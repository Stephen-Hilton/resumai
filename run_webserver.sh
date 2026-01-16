#!/usr/bin/env bash
set -euo pipefail

# Default port or use PORT environment variable
PORT=${PORT:-5001}

echo "Attempting to start ResumAI web server on port $PORT..."
echo ""

# Function to check if port is in use
check_port() {
  lsof -ti:$1 2>/dev/null || true
}

# Function to kill process on port
kill_port() {
  local port=$1
  local pid=$(check_port $port)
  
  if [ ! -z "$pid" ]; then
    echo "Found process $pid using port $port"
    kill -9 $pid 2>/dev/null || true
    sleep 2
    return 0
  fi
  return 1
}

# Try to free the port (up to 3 attempts)
for attempt in {1..3}; do
  PID=$(check_port $PORT)
  
  if [ -z "$PID" ]; then
    echo "Port $PORT is available"
    break
  fi
  
  echo "Attempt $attempt: Killing process $PID on port $PORT..."
  kill_port $PORT
  
  # Check if port is now free
  sleep 1
  PID=$(check_port $PORT)
  if [ -z "$PID" ]; then
    echo "Port $PORT is now free"
    break
  fi
  
  if [ $attempt -eq 3 ]; then
    echo ""
    echo "WARNING: Could not free port $PORT after 3 attempts"
    echo ""
    echo "This is likely macOS AirPlay Receiver. You have two options:"
    echo ""
    echo "1. Disable AirPlay Receiver:"
    echo "   System Settings > General > AirDrop & Handoff > AirPlay Receiver (turn OFF)"
    echo ""
    echo "2. Use a different port:"
    echo "   PORT=5001 bash run_webserver.sh"
    echo ""
    exit 1
  fi
done

# Activate virtual environment if it exists
if [ -d ".venv_resumai" ]; then
  source .venv_resumai/bin/activate
fi

# Set Flask environment variables
export FLASK_APP=src/ui/app.py
export FLASK_ENV=development
export PORT=$PORT

# Start the server
echo ""
echo "Starting ResumAI web server on http://localhost:$PORT"
echo "Press Ctrl+C to stop"
echo ""
python -m src.ui.app
