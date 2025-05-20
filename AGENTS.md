
# Contributor Guide

## Dev Environment Tips

Do NOT Run `install.sh` this script, which references `requirements.txt`. This script will be executed during environement setup for you. You can reference`install.sh` and `requirements.txt` to review causes of dependency issues and update these files as needed to address, but the effects will not take place until the next task session.

Do NOT attempt to run any command which requires open network communication.  Your Dev environment is isolated for safety.

## Style Instructions

## Testing Instructions

## CHANGELOG/README Instructions
Append a single line summary to CHANGELOG.md describing the changes with a preceeding timestamp
if errors were encountered, list them indented below the changelog row with a single line summary

When components are added that require manual application startup for local testing/debug, document all steps and commands neccessary to set up the local environment and start services/components in README.md using explcit commands.

## PR instructions


## dev.sh startup script
For applications that can be executed locally, create, or update dev.sh file as needed to completely setup the application and start it.  Example:
```#!/usr/bin/env bash
set -euo pipefail

# Step 1: Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

# Step 2: Activate virtual environment
source venv/bin/activate
echo "Using virtual environment at ./venv"

# Step 3: Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 4: Start backend in background
echo "Starting FastAPI backend..."
cd backend/app
uvicorn main:app --reload &
BACKEND_PID=$!
cd ../../

# Step 5: Start frontend in background
echo "Starting frontend dev server..."
cd frontend
npm install
npm run dev &
FRONTEND_PID=$!
cd ..

# Step 6: Wait briefly for servers to start
sleep 2

# Step 7: Open in default browser (macOS or Linux)
echo "Opening http://localhost:5173..."
if command -v xdg-open > /dev/null; then
  xdg-open http://localhost:5173
elif command -v open > /dev/null; then
  open http://localhost:5173
else
  echo "Please open http://localhost:5173 in your browser"
fi

# Step 8: Wait for servers to shut down manually
wait $BACKEND_PID $FRONTEND_PID
```


