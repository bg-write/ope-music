# 🎵 Billboard Hot 100 Scraper

A robust Python-based web scraper for Billboard's Hot 100 chart with BigQuery integration and automated weekly data collection.

## 🚀 Features

- **Real-time scraping** from Billboard.com using BeautifulSoup
- **Dual database support**: SQLite (development) + BigQuery (production)
- **Artist scoring system**: #1 = 100 points, #2 = 99 points, etc.
- **Weekly automation** ready for cron jobs
- **Error handling** with retry logic and fallback data
- **Rate limiting** to respect Billboard's servers
- **Data validation** and cleaning

## 📁 File Structure

```
python_backend/
├── billboard_scraper.py      # Main scraper class
├── billboard_database.py     # Database operations
├── test_billboard.py         # Test suite
├── requirements.txt          # Python dependencies
└── README_BILLBOARD.md      # This file
```

## 🛠️ Installation

### 1. Install Dependencies

```bash
cd python_backend
pip install -r requirements.txt
```

### 2. For BigQuery (Optional)

```bash
pip install google-cloud-bigquery google-auth
```

## 🧪 Testing

Run the test suite to verify everything works:

```bash
cd python_backend
python test_billboard.py
```

## 📊 Usage

### Basic Scraping

```python
from billboard_scraper import BillboardScraper

# Initialize scraper
scraper = BillboardScraper()

# Scrape current chart
chart_entries = scraper.scrape_hot_100()

# Calculate artist scores
artist_scores = scraper.calculate_artist_scores(chart_entries)

# Get top artists
top_artists = scraper.get_top_artists(chart_entries, top_n=10)
```

### Database Operations

```python
from billboard_database import BillboardDatabase

# SQLite (development)
db = BillboardDatabase("sqlite", "billboard_charts.db")

# BigQuery (production)
db = BillboardDatabase("bigquery", "your-project-id")

# Save chart data
db.save_chart_data(chart_entries, artist_scores, "2025-01-01")

# Retrieve latest data
latest_chart = db.get_latest_chart_data()
top_artists = db.get_top_artists()
```

## 🗄️ Database Schema

### Chart Entries Table
- `rank`: Chart position (1-100)
- `title`: Song title
- `artist`: Artist name
- `chart_date`: Date of chart
- `scraped_at`: Timestamp of scraping

### Artist Scores Table
- `artist`: Artist name
- `total_score`: Total points across all songs
- `chart_date`: Date of chart
- `songs_count`: Number of songs on chart
- `chart_positions`: JSON array of chart positions
- `scraped_at`: Timestamp of scraping

## 🔄 Weekly Automation

### Cron Job Setup

```bash
# Add to crontab (runs every Monday at 9 AM)
0 9 * * 1 cd /path/to/your/project && python python_backend/billboard_scraper.py
```

### Python Script for Automation

```python
#!/usr/bin/env python3
"""
Weekly Billboard chart scraper
Run this script weekly to collect chart data
"""

from billboard_scraper import BillboardScraper
from billboard_database import BillboardDatabase
import logging

# Setup logging
logging.basicConfig(
    filename='billboard_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def weekly_scrape():
    """Weekly scraping job."""
    try:
        # Initialize components
        scraper = BillboardScraper()
        db = BillboardDatabase("bigquery", "your-project-id")  # or "sqlite"
        
        # Scrape data
        chart_entries = scraper.scrape_hot_100()
        if not chart_entries:
            raise Exception("No chart data found")
        
        # Calculate scores
        artist_scores = scraper.calculate_artist_scores(chart_entries)
        top_artists = scraper.get_top_artists(chart_entries)
        
        # Save to database
        chart_date = scraper.get_chart_date()
        db.save_chart_data(chart_entries, top_artists, chart_date)
        
        logging.info(f"Weekly scrape completed: {len(chart_entries)} entries saved")
        
    except Exception as e:
        logging.error(f"Weekly scrape failed: {e}")
        raise

if __name__ == "__main__":
    weekly_scrape()
```

## 🌐 API Integration

The scraper integrates with your existing Netlify Functions:

- **Endpoint**: `/.netlify/functions/billboard`
- **Returns**: JSON with chart entries, top artists, and metadata
- **Fallback**: Mock data if scraping fails

## 📈 BigQuery Integration

### Setup BigQuery Tables

```sql
-- Create dataset
CREATE DATASET `your-project.billboard`;

-- Chart entries table
CREATE TABLE `your-project.billboard.chart_entries` (
    rank INT64 NOT NULL,
    title STRING NOT NULL,
    artist STRING NOT NULL,
    chart_date DATE NOT NULL,
    scraped_at TIMESTAMP NOT NULL
);

-- Artist scores table
CREATE TABLE `your-project.billboard.artist_scores` (
    artist STRING NOT NULL,
    total_score INT64 NOT NULL,
    chart_date DATE NOT NULL,
    songs_count INT64 NOT NULL,
    chart_positions STRING NOT NULL,
    scraped_at TIMESTAMP NOT NULL
);
```

### BigQuery Queries

```sql
-- Top artists of all time
SELECT 
    artist,
    SUM(total_score) as lifetime_score,
    COUNT(DISTINCT chart_date) as weeks_on_chart
FROM `your-project.billboard.artist_scores`
GROUP BY artist
ORDER BY lifetime_score DESC
LIMIT 20;

-- Chart performance over time
SELECT 
    chart_date,
    COUNT(*) as total_entries,
    AVG(rank) as avg_rank
FROM `your-project.billboard.chart_entries`
GROUP BY chart_date
ORDER BY chart_date DESC;
```

## 🔧 Configuration

### Environment Variables

```bash
# For BigQuery
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
export BIGQUERY_PROJECT_ID="your-project-id"

# For logging
export LOG_LEVEL="INFO"
export LOG_FILE="billboard_scraper.log"
```

### Rate Limiting

Adjust scraping delays in `billboard_scraper.py`:

```python
# In scrape_hot_100 method
time.sleep(delay)  # Default: 2 seconds
```

## 🚨 Error Handling

The scraper includes comprehensive error handling:

- **Network failures**: Automatic retries with exponential backoff
- **HTML parsing errors**: Fallback selectors and validation
- **Database errors**: Transaction rollback and logging
- **Rate limiting**: Respectful delays between requests

## 📊 Data Quality

- **Validation**: Checks for required fields and data types
- **Cleaning**: Removes HTML artifacts and normalizes text
- **Filtering**: Excludes navigation elements and invalid entries
- **Logging**: Detailed logs for debugging and monitoring

## 🔮 Future Enhancements

- **Real-time streaming** with WebSocket updates
- **Machine learning** for trend prediction
- **Social media integration** for artist mentions
- **Geographic analysis** by region/chart
- **Genre classification** and analysis
- **Playlist generation** based on chart data

## 📝 License

This project is part of your music analytics blog. Feel free to modify and extend as needed.

## 🤝 Contributing

1. Test your changes with `python test_billboard.py`
2. Update documentation as needed
3. Follow existing code style and patterns
4. Add logging for new functionality

## 📞 Support

For issues or questions:
1. Check the logs in `billboard_scraper.log`
2. Run the test suite
3. Verify your BigQuery credentials (if using)
4. Check Billboard's HTML structure hasn't changed

---

**Happy scraping! 🎵📊**
