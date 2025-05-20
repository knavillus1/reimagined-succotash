#!/usr/bin/env bash
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
uvicorn backend.app.main:app --reload &
BACKEND_PID=$!

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
