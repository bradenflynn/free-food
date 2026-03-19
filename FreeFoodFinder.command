#!/bin/bash

# Navigate to the project directory
cd "/Users/bradenflynn/Downloads/free food"

# Kill any existing sessions
kill -9 $(pgrep -f "python backend/api/api.py") 2>/dev/null
kill -9 $(pgrep -f "python backend/core/main.py") 2>/dev/null

echo "🚀 Starting Free Food Finder..."

# Activate virtual environment
source .venv/bin/activate

# Start the API in the background
python backend/api/api.py > /dev/null 2>&1 &
API_PID=$!

echo "📡 API Server started on http://localhost:5001"

echo "🔍 Running the Instagram Hunter..."
python backend/core/main.py

echo "📤 Syncing results to GitHub for sharing..."
git add .
git commit -m "Auto-update food finds via local scan"
git push origin main

echo "✅ Scan complete & Shared!"

# Open the dashboard ONLY after the scan and sync are complete
open index.html

echo "🌐 Refresh your public GitHub Pages link to see results."

# Wait for background process if needed, or exit
# kill $API_PID # Uncomment if you want the API to stop when the scan finishes
