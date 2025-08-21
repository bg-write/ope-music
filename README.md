# OPE! 🎵

A minimal music discovery website powered by dynamic APIs.

## ✨ Features

- **Music Reviews** - 1-4 scale ratings with decimal precision
- **Smart Search** - Find content by artist or title
- **Shareable Links** - Direct links to individual reviews
- **Mobile-Responsive** - Works on all devices
- **Dynamic Content** - Real-time updates via API
- **Data Export** - CSV download with data quality validation and BigQuery-ready formats
- **Public API** - RESTful endpoint for programmatic access
- **Analytics Tracking** - User behavior monitoring with performance metrics
- **Data Quality Controls** - Enterprise-grade validation, sanitization, and dashboard

## 🚀 Live Site

**Visit**: [https://ope-music.netlify.app](https://ope-music.netlify.app)

**Public API**: [https://ope-music.netlify.app/api/reviews](https://ope-music.netlify.app/api/reviews)

## 🛠 Built With

- **HTML5** - Semantic structure
- **CSS3** - Clean, minimal styling
- **Vanilla JavaScript** - Dynamic content loading
- **Markdown** - Simple content management
- **Python** - Content conversion tools
- **Netlify Functions** - Serverless API backend
- **Data Analytics** - CSV export and analytics tracking
- **Data Quality** - Validation, sanitization, and monitoring

## 📁 Project Structure

```
ope/
├── index.html                    # Main website (API-powered)
├── styles.css                    # Styling
├── content/                      # Content (Markdown)
│   ├── songs.md                  # Song reviews
│   └── drafts.md                 # Work-in-progress reviews
├── python_backend/               # Content conversion tools
├── netlify_functions/            # API backend
└── images/                       # Assets
```

## 📝 Content Management

### **Adding New Reviews**
1. **Write in Markdown** - Add to `content/songs.md`
2. **Run converter** - `python python_backend/markdown_converter.py`
3. **Deploy** - `git push` (Netlify auto-deploys)

### **Workflow Benefits**
- ✅ **No build step** - Instant updates
- ✅ **No file corruption** - API handles everything
- ✅ **Scalable** - Easy to add 100+ reviews
- ✅ **Maintainable** - Clean separation of concerns

## 🌐 Deployment

Deployed on Netlify with automatic builds from GitHub. No build process needed - just push to deploy!

🌽
