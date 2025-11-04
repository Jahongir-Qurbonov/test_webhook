#!/bin/bash

export $(grep -v '^#' .env | xargs)

# Install dependencies
echo "Installing dependencies..."
uv sync

echo "Starting server in background..."
python minimal.py --type server > data/server.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo "Running test with message: '$1'"
python minimal.py --type cli --msg "$1"

# Kill server
kill $SERVER_PID
echo "Server stopped."
