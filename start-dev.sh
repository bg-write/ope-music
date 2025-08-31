#!/bin/bash
echo "🚀 Starting OPE! Development Environment..."

# Activate virtual environment and start server
cd python_backend && source venv/bin/activate && cd .. && python serve_billboard_data.py &

echo "✅ Billboard API server started on http://localhost:8000"
echo "🌐 Open index.html with live server on port 5500"
echo "📊 Quick test: curl http://localhost:8000/api/billboard"
