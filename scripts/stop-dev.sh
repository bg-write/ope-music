#!/bin/bash
echo "🛑 Stopping OPE! Development Environment..."

# Kill all Python servers
echo "🔄 Stopping API servers..."
pkill -f "serve_billboard_data.py" 2>/dev/null || echo "   📊 Billboard API: Not running"
pkill -f "serve_reviews_data.py" 2>/dev/null || echo "   🎵 Reviews API: Not running"
pkill -f "python.*http.server.*5500" 2>/dev/null || echo "   🌐 Live server: Not running"

# Kill any remaining Python processes that might be related
pkill -f "python.*serve.*data" 2>/dev/null || true

echo ""
echo "✅ All development servers stopped"
echo "🌐 You can now safely close your browser tabs"
echo "📝 Note: If you started servers in a separate terminal, you may need to close that terminal manually"
