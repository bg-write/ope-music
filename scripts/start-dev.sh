#!/bin/bash
echo "🚀 Starting OPE! Development Environment..."

# Stop any existing servers first
echo "🛑 Stopping any existing servers..."
pkill -f "serve_billboard_data.py" 2>/dev/null || true
pkill -f "serve_reviews_data.py" 2>/dev/null || true
pkill -f "python.*http.server.*5500" 2>/dev/null || true
sleep 1

# Activate virtual environment globally
echo "🐍 Activating Python virtual environment..."
cd python_backend && source venv/bin/activate && cd ..
echo "✅ Virtual environment activated"

# Start both API servers
echo "🌐 Starting API servers..."
echo "💡 Option 1: Auto-start in background (recommended)"
echo "💡 Option 2: Manual start - run './scripts/start-apis.sh' in a new terminal"

# Try to open new terminal, but fallback gracefully
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS - try to open new Terminal window
    if osascript -e 'tell application "Terminal" to do script "cd '"$(pwd)"' && ./scripts/start-apis.sh"' 2>/dev/null; then
        echo "✅ Opened new Terminal window with API servers"
        sleep 4
    else
        echo "⚠️  Could not open new Terminal. Starting servers in background..."
        python python_backend/serve_billboard_data.py &
        python python_backend/serve_reviews_data.py &
        sleep 3
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux - try to open new terminal
    if gnome-terminal -- bash -c "cd '$(pwd)' && ./scripts/start-apis.sh; exec bash" 2>/dev/null || \
       xterm -e "cd '$(pwd)' && ./scripts/start-apis.sh; exec bash" 2>/dev/null; then
        echo "✅ Opened new terminal with API servers"
        sleep 4
    else
        echo "⚠️  Could not open new terminal. Starting servers in background..."
        python python_backend/serve_billboard_data.py &
        python python_backend/serve_reviews_data.py &
        sleep 3
    fi
else
    # Fallback - start in background
    echo "⚠️  Unsupported OS. Starting servers in background..."
    python python_backend/serve_billboard_data.py &
    python python_backend/serve_reviews_data.py &
    sleep 3
fi

echo "✅ API servers should be running"
echo ""
echo "🌐 Available API endpoints:"
echo "   📊 Billboard: http://localhost:8000/api/billboard"
echo "   🎵 Reviews: http://localhost:8001/api/reviews"
echo "   🔍 Search: http://localhost:8001/api/search?q=<query>"
echo "   📈 Analytics: http://localhost:8001/api/analytics"
echo ""

# Start live server for frontend (port 5500)
echo "🚀 Starting live server for frontend..."
if command -v python3 >/dev/null 2>&1; then
    python3 -m http.server 5500 &
    echo "✅ Live server started on http://localhost:5500"
elif command -v python >/dev/null 2>&1; then
    python -m http.server 5500 &
    echo "✅ Live server started on http://localhost:5500"
else
    echo "⚠️  Python not found. Please start a live server manually on port 5500"
fi

sleep 2

# Open all URLs in browser
echo "🌐 Opening all URLs in browser..."
if command -v open >/dev/null 2>&1; then
    # macOS
    open http://localhost:5500/#
    sleep 1
    open http://localhost:8001/api/reviews
    sleep 1
    open http://localhost:8000/api/billboard
elif command -v xdg-open >/dev/null 2>&1; then
    # Linux
    xdg-open http://localhost:5500/#
    sleep 1
    xdg-open http://localhost:8001/api/reviews
    sleep 1
    xdg-open http://localhost:8000/api/billboard
elif command -v start >/dev/null 2>&1; then
    # Windows
    start http://localhost:5500/#
    sleep 1
    start http://localhost:8001/api/reviews
    sleep 1
    start http://localhost:8000/api/billboard
else
    echo "⚠️  Could not auto-open browser. Please open these URLs manually:"
    echo "   🏠 Frontend: http://localhost:5500/#"
    echo "   🎵 Reviews API: http://localhost:8001/api/reviews"
    echo "   📊 Billboard API: http://localhost:8000/api/billboard"
fi

echo ""
echo "🔍 Running validation tests..."
echo "Local APIs:"
billboard_result=$(curl -s http://localhost:8000/api/billboard | jq '.success' 2>/dev/null)
reviews_result=$(curl -s http://localhost:8001/api/reviews | jq '.success' 2>/dev/null)
echo "  📊 Billboard API: $([ "$billboard_result" = "true" ] && echo "✅ Working" || echo "❌ Failed")"
echo "  🎵 Reviews API: $([ "$reviews_result" = "true" ] && echo "✅ Working" || echo "❌ Failed")"

echo "Production APIs:"
prod_billboard_result=$(curl -s https://ope-music.netlify.app/api/billboard | jq '.success' 2>/dev/null)
# Production reviews API returns data directly, not wrapped in success object
prod_reviews_result=$(curl -s https://ope-music.netlify.app/api/reviews | jq '.reviews | length' 2>/dev/null)
echo "  📊 Production Billboard: $([ "$prod_billboard_result" = "true" ] && echo "✅ Working" || echo "❌ Failed")"
echo "  🎵 Production Reviews: $([ "$prod_reviews_result" -gt 0 ] && echo "✅ Working ($prod_reviews_result reviews)" || echo "❌ Failed")"

echo ""
echo "💡 Quick tests:"
echo "   curl http://localhost:8000/api/billboard"
echo "   curl http://localhost:8001/api/reviews"

echo ""
echo "🎉 OPE! Development Environment is ready!"
echo "   🏠 Frontend: http://localhost:5500/#"
echo "   🎵 Reviews API: http://localhost:8001/api/reviews"
echo "   📊 Billboard API: http://localhost:8000/api/billboard"
echo ""
echo "📝 API Server Options:"
echo "   🎯 If you see a new Terminal window: API servers are running there"
echo "   🎯 If not: API servers are running in background of this terminal"
echo "   🎯 Manual option: Open new terminal and run './scripts/start-apis.sh'"
echo ""
echo "🛑 To stop API servers: Run './scripts/stop-dev.sh' or press Ctrl+C in the API terminal"
echo "🚀 This terminal is now free for other commands!"
