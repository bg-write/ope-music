#!/bin/bash
echo "🚀 Starting OPE! API Servers..."
echo "📍 Working directory: $(pwd)"

# Activate virtual environment
echo "🐍 Activating Python virtual environment..."
source python_backend/venv/bin/activate
echo "✅ Virtual environment activated"

# Start both API servers
echo "🌐 Starting API servers..."
python python_backend/serve_billboard_data.py &
python python_backend/serve_reviews_data.py &

echo ""
echo "✅ Both API servers started!"
echo "📊 Billboard API: http://localhost:8000/api/billboard"
echo "🎵 Reviews API: http://localhost:8001/api/reviews"
echo ""
echo "🔄 Press Ctrl+C to stop all servers"

# Wait for user to stop
wait
