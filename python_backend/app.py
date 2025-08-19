#!/usr/bin/env python3
"""
Flask API for OPE! Music Reviews
Serves review data from JSON files
"""

from flask import Flask, jsonify, request
import json
import os
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Configuration
DATA_FILE = Path(__file__).parent / "data" / "reviews.json"

def load_reviews():
    """Load reviews from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('reviews', [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_reviews(reviews):
    """Save reviews to JSON file"""
    try:
        data = {
            "metadata": {
                "last_updated": datetime.now().isoformat(),
                "total_reviews": len(reviews)
            },
            "reviews": reviews
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving reviews: {e}")
        return False

@app.route('/')
def home():
    """API home endpoint"""
    return jsonify({
        "message": "OPE! Music Reviews API",
        "version": "1.0.0",
        "endpoints": {
            "reviews": "/api/reviews",
            "review_by_id": "/api/reviews/<review_id>",
            "search": "/api/search?q=<query>",
            "analytics": "/api/analytics"
        }
    })

@app.route('/api/reviews')
def get_reviews():
    """Get all reviews with optional pagination"""
    reviews = load_reviews()
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_reviews = reviews[start_idx:end_idx]
    
    return jsonify({
        "reviews": paginated_reviews,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(reviews),
            "pages": (len(reviews) + per_page - 1) // per_page
        }
    })

@app.route('/api/reviews/<review_id>')
def get_review(review_id):
    """Get a specific review by ID"""
    reviews = load_reviews()
    
    # Find review by ID
    review = next((r for r in reviews if r['review_id'] == review_id), None)
    
    if review:
        return jsonify(review)
    else:
        return jsonify({"error": "Review not found"}), 404

@app.route('/api/search')
def search_reviews():
    """Search reviews by artist, song title, or text"""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({"error": "Search query required"}), 400
    
    reviews = load_reviews()
    results = []
    
    # Split search into individual terms
    search_terms = query.split()
    
    for review in reviews:
        # Create searchable text
        searchable_text = f"{review['song_artist']} {review['song_title']} {review['review_text']}".lower()
        
        # Check if ALL terms appear somewhere
        if all(term in searchable_text for term in search_terms):
            results.append(review)
    
    return jsonify({
        "query": query,
        "results": results,
        "total_results": len(results)
    })

@app.route('/api/analytics')
def get_analytics():
    """Get basic analytics about reviews"""
    reviews = load_reviews()
    
    if not reviews:
        return jsonify({"error": "No reviews found"}), 404
    
    # Calculate analytics
    total_reviews = len(reviews)
    
    # Rating distribution
    rating_counts = {}
    for review in reviews:
        score = review['review_score']
        rating_counts[score] = rating_counts.get(score, 0) + 1
    
    # Artist counts
    artist_counts = {}
    for review in reviews:
        artist = review['song_artist']
        artist_counts[artist] = artist_counts.get(artist, 0) + 1
    
    # Most reviewed artist
    most_reviewed_artist = max(artist_counts.items(), key=lambda x: x[1]) if artist_counts else None
    
    return jsonify({
        "total_reviews": total_reviews,
        "rating_distribution": rating_counts,
        "artist_counts": artist_counts,
        "most_reviewed_artist": most_reviewed_artist,
        "average_rating": "N/A"  # We'll implement this later
    })

@app.route('/api/export/csv')
def export_csv():
    """Export reviews to CSV format for BigQuery practice"""
    reviews = load_reviews()
    
    if not reviews:
        return jsonify({"error": "No reviews found"}), 404
    
    # Create CSV content
    csv_lines = []
    
    # Header
    headers = ['review_id', 'song_title', 'song_artist', 'review_date', 'review_score', 'review_text', 'song_url']
    csv_lines.append(','.join(headers))
    
    # Data rows
    for review in reviews:
        # Escape commas and quotes in text fields
        row = [
            review['review_id'],
            f'"{review["song_title"].replace('"', '""')}"',
            f'"{review["song_artist"].replace('"', '""')}"',
            f'"{review["review_date"].replace('"', '""')}"',
            review['review_score'],
            f'"{review["review_text"].replace('"', '""').replace(",", ";")}"',
            review['song_url']
        ]
        csv_lines.append(','.join(row))
    
    csv_content = '\n'.join(csv_lines)
    
    return csv_content, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=ope_reviews.csv'
    }

if __name__ == '__main__':
    print("🎵 Starting OPE! Music Reviews API...")
    print(f"📁 Data file: {DATA_FILE}")
    print("🌐 API will be available at: http://localhost:5001")
    print("📚 Endpoints:")
    print("   - GET /api/reviews - List all reviews")
    print("   - GET /api/reviews/<id> - Get specific review")
    print("   - GET /api/search?q=<query> - Search reviews")
    print("   - GET /api/analytics - Get analytics")
    print("   - GET /api/export/csv - Export to CSV")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5001)
