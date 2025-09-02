#!/bin/bash
echo "📊 Updating Billboard Hot 100 Data..."

# Activate environment and run scraper
cd python_backend && source venv/bin/activate && python run_scraper.py && python validate_data_quality.py

echo "✅ Billboard data updated!"
echo "📊 Entries found: $(cat data/current/billboard_chart_data.json | jq '.data.total_entries')"
echo "🚀 Ready to deploy: git add . && git commit -m 'Update Billboard data' && git push"
