#!/usr/bin/env python3
"""
Billboard Chart Database Operations
Supports both SQLite (local development) and BigQuery (production).

Author: Your Music Analytics Blog
Date: 2025
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
import os

# BigQuery imports (optional)
try:
    from google.cloud import bigquery
    from google.oauth2 import service_account
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False
    logging.warning("BigQuery not available. Install with: pip install google-cloud-bigquery")

logger = logging.getLogger(__name__)

class BillboardDatabase:
    """Database operations for Billboard chart data."""
    
    def __init__(self, db_type: str = "sqlite", db_path: str = "billboard_charts.db"):
        """
        Initialize database connection.
        
        Args:
            db_type: "sqlite" or "bigquery"
            db_path: For SQLite: file path, for BigQuery: project_id
        """
        self.db_type = db_type.lower()
        self.db_path = db_path
        
        if self.db_type == "sqlite":
            self._init_sqlite()
        elif self.db_type == "bigquery":
            if not BIGQUERY_AVAILABLE:
                raise ImportError("BigQuery not available. Install google-cloud-bigquery")
            self._init_bigquery()
        else:
            raise ValueError("db_type must be 'sqlite' or 'bigquery'")
    
    def _init_sqlite(self):
        """Initialize SQLite database and create tables."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable dict-like access
        
        # Create tables
        self._create_sqlite_tables()
        logger.info(f"SQLite database initialized: {self.db_path}")
    
    def _init_bigquery(self):
        """Initialize BigQuery client."""
        try:
            # Try to use service account credentials
            if os.path.exists('service-account-key.json'):
                credentials = service_account.Credentials.from_service_account_file(
                    'service-account-key.json'
                )
                self.client = bigquery.Client(credentials=credentials, project=self.db_path)
            else:
                # Use default credentials
                self.client = bigquery.Client(project=self.db_path)
            
            # Create tables if they don't exist
            self._create_bigquery_tables()
            logger.info(f"BigQuery client initialized: project {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery: {e}")
            raise
    
    def _create_sqlite_tables(self):
        """Create SQLite tables for chart data."""
        cursor = self.conn.cursor()
        
        # Chart entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chart_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rank INTEGER NOT NULL,
                title TEXT NOT NULL,
                artist TEXT NOT NULL,
                chart_date DATE NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(rank, chart_date)
            )
        ''')
        
        # Artist scores table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS artist_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                artist TEXT NOT NULL,
                total_score INTEGER NOT NULL,
                chart_date DATE NOT NULL,
                songs_count INTEGER NOT NULL,
                chart_positions TEXT NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(artist, chart_date)
            )
        ''')
        
        # Weekly summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chart_date DATE UNIQUE NOT NULL,
                total_entries INTEGER NOT NULL,
                top_artist TEXT NOT NULL,
                top_score INTEGER NOT NULL,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("SQLite tables created successfully")
    
    def _create_bigquery_tables(self):
        """Create BigQuery tables for chart data."""
        try:
            # Chart entries table
            chart_entries_schema = [
                bigquery.SchemaField("rank", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("artist", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("chart_date", "DATE", mode="REQUIRED"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP", mode="REQUIRED")
            ]
            
            chart_entries_table = bigquery.Table(
                f"{self.db_path}.billboard.chart_entries",
                schema=chart_entries_schema
            )
            
            # Artist scores table
            artist_scores_schema = [
                bigquery.SchemaField("artist", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("total_score", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("chart_date", "DATE", mode="REQUIRED"),
                bigquery.SchemaField("songs_count", "INTEGER", mode="REQUIRED"),
                bigquery.SchemaField("chart_positions", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP", mode="REQUIRED")
            ]
            
            artist_scores_table = bigquery.Table(
                f"{self.db_path}.billboard.artist_scores",
                schema=artist_scores_schema
            )
            
            # Create tables (ignore if they exist)
            try:
                self.client.create_table(chart_entries_table, exists_ok=True)
                self.client.create_table(artist_scores_table, exists_ok=True)
                logger.info("BigQuery tables created successfully")
            except Exception as e:
                logger.warning(f"Tables may already exist: {e}")
                
        except Exception as e:
            logger.error(f"Failed to create BigQuery tables: {e}")
            raise
    
    def save_chart_data(self, chart_entries: List[Dict], artist_scores: List[Dict], chart_date: str):
        """
        Save chart data to database.
        
        Args:
            chart_entries: List of chart entries
            artist_scores: List of artist scores
            chart_date: Date of the chart
        """
        try:
            if self.db_type == "sqlite":
                self._save_chart_data_sqlite(chart_entries, artist_scores, chart_date)
            else:
                self._save_chart_data_bigquery(chart_entries, artist_scores, chart_date)
            
            logger.info(f"Chart data saved for {chart_date}")
            
        except Exception as e:
            logger.error(f"Failed to save chart data: {e}")
            raise
    
    def _save_chart_data_sqlite(self, chart_entries: List[Dict], artist_scores: List[Dict], chart_date: str):
        """Save chart data to SQLite database."""
        cursor = self.conn.cursor()
        
        try:
            # Save chart entries
            for entry in chart_entries:
                cursor.execute('''
                    INSERT OR REPLACE INTO chart_entries 
                    (rank, title, artist, chart_date, scraped_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    entry['rank'],
                    entry['title'],
                    entry['artist'],
                    chart_date,
                    entry['scraped_at']
                ))
            
            # Save artist scores
            for score in artist_scores:
                chart_positions = json.dumps(score['chart_positions'])
                cursor.execute('''
                    INSERT OR REPLACE INTO artist_scores 
                    (artist, total_score, chart_date, songs_count, chart_positions, scraped_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    score['artist'],
                    score['total_score'],
                    chart_date,
                    score['songs_count'],
                    chart_positions,
                    datetime.now().isoformat()
                ))
            
            # Save weekly summary
            if artist_scores:
                top_artist = artist_scores[0]
                cursor.execute('''
                    INSERT OR REPLACE INTO weekly_summary 
                    (chart_date, total_entries, top_artist, top_score, scraped_at)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    chart_date,
                    len(chart_entries),
                    top_artist['artist'],
                    top_artist['total_score'],
                    datetime.now().isoformat()
                ))
            
            self.conn.commit()
            
        except Exception as e:
            self.conn.rollback()
            raise
    
    def _save_chart_data_bigquery(self, chart_entries: List[Dict], artist_scores: List[Dict], chart_date: str):
        """Save chart data to BigQuery."""
        try:
            # Prepare chart entries data
            chart_entries_rows = []
            for entry in chart_entries:
                chart_entries_rows.append({
                    'rank': entry['rank'],
                    'title': entry['title'],
                    'artist': entry['artist'],
                    'chart_date': chart_date,
                    'scraped_at': entry['scraped_at']
                })
            
            # Prepare artist scores data
            artist_scores_rows = []
            for score in artist_scores:
                artist_scores_rows.append({
                    'artist': score['artist'],
                    'total_score': score['total_score'],
                    'chart_date': chart_date,
                    'songs_count': score['songs_count'],
                    'chart_positions': json.dumps(score['chart_positions']),
                    'scraped_at': datetime.now().isoformat()
                })
            
            # Insert data
            chart_entries_table = f"{self.db_path}.billboard.chart_entries"
            artist_scores_table = f"{self.db_path}.billboard.artist_scores"
            
            # Use streaming inserts for real-time data
            errors = self.client.insert_rows_json(chart_entries_table, chart_entries_rows)
            if errors:
                logger.error(f"Chart entries insert errors: {errors}")
            
            errors = self.client.insert_rows_json(artist_scores_table, artist_scores_rows)
            if errors:
                logger.error(f"Artist scores insert errors: {errors}")
                
        except Exception as e:
            logger.error(f"Failed to save to BigQuery: {e}")
            raise
    
    def get_latest_chart_data(self, limit: int = 100) -> List[Dict]:
        """
        Get the latest chart data from database.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of chart entries
        """
        try:
            if self.db_type == "sqlite":
                return self._get_latest_chart_data_sqlite(limit)
            else:
                return self._get_latest_chart_data_bigquery(limit)
        except Exception as e:
            logger.error(f"Failed to get latest chart data: {e}")
            return []
    
    def _get_latest_chart_data_sqlite(self, limit: int) -> List[Dict]:
        """Get latest chart data from SQLite."""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT rank, title, artist, chart_date, scraped_at
            FROM chart_entries
            WHERE chart_date = (SELECT MAX(chart_date) FROM chart_entries)
            ORDER BY rank
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def _get_latest_chart_data_bigquery(self, limit: int) -> List[Dict]:
        """Get latest chart data from BigQuery."""
        try:
            query = f'''
                SELECT rank, title, artist, chart_date, scraped_at
                FROM `{self.db_path}.billboard.chart_entries`
                WHERE chart_date = (
                    SELECT MAX(chart_date) 
                    FROM `{self.db_path}.billboard.chart_entries`
                )
                ORDER BY rank
                LIMIT {limit}
            '''
            
            query_job = self.client.query(query)
            results = query_job.result()
            
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"BigQuery query failed: {e}")
            return []
    
    def get_top_artists(self, limit: int = 10) -> List[Dict]:
        """
        Get top performing artists from database.
        
        Args:
            limit: Maximum number of artists to return
            
        Returns:
            List of top artists
        """
        try:
            if self.db_type == "sqlite":
                return self._get_top_artists_sqlite(limit)
            else:
                return self._get_top_artists_bigquery(limit)
        except Exception as e:
            logger.error(f"Failed to get top artists: {e}")
            return []
    
    def _get_top_artists_sqlite(self, limit: int) -> List[Dict]:
        """Get top artists from SQLite."""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT artist, total_score, chart_date, songs_count, chart_positions
            FROM artist_scores
            WHERE chart_date = (SELECT MAX(chart_date) FROM artist_scores)
            ORDER BY total_score DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        artists = []
        for i, row in enumerate(rows):
            chart_positions = json.loads(row['chart_positions'])
            artists.append({
                'rank': i + 1,
                'artist': row['artist'],
                'total_score': row['total_score'],
                'chart_positions': chart_positions,
                'songs_count': row['songs_count']
            })
        
        return artists
    
    def _get_top_artists_bigquery(self, limit: int) -> List[Dict]:
        """Get top artists from BigQuery."""
        try:
            query = f'''
                SELECT artist, total_score, chart_date, songs_count, chart_positions
                FROM `{self.db_path}.billboard.artist_scores`
                WHERE chart_date = (
                    SELECT MAX(chart_date) 
                    FROM `{self.db_path}.billboard.artist_scores`
                )
                ORDER BY total_score DESC
                LIMIT {limit}
            '''
            
            query_job = self.client.query(query)
            results = query_job.result()
            
            artists = []
            for i, row in enumerate(results):
                chart_positions = json.loads(row.chart_positions)
                artists.append({
                    'rank': i + 1,
                    'artist': row.artist,
                    'total_score': row.total_score,
                    'chart_positions': chart_positions,
                    'songs_count': row.songs_count
                })
            
            return artists
            
        except Exception as e:
            logger.error(f"BigQuery query failed: {e}")
            return []
    
    def close(self):
        """Close database connections."""
        if self.db_type == "sqlite" and hasattr(self, 'conn'):
            self.conn.close()
        elif self.db_type == "bigquery" and hasattr(self, 'client'):
            self.client.close()

def main():
    """Test database operations."""
    print("🗄️ Billboard Database Test")
    print("=" * 30)
    
    # Test SQLite
    try:
        db = BillboardDatabase("sqlite", "test_billboard.db")
        print("✅ SQLite database initialized")
        
        # Test data
        test_entries = [
            {'rank': 1, 'title': 'Test Song', 'artist': 'Test Artist', 'scraped_at': datetime.now().isoformat()}
        ]
        test_scores = [
            {'artist': 'Test Artist', 'total_score': 100, 'chart_positions': [1], 'songs_count': 1}
        ]
        
        db.save_chart_data(test_entries, test_scores, '2025-01-01')
        print("✅ Test data saved")
        
        latest = db.get_latest_chart_data()
        print(f"✅ Retrieved {len(latest)} entries")
        
        top_artists = db.get_top_artists()
        print(f"✅ Retrieved {len(top_artists)} top artists")
        
        db.close()
        print("✅ Database closed")
        
        # Clean up test file
        os.remove("test_billboard.db")
        print("✅ Test database cleaned up")
        
    except Exception as e:
        print(f"❌ SQLite test failed: {e}")
    
    # Test BigQuery if available
    if BIGQUERY_AVAILABLE:
        try:
            # This would require actual BigQuery credentials
            print("\n🔍 BigQuery test skipped (requires credentials)")
        except Exception as e:
            print(f"❌ BigQuery test failed: {e}")
    else:
        print("\n🔍 BigQuery not available")

if __name__ == "__main__":
    main()
