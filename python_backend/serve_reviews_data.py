#!/usr/bin/env python3
"""
Simple HTTP server to serve Reviews data locally for frontend testing.
This allows the frontend to fetch real Reviews data while we work on the Netlify Function.

Usage:
    python serve_reviews_data.py
"""

import json
import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs
from pathlib import Path

class ReviewsDataHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler that serves Reviews data."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        # Serve Reviews data at /api/reviews
        if parsed_path.path == '/api/reviews':
            self.send_reviews_data()
        elif parsed_path.path == '/api/search':
            self.send_search_results(parsed_path.query)
        elif parsed_path.path == '/api/analytics':
            self.send_analytics_data()
        else:
            # Default to serving files
            super().do_GET()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_reviews_data(self):
        """Send Reviews data as JSON."""
        try:
            # Read the Reviews data file
            data_file = Path('../netlify_functions/reviews.json')
            
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response_data = {
                    'success': True,
                    'data': data,
                    'message': 'Reviews data loaded from local file',
                    'source': 'local_data'
                }
                
                self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
                
            else:
                # Send 404 if data file doesn't exist
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_data = {
                    'success': False,
                    'error': 'Reviews data file not found',
                    'message': 'Reviews data file not found at ../netlify_functions/reviews.json'
                }
                
                self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
                
        except Exception as e:
            # Send 500 on error
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_data = {
                'success': False,
                'error': str(e),
                'message': 'Internal server error'
            }
            
            self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
    
    def send_search_results(self, query_string):
        """Send search results as JSON."""
        try:
            # Parse query parameters
            query_params = parse_qs(query_string)
            search_query = query_params.get('q', [''])[0]
            
            if not search_query:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_data = {
                    'success': False,
                    'error': 'Search query required',
                    'message': 'Please provide a search query with ?q=<query>'
                }
                
                self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
                return
            
            # Read the Reviews data file
            data_file = Path('../netlify_functions/reviews.json')
            
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Search through reviews
                reviews = data.get('reviews', [])
                results = []
                search_terms = search_query.lower().split()
                
                for review in reviews:
                    searchable_text = f"{review.get('song_artist', '')} {review.get('song_title', '')} {review.get('review_text', '')}".lower()
                    if all(term in searchable_text for term in search_terms):
                        results.append(review)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response_data = {
                    'success': True,
                    'query': search_query,
                    'results': results,
                    'total_results': len(results),
                    'message': f'Found {len(results)} results for "{search_query}"',
                    'source': 'local_data'
                }
                
                self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
                
            else:
                # Send 404 if data file doesn't exist
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_data = {
                    'success': False,
                    'error': 'Reviews data file not found',
                    'message': 'Reviews data file not found at ../netlify_functions/reviews.json'
                }
                
                self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
                
        except Exception as e:
            # Send 500 on error
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_data = {
                'success': False,
                'error': str(e),
                'message': 'Internal server error'
            }
            
            self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
    
    def send_analytics_data(self):
        """Send analytics data as JSON."""
        try:
            # Read the Reviews data file
            data_file = Path('../netlify_functions/reviews.json')
            
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                reviews = data.get('reviews', [])
                
                # Calculate analytics
                rating_counts = {}
                artist_counts = {}
                genre_counts = {}
                
                for review in reviews:
                    # Rating distribution
                    score = review.get('review_score', 0)
                    rating_counts[score] = rating_counts.get(score, 0) + 1
                    
                    # Artist counts
                    artist = review.get('song_artist', 'Unknown')
                    artist_counts[artist] = artist_counts.get(artist, 0) + 1
                    
                    # Genre counts
                    genre = review.get('song_genre', 'Unknown')
                    genre_counts[genre] = genre_counts.get(genre, 0) + 1
                
                # Send response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response_data = {
                    'success': True,
                    'total_reviews': len(reviews),
                    'rating_distribution': rating_counts,
                    'artist_counts': artist_counts,
                    'genre_counts': genre_counts,
                    'message': 'Analytics data calculated from local file',
                    'source': 'local_data'
                }
                
                self.wfile.write(json.dumps(response_data, indent=2).encode('utf-8'))
                
            else:
                # Send 404 if data file doesn't exist
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                error_data = {
                    'success': False,
                    'error': 'Reviews data file not found',
                    'message': 'Reviews data file not found at ../netlify_functions/reviews.json'
                }
                
                self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
                
        except Exception as e:
            # Send 500 on error
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_data = {
                'success': False,
                'error': str(e),
                'message': 'Internal server error'
            }
            
            self.wfile.write(json.dumps(error_data, indent=2).encode('utf-8'))
    
    def end_headers(self):
        """Add CORS headers."""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def main():
    """Start the HTTP server."""
    PORT = 8001  # Different port from Billboard server
    
    # Change to the project root directory
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), ReviewsDataHandler) as httpd:
        print(f"🌐 Reviews Data Server running on http://localhost:{PORT}")
        print(f"📊 Reviews data available at: http://localhost:{PORT}/api/reviews")
        print(f"🔍 Search available at: http://localhost:{PORT}/api/search?q=<query>")
        print(f"📈 Analytics available at: http://localhost:{PORT}/api/analytics")
        print(f"📁 Static files served from: {os.getcwd()}")
        print(f"🔄 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    main()
