#!/usr/bin/env python3
"""
Billboard Scraper Runner Script

This script can be run to scrape Billboard Hot 100 data and output it in JSON format.
It's designed to be called from the frontend or run independently.

Usage:
    python run_scraper.py
"""

import json
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from billboard_scraper import BillboardScraper
from billboard_database import BillboardDatabase

def main():
    """Main function to run the scraper and output results."""
    try:
        print("🎵 Starting Billboard Hot 100 Scraper...")
        
        # Initialize scraper
        scraper = BillboardScraper()
        
        # Scrape the data
        print("🌐 Scraping Billboard Hot 100...")
        chart_entries = scraper.scrape_hot_100()
        
        if not chart_entries:
            print("❌ No chart entries found")
            sys.exit(1)
        
        print(f"✅ Successfully scraped {len(chart_entries)} chart entries")
        
        # Calculate artist scores
        print("🏆 Calculating artist scores...")
        artist_scores = scraper.calculate_artist_scores(chart_entries)
        
        # Get top artists
        top_artists = scraper.get_top_artists(chart_entries, top_n=10)
        
        # Prepare output data
        output_data = {
            "chart_date": scraper.get_chart_date(),
            "total_entries": len(chart_entries),
            "scraped_at": datetime.now().isoformat(),
            "chart_entries": chart_entries,
            "top_artists": top_artists
        }
        
        # Output to JSON
        print("💾 Outputting data to JSON...")
        json_output = json.dumps(output_data, indent=2, ensure_ascii=False)
        
        # Write to current data (for frontend API)
        output_file = "../data/current/billboard_chart_data.json"
        os.makedirs("../data/current", exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_output)
        
        print(f"✅ Data saved to {output_file}")
        
        # Create historical backup with date
        chart_date = scraper.get_chart_date()
        if chart_date:
            # Extract date from chart_date (format: "Week of August 31, 2025")
            try:
                from datetime import datetime
                date_obj = datetime.strptime(chart_date, "Week of %B %d, %Y")
                date_str = date_obj.strftime("%Y-%m-%d")
                
                # Create historical folder
                historical_dir = f"../data/historical/{date_str}"
                os.makedirs(historical_dir, exist_ok=True)
                
                # Save historical copy
                historical_file = f"{historical_dir}/billboard_{date_str}.json"
                with open(historical_file, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                
                print(f"📚 Historical backup saved to {historical_file}")
                
            except ValueError:
                print("⚠️  Could not parse chart date for historical backup")
        else:
            print("⚠️  No chart date available for historical backup")
        
        # Also output to stdout for potential piping
        print("\n" + "="*50)
        print("BILLBOARD DATA OUTPUT")
        print("="*50)
        print(json_output)
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
