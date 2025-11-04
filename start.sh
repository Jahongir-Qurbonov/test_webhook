#!/bin/bash

source .env

args=("$@")

uv run fastapi dev app/main.py > /dev/null 2>&1 &
echo "Starting server..."

sleep 5

echo ""
echo "Running CLI command..."
uv run app/cli.py "${args[@]}"
