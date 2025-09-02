# 🚀 Quick Start - Daily Routine

## TURNING THE APP ON LOCALLY
```bash
./scripts/start-dev.sh
```
*Auto-starts: Python venv + both APIs + live server + opens browser + runs validation*

## WHAT IT STARTS
- 🐍 **Python Virtual Environment** (activated globally)
- 📊 **Billboard API** on `http://localhost:8000`
- 🎵 **Reviews API** on `http://localhost:8001` 
- 🌐 **Live Server** on `http://localhost:5500`
- 🔍 **Auto-validation** of all APIs (local + production)
- 🚀 **Browser** opens to `http://localhost:5500`

## STOPPING
```bash
./scripts/stop-dev.sh
```
*Stops all servers and live server*

---
**Available Endpoints:**
- 📊 Billboard: `http://localhost:8000/api/billboard`
- 🎵 Reviews: `http://localhost:8001/api/reviews`
- 🔍 Search: `http://localhost:8001/api/search?q=<query>`
- 📈 Analytics: `http://localhost:8001/api/analytics`
