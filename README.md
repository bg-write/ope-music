# OPE! 🎵

A music reviews platform with data analytics.

## ✨ Features

- **Music Reviews** - 1-4 scale ratings with decimal precision and rich metadata
- **Smart Search** - Find content by artist or title with optimized performance
- **Shareable Links** - Direct links to individual reviews
- **Mobile-Responsive** - Works on all devices with accessibility features
- **Dynamic Content** - Real-time updates via API with comprehensive metadata
- **Data Export** - CSV download with data quality validation and BigQuery-ready formats
- **Public API** - RESTful endpoint for programmatic access with 15+ metadata fields
- **Analytics Tracking** - User behavior monitoring with performance metrics
- **Data Quality Controls** - Enterprise-grade validation, sanitization, and monitoring
- **BigQuery Integration** - Professional data warehouse with real-time sync
- **Looker Studio Dashboard** - Interactive analytics portfolio showcasing data skills
- **Rich Metadata** - Genre, mood, instrumentation, duration, labels, and more
- **Billboard Integration** - Real-time Hot 100 chart tracking with historical data

## 🚀 Live Site

**Visit**: [https://ope-music.netlify.app](https://ope-music.netlify.app)

**Reviews API**: [https://ope-music.netlify.app/api/reviews](https://ope-music.netlify.app/api/reviews)

**Analytics Dashboard**: [OPE! on Looker Studio](https://lookerstudio.google.com/reporting/86a21abe-e77c-4fda-9b58-423d4a45da2b) (Powered by BigQuery)

## 🛠 Built With

- **HTML5** - Semantic structure with accessibility features
- **CSS3** - Clean, minimal styling with responsive design
- **Vanilla JavaScript** - Dynamic content loading and analytics
- **Markdown** - Simple content management with rich metadata
- **Python** - Content conversion tools and data processing
- **Netlify Functions** - Serverless API backend with CORS support
- **BigQuery** - Enterprise data warehouse with real-time integration
- **Looker Studio** - Professional data visualization and analytics
- **Data Analytics** - CSV export, analytics tracking, and quality monitoring
- **Data Quality** - Validation, sanitization, and comprehensive monitoring

## 📁 Project Structure

```
ope/
├── index.html                    # Main website (API-powered with analytics)
├── styles.css                    # Styling with accessibility features
├── content/                      # Content (Markdown with rich metadata)
│   ├── songs.md                  # Song reviews with comprehensive metadata
│   └── drafts.md                 # Work-in-progress reviews
├── data/                         # DATA STORAGE (All data files)
│   ├── current/                  # THIS WEEK'S DATA (Frontend API)
│   │   └── billboard_chart_data.json
│   ├── exports/                  # THIS WEEK'S ANALYSIS FILES
│   │   └── *_2025-08-31.csv
│   └── historical/               # ALL PAST WEEKS (Organized by Date)
│       ├── 2025-08-30/
│       └── 2025-08-31/
├── python_backend/               # DATA PROCESSING (Development)
│   ├── billboard_scraper.py      # Scrapes Billboard.com
│   ├── serve_billboard_data.py   # Local API server (port 8000)
│   ├── serve_reviews_data.py     # Local API server (port 8001)
│   ├── billboard_database.py     # Database operations
│   └── venv/                     # Python environment
├── netlify_functions/            # PRODUCTION DEPLOYMENT (Live Site)
│   ├── billboard.js              # Production Billboard API
│   ├── reviews.js                # Production Reviews API
│   └── reviews.json              # Reviews data for production
├── scripts/                      # DEVELOPMENT AUTOMATION
│   ├── start-dev.sh              # One-command daily startup
│   ├── stop-dev.sh               # Clean shutdown
│   └── update-billboard.sh       # Weekly data updates
├── docs/                         # Documentation and development notes
└── images/                       # Assets and branding
```

### **🎯 Clear Distinctions:**

- **`data/`** = **DATA STORAGE** (JSON/CSV files, organized by time)
- **`python_backend/`** = **DATA PROCESSING** (Development - your local machine)
- **`netlify_functions/`** = **PRODUCTION DEPLOYMENT** (Live website)
- **`scripts/`** = **DEVELOPMENT AUTOMATION** (One-command workflows)

### **🔄 How They Work Together:**

1. **`python_backend/`** → Scrapes data → Saves to **`data/`**
2. **`python_backend/`** → Serves local APIs (development)
3. **`netlify_functions/`** → Serves production APIs (deployed)
4. **`data/`** → Provides data to both local and production APIs

## 📊 Data Analytics Features

### **Rich Metadata Structure**
- **Song Details**: Artist, title, album, label, genre, mood, instrumentation
- **Review Data**: Date, score, text, with data quality validation
- **Technical Fields**: Duration, language, audio URLs, release dates

### **Professional Analytics**
- **BigQuery Integration** - Real-time data warehouse
- **Looker Studio Dashboard** - Interactive portfolio piece
- **Data Quality Monitoring** - Enterprise-grade validation
- **CSV Export** - Analysis-ready data formats

## 🌐 Deployment

Deployed on Netlify with automatic builds from GitHub. BigQuery integration provides real-time data sync, and Looker Studio dashboard showcases professional analytics skills.

🌽
