#!/bin/bash
echo "📊 Updating Billboard Hot 100 Data..."

# Get current date for historical backup
CURRENT_DATE=$(date +"%Y-%m-%d")
echo "📅 Update date: $CURRENT_DATE"

# Check if we have existing current data to backup
if [ -f "data/current/billboard_chart_data.json" ]; then
    echo "📚 Backing up current data to historical..."
    
    # Read the chart date from current data
    CHART_DATE=$(cat data/current/billboard_chart_data.json | jq -r '.chart_date' 2>/dev/null)
    
    if [ "$CHART_DATE" != "null" ] && [ -n "$CHART_DATE" ]; then
        # Extract date from chart_date (format: "Week of August 31, 2025")
        if [[ $CHART_DATE =~ Week\ of\ ([A-Za-z]+)\ ([0-9]+),\ ([0-9]{4}) ]]; then
            MONTH=${BASH_REMATCH[1]}
            DAY=${BASH_REMATCH[2]}
            YEAR=${BASH_REMATCH[3]}
            
            # Convert month name to number
            case $MONTH in
                "January") MONTH_NUM="01" ;;
                "February") MONTH_NUM="02" ;;
                "March") MONTH_NUM="03" ;;
                "April") MONTH_NUM="04" ;;
                "May") MONTH_NUM="05" ;;
                "June") MONTH_NUM="06" ;;
                "July") MONTH_NUM="07" ;;
                "August") MONTH_NUM="08" ;;
                "September") MONTH_NUM="09" ;;
                "October") MONTH_NUM="10" ;;
                "November") MONTH_NUM="11" ;;
                "December") MONTH_NUM="12" ;;
            esac
            
            HISTORICAL_DATE="${YEAR}-${MONTH_NUM}-${DAY}"
            echo "📅 Chart date: $CHART_DATE -> Historical folder: $HISTORICAL_DATE"
            
            # Create historical directory
            mkdir -p "data/historical/$HISTORICAL_DATE"
            
            # Move current data to historical
            cp "data/current/billboard_chart_data.json" "data/historical/$HISTORICAL_DATE/billboard_$HISTORICAL_DATE.json"
            echo "✅ Current data backed up to data/historical/$HISTORICAL_DATE/"
        else
            echo "⚠️  Could not parse chart date format, using current date"
            mkdir -p "data/historical/$CURRENT_DATE"
            cp "data/current/billboard_chart_data.json" "data/historical/$CURRENT_DATE/billboard_$CURRENT_DATE.json"
        fi
    else
        echo "⚠️  No chart date found, using current date"
        mkdir -p "data/historical/$CURRENT_DATE"
        cp "data/current/billboard_chart_data.json" "data/historical/$CURRENT_DATE/billboard_$CURRENT_DATE.json"
    fi
else
    echo "ℹ️  No existing current data to backup"
fi

# Move old exports to historical before running scraper
if [ -d "data/exports" ] && [ "$(ls -A data/exports)" ]; then
    echo "📁 Moving old exports to historical..."
    
    # Get the date from current data for historical folder
    if [ -f "data/current/billboard_chart_data.json" ]; then
        OLD_CHART_DATE=$(cat data/current/billboard_chart_data.json | jq -r '.chart_date' 2>/dev/null)
        if [ "$OLD_CHART_DATE" != "null" ] && [ -n "$OLD_CHART_DATE" ]; then
            # Create historical exports folder
            mkdir -p "data/historical/$OLD_CHART_DATE/exports"
            
            # Move all current exports to historical
            mv data/exports/* "data/historical/$OLD_CHART_DATE/exports/" 2>/dev/null
            echo "✅ Old exports moved to data/historical/$OLD_CHART_DATE/exports/"
        else
            echo "⚠️  Could not determine old chart date for exports backup"
        fi
    fi
fi

# Activate environment and run scraper
echo "🔄 Running Billboard scraper..."
cd python_backend && source venv/bin/activate && python run_scraper.py && python validate_data_quality.py

# Check if scraper was successful
if [ $? -eq 0 ]; then
    echo "✅ Billboard data updated successfully!"
    
    # Move new database exports to data/exports
    echo "📊 Moving new exports to data/exports..."
    cd ..
    if [ -f "python_backend/database_export_artist_scores.csv" ]; then
        mv python_backend/database_export_*.csv data/exports/ 2>/dev/null
        echo "✅ New exports moved to data/exports/"
    fi
    
    # Update Netlify function data for production
    echo "🌐 Updating production API data..."
    cp data/current/billboard_chart_data.json netlify_functions/billboard_data.json
    echo "✅ Production API data updated"
    
    # Display summary
    echo ""
    echo "📊 Update Summary:"
    echo "=================="
    echo "📅 Chart date: $(cat data/current/billboard_chart_data.json | jq -r '.chart_date')"
    echo "📈 Total entries: $(cat data/current/billboard_chart_data.json | jq '.data.total_entries')"
    echo "🏆 Top artist: $(cat data/current/billboard_chart_data.json | jq -r '.data.top_artists[0].artist')"
    echo "📚 Historical backup: Created"
    echo "📁 Current data: Updated"
    echo "📊 Exports: Updated (current week only)"
    
    echo ""
    echo "🚀 Ready to deploy:"
    echo "   git add . && git commit -m 'Update Billboard data' && git push"
else
    echo "❌ Billboard update failed!"
    exit 1
fi
