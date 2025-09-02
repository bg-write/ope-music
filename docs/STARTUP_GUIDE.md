# 🚀 OPE! Development Startup Guide

## TURNING THE APP ON LOCALLY

### Quick Start (Recommended)
```bash
./start-dev.sh
```
**This will:**
- ✅ Start Billboard API server (port 8000)
- ✅ Start Reviews API server (port 8001) 
- ✅ Auto-open frontend in browser
- ✅ Show all available endpoints

### Manual Start (Alternative)
```bash
# Start Billboard API
cd python_backend && source venv/bin/activate && cd .. && python serve_billboard_data.py &

# Start Reviews API  
cd python_backend && source venv/bin/activate && cd .. && python serve_reviews_data.py &

# Open frontend manually
open index.html  # macOS
# or xdg-open index.html  # Linux
# or start index.html      # Windows
```

## AVAILABLE API ENDPOINTS

### Billboard API (Port 8000)
- 📊 **Main Data**: `http://localhost:8000/api/billboard`
- 🎯 **Test**: `curl -s http://localhost:8000/api/billboard | jq '.success'`

### Reviews API (Port 8001)
- 🎵 **All Reviews**: `http://localhost:8001/api/reviews`
- 🔍 **Search**: `http://localhost:8001/api/search?q=<query>`
- 📈 **Analytics**: `http://localhost:8001/api/analytics`
- 🎯 **Test**: `curl -s http://localhost:8001/api/reviews | jq '.success'`

## QUICK VALIDATION

### Local APIs
```bash
# Billboard API
curl -s http://localhost:8000/api/billboard | jq '.success'

# Reviews API
curl -s http://localhost:8001/api/reviews | jq '.success'

# Search functionality
curl -s "http://localhost:8001/api/search?q=florence" | jq '.total_results'

# Analytics
curl -s http://localhost:8001/api/analytics | jq '.total_reviews'
```

### Production APIs
```bash
# Billboard API
curl -s https://ope-music.netlify.app/api/billboard | jq '.success'

# Reviews API
curl -s https://ope-music.netlify.app/api/reviews | jq '.success'
```

## STOPPING THE APP

### Quick Stop
```bash
./stop-dev.sh
```

### Manual Stop
```bash
# Kill all Python servers
pkill -f "serve_billboard_data.py"
pkill -f "serve_reviews_data.py"
```

## DEVELOPMENT WORKFLOW

### Adding New Reviews
```bash
./add-review.sh
```

### Updating Billboard Data
```bash
./update-billboard.sh
```

### Deploying to Production
```bash
./deploy-to-netlify.sh
```

## TROUBLESHOOTING

### Port Conflicts
- **Billboard API**: Port 8000
- **Reviews API**: Port 8001
- **Frontend**: Port 5500 (Live Server)

### Common Issues
1. **"Port already in use"**: Run `./stop-dev.sh` first
2. **"No module named 'requests'"**: Make sure venv is activated
3. **CORS errors**: Both servers include CORS headers automatically

### Health Checks
```bash
# Check if servers are running
ps aux | grep "serve_.*_data.py"

# Test API responses
curl -s http://localhost:8000/api/billboard | jq '.data.total_entries'
curl -s http://localhost:8001/api/reviews | jq '.data.metadata.total_reviews'
```

## FRONTEND DEVELOPMENT

### Live Reload
- The frontend automatically detects localhost vs production
- Local APIs are used when available
- Fallback to production APIs if local servers are down

### Testing Changes
1. Make changes to `index.html` or `styles.css`
2. Refresh browser (or use Live Server auto-reload)
3. Test both local and production modes

---

**💡 Pro Tip**: Use `./start-dev.sh` for the complete development experience with auto-opened browser and all APIs running!
