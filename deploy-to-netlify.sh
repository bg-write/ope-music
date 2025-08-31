#!/bin/bash

echo "🚀 Preparing Billboard Scraper for Netlify deployment..."

# Ensure data files are up to date
echo "📊 Checking data files..."
if [ ! -f "data_output/billboard_chart_data.json" ]; then
    echo "❌ Billboard data file not found! Run the scraper first."
    echo "   cd python_backend && source venv/bin/activate && python run_scraper.py"
    exit 1
fi

# Verify the Netlify function exists
if [ ! -f "netlify_functions/billboard.js" ]; then
    echo "❌ Billboard Netlify function not found!"
    exit 1
fi

# Check if data is recent (within last 7 days)
data_date=$(grep -o '"chart_date": "[^"]*"' data_output/billboard_chart_data.json | cut -d'"' -f4)
if [ -z "$data_date" ]; then
    echo "⚠️  Warning: Could not determine chart date from data file"
else
    echo "📅 Chart data date: $data_date"
fi

echo "✅ All files ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Commit your changes: git add . && git commit -m 'Ready for Netlify deployment'"
echo "2. Push to your repository: git push origin main"
echo "3. Deploy to Netlify (or enable auto-deploy from your repo)"
echo ""
echo "🌐 Your Billboard API will be available at:"
echo "   https://your-site.netlify.app/api/billboard"
echo ""
echo "💡 The API will work automatically without your local terminal!"
