#!/usr/bin/env bash
set -euo pipefail

# Export optional debug environment variables if provided
: "${DEBUG:=}"
: "${VITE_ENABLE_DEBUG:=}"
export DEBUG VITE_ENABLE_DEBUG

# Set required Azure Tables variables with sane defaults
: "${AZURE_TABLES_ACCOUNT_URL:=https://knavillus10portfoliostrg.table.core.windows.net}"
: "${AZURE_TABLES_TABLE_NAME:=projects}"

# Set required Azure Blob Storage variables with sane defaults
: "${AZURE_BLOB_STORAGE_ACCOUNT_URL:=https://knavillus10portfoliostrg.blob.core.windows.net}"
: "${AZURE_BLOB_CONTAINER_NAME:=images}"

export AZURE_TABLES_ACCOUNT_URL AZURE_TABLES_TABLE_NAME AZURE_BLOB_STORAGE_ACCOUNT_URL AZURE_BLOB_CONTAINER_NAME

# CORS allowed origins for the backend (comma-separated)
: "${ALLOW_ORIGINS:=http://localhost:5173}"
export ALLOW_ORIGINS

# Function to kill existing processes
kill_existing_processes() {
  echo "Checking for existing backend and frontend processes..."
  BACKEND_PID=$(lsof -ti:8000 || true)
  FRONTEND_PID=$(lsof -ti:5173 || true)

  if [ -n "$BACKEND_PID" ]; then
    echo "Stopping existing backend process (PID: $BACKEND_PID)..."
    kill -9 $BACKEND_PID
  fi

  if [ -n "$FRONTEND_PID" ]; then
    echo "Stopping existing frontend process (PID: $FRONTEND_PID)..."
    kill -9 $FRONTEND_PID
  fi
}

# Step 0: Kill existing processes
kill_existing_processes

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

# Ensure we are in the correct directory before running npm commands
cd frontend
if [ ! -f "package.json" ]; then
  echo "Error: package.json not found in the frontend directory. Please check your working directory."
  exit 1
fi

# Run npm commands in the frontend directory
# Always install dependencies so new packages are picked up
npm install --no-audit --progress=false
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
