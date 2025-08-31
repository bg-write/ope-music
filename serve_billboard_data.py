#!/usr/bin/env python3
"""
Simple HTTP server to serve Billboard data locally for frontend testing.
This allows the frontend to fetch real Billboard data while we work on the Netlify Function.

Usage:
    python serve_billboard_data.py
"""

import json
import http.server
import socketserver
import os
from urllib.parse import urlparse
from pathlib import Path

class BillboardDataHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler that serves Billboard data."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        # Serve Billboard data at /api/billboard
        if parsed_path.path == '/api/billboard':
            self.send_billboard_data()
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
    
    def send_billboard_data(self):
        """Send Billboard chart data as JSON."""
        try:
            # Read the Billboard data file
            data_file = Path('data_output/billboard_chart_data.json')
            
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
                    'message': 'Billboard chart data loaded from local file',
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
                    'error': 'Billboard data file not found',
                    'message': 'Run the scraper first to generate data'
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
    PORT = 8000
    
    # Change to the project root directory
    os.chdir(Path(__file__).parent)
    
    with socketserver.TCPServer(("", PORT), BillboardDataHandler) as httpd:
        print(f"🌐 Billboard Data Server running on http://localhost:{PORT}")
        print(f"📊 Billboard data available at: http://localhost:{PORT}/api/billboard")
        print(f"📁 Static files served from: {os.getcwd()}")
        print(f"🔄 Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")

if __name__ == "__main__":
    main()
