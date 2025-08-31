#!/usr/bin/env python3
"""
Billboard Hot 100 Web Scraper
Scrapes weekly chart data from Billboard.com and calculates artist performance scores.

Author: Your Music Analytics Blog
Date: 2025
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
from urllib.parse import unquote

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BillboardScraper:
    """Billboard Hot 100 chart scraper with robust error handling."""
    
    def __init__(self):
        self.base_url = "https://www.billboard.com/charts/hot-100/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_chart_date(self) -> str:
        """Get the current chart date in YYYY-MM-DD format."""
        return datetime.now().strftime('%Y-%m-%d')
    
    def scrape_hot_100(self, max_retries: int = 3, delay: float = 2.0) -> List[Dict]:
        """
        Scrape the Billboard Hot 100 chart.
        
        Args:
            max_retries: Maximum number of retry attempts
            delay: Delay between retries in seconds
            
        Returns:
            List of chart entries with rank, title, artist, and date
        """
        for attempt in range(max_retries):
            try:
                # Attempting to scrape Billboard Hot 100
                
                # Make request with rate limiting
                time.sleep(delay)
                response = self.session.get(self.base_url, timeout=30)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract chart data
                chart_entries = self._parse_chart_html(soup)
                
                if chart_entries:
                    print(f"✅ Successfully scraped {len(chart_entries)} chart entries")
                    return chart_entries
                else:
                    logger.warning("No chart entries found in HTML")
                    
            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    logger.error(f"All {max_retries} attempts failed")
                    raise
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise
        
        return []
    
    def _parse_chart_html(self, soup) -> List[Dict]:
        """
        Parse the HTML to extract chart entries.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            List of chart entry dictionaries
        """
        try:
            # Try multiple selectors for Billboard's current structure
            chart_rows = []
            
            # Method 1: Current Billboard structure
            chart_rows = soup.find_all('div', class_='o-chart-results-list-row-container')
            
            # Method 2: Alternative structure
            if not chart_rows:
                chart_rows = soup.find_all('div', class_='chart-list-item')
            
            # Method 3: Look for chart-related classes
            if not chart_rows:
                chart_rows = soup.find_all('div', class_=lambda x: x and 'chart' in x.lower())
            
            # Method 4: Look for list items
            if not chart_rows:
                chart_rows = soup.find_all('li', class_=lambda x: x and 'chart' in x.lower())
            
            # Method 5: Look for data-rank elements
            if not chart_rows:
                chart_rows = soup.find_all(['div', 'li'], attrs={'data-rank': True})
            
            # Method 6: Look for elements by rank numbers
            if not chart_rows:
                rank_elements = soup.find_all(text=lambda text: text and text.strip().isdigit() and 1 <= int(text.strip()) <= 100)
                if rank_elements:
                    chart_rows = []
                    for rank_elem in rank_elements[:100]:
                        parent = rank_elem.parent
                        if parent:
                            chart_rows.append(parent)
            
            if not chart_rows:
                logger.error("No chart rows found with any method")
                return []
            
            # Total chart rows found
            chart_entries = []
            
            # Process the rows we found
            for index, row in enumerate(chart_rows):
                if index >= 100:  # Limit to top 100
                    break
                    
                try:
                    entry = self._extract_chart_entry(row, index + 1, self.get_chart_date())
                    if entry:
                        chart_entries.append(entry)
                except Exception as e:
                    logger.warning(f"Error parsing row {index + 1}: {e}")
                    continue
            
            # Validate we got enough data
            if len(chart_entries) < 50:
                logger.warning(f"Only found {len(chart_entries)} entries, may need selector updates")
            
            # Check for missing ranks
            if len(chart_entries) < 100:
                extracted_ranks = [entry['rank'] for entry in chart_entries]
                missing_ranks = [r for r in range(1, 101) if r not in extracted_ranks]
                logger.warning(f"❌ MISSING RANKS: {missing_ranks}")
                logger.warning(f"📊 Found {len(chart_entries)}/100 entries. Missing {len(missing_ranks)} ranks.")
            
            return chart_entries
            
        except Exception as e:
            logger.error(f"Error parsing chart HTML: {e}")
            return []
    
    def _extract_chart_entry(self, row, rank: int, chart_date: str) -> Optional[Dict]:
        """
        Extract a single chart entry from a row.
        
        Args:
            row: BeautifulSoup element for the chart row
            rank: Chart position (1-100)
            chart_date: Date of the chart
            
        Returns:
            Dictionary with chart entry data or None if invalid
        """
        try:
            # Extract rank - try multiple methods
            actual_rank = rank
            rank_element = row.find('li', class_='o-chart-results-list__item')
            if rank_element:
                rank_text = rank_element.get_text(strip=True)
                if rank_text.isdigit():
                    actual_rank = int(rank_text)
            
            # Also look for rank in other common locations
            for rank_selector in ['.rank', '.position', '.chart-rank', '[data-rank]']:
                rank_elem = row.select_one(rank_selector)
                if rank_elem:
                    rank_text = rank_elem.get_text(strip=True)
                    if rank_text.isdigit() and 1 <= int(rank_text) <= 100:
                        actual_rank = int(rank_text)
                        break
            
            # Extract song title - try multiple selectors
            title = ""
            title_selectors = [
                'h3.c-title', 'h3', 'h4', '.title', '.song-title', 
                '.chart-title', '.track-title', '[class*="title"]'
            ]
            
            for selector in title_selectors:
                title_element = row.select_one(selector)
                if title_element:
                    title = title_element.get_text(strip=True)
                    if title and len(title) > 1:
                        break
            
            # Extract artist name - try multiple selectors
            artist = ""
            
            # Method 1: ALWAYS try social media share URLs FIRST (most reliable for full artist info)
            artist = self._extract_artist_from_share_urls(row)
            
            # Clean up extra Billboard text from artist field
            if artist:
                artist = artist.replace(" on this week's Billboard Hot 100™!", "")
                artist = artist.replace(" on this week's Billboard Hot 100!", "")
                artist = artist.replace(" on this week's Billboard Hot 100", "")
                artist = artist.replace(" on this week's Billboard Hot 100™", "")
            
            # Method 2: If social media extraction failed, try regular selectors
            if not artist:
                artist_element = row.find('span', class_='c-label')
                if artist_element:
                    artist = artist_element.get_text(strip=True)
            
            # Method 3: Look for artist in links
            if not artist:
                artist_links = row.find_all('a', href=lambda href: href and '/artist/' in href)
                for link in artist_links:
                    text = link.get_text(strip=True)
                    if text and len(text) > 2:
                        artist = text
                        break
            
            # Method 4: If still no artist, try looking for any link text that might be an artist
            if not artist:
                all_links = row.find_all('a')
                for link in all_links:
                    text = link.get_text(strip=True)
                    if (text and 
                        len(text) > 2 and 
                        not re.match(r'^\d{2}/\d{2}/\d{2}$', text) and  # Not date format
                        not re.match(r'^\d+$', text) and  # Not just numbers
                        not re.match(r'^(expand|menu|search|login|share|chart)$', text.lower())):  # Not navigation
                        artist = text
                        break
            
            # Extracted entry data
            
            # Validate entry
            if not title or not artist:
                logger.warning(f"❌ FILTERED OUT Rank {actual_rank}: title='{title}', artist='{artist}' - Missing title or artist")
                return None
            
            # Additional validation
            if len(title) < 2 or len(artist) < 2:
                logger.warning(f"❌ FILTERED OUT Rank {actual_rank}: title='{title}', artist='{artist}' - Text too short after cleaning")
                return None
            
            # Successfully extracted entry
            
            return {
                'rank': actual_rank,
                'title': title,
                'artist': artist,
                'chart_date': chart_date,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"❌ ERROR extracting Rank {rank}: {e}")
            return None
    
    def _extract_artist_from_share_urls(self, row) -> str:
        """
        Extract artist information from social media share URLs.
        
        Args:
            row: BeautifulSoup element for the chart row
            
        Returns:
            Artist string extracted from social media URLs
        """
        try:
            # Look for Facebook and Twitter share links
            share_links = row.find_all('a', href=lambda href: href and ('facebook.com' in href or 'twitter.com' in href))
            
            for link in share_links:
                href = link.get('href', '')
                
                # Try to extract artist from Facebook share URL
                if 'facebook.com' in href:
                    try:
                        # Facebook share URLs often have quote parameter with full artist info
                        if 'quote=' in href:
                            quote_match = re.search(r'quote=([^&]+)', href)
                            if quote_match:
                                quote_text = unquote(quote_match.group(1))
                                # Look for artist information in the quote
                                if ' by ' in quote_text:
                                    # Format: "Song Title by Artist Featuring Other Artist"
                                    parts = quote_text.split(' by ', 1)
                                    if len(parts) == 2:
                                        full_artist_info = parts[1].strip()
                                        return full_artist_info
                    except Exception as e:
                        # Failed to parse Facebook URL
                        pass
                
                # Try to extract artist from Twitter share URL
                if 'twitter.com' in href:
                    try:
                        # Twitter share URLs often have text parameter with full artist info
                        if 'text=' in href:
                            text_match = re.search(r'text=([^&]+)', href)
                            if text_match:
                                text_content = unquote(text_match.group(1))
                                # Look for artist information in the text
                                if ' by ' in text_content:
                                    parts = text_content.split(' by ', 1)
                                    if len(parts) == 2:
                                        full_artist_info = parts[1].strip()
                                        return full_artist_info
                    except Exception as e:
                        # Failed to parse Twitter URL
                        pass
            
            return "" # Return empty string if no artist found
            
        except Exception as e:
            # Error extracting artist from share URLs
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common Billboard artifacts
        text = re.sub(r'Billboard\s*', '', text)
        text = re.sub(r'Hot\s*100\s*', '', text)
        
        return text
    
    def calculate_artist_scores(self, chart_entries: List[Dict]) -> Dict[str, int]:
        """
        Calculate point totals for each artist based on chart performance.
        
        Args:
            chart_entries: List of chart entries from scraping
            
        Returns:
            Dictionary mapping artist names to their total points
        """
        artist_scores = {}
        
        for entry in chart_entries:
            artist = entry['artist']
            rank = entry['rank']
            
            # Point system: #1 = 100 points, #2 = 99 points, etc.
            points = 101 - rank
            
            if artist in artist_scores:
                artist_scores[artist] += points
            else:
                artist_scores[artist] = points
        
        # Sort by total points (descending)
        return dict(sorted(artist_scores.items(), key=lambda x: x[1], reverse=True))
    
    def get_top_artists(self, chart_entries: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        Get the top performing artists of the week.
        
        Args:
            chart_entries: List of chart entries
            top_n: Number of top artists to return
            
        Returns:
            List of top artists with their scores and chart positions
        """
        artist_scores = self.calculate_artist_scores(chart_entries)
        
        top_artists = []
        for i, (artist, total_score) in enumerate(artist_scores.items()):
            if i >= top_n:
                break
                
            # Get all chart positions for this artist
            positions = [entry['rank'] for entry in chart_entries if entry['artist'] == artist]
            positions.sort()
            
            top_artists.append({
                'rank': i + 1,
                'artist': artist,
                'total_score': total_score,
                'chart_positions': positions,
                'songs_count': len(positions)
            })
        
        return top_artists
