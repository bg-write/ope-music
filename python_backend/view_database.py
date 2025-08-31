#!/usr/bin/env python3
"""
Database Viewer - Export SQLite database to readable formats
"""

import sqlite3
import pandas as pd
import json
from pathlib import Path

def export_database_to_csv():
    """Export all database tables to CSV files for easy viewing"""
    
    db_path = Path('billboard.db')
    if not db_path.exists():
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Get all table names
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Found {len(tables)} tables: {', '.join(tables)}")
        
        # Export each table to CSV
        for table in tables:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            csv_path = f"database_export_{table}.csv"
            df.to_csv(csv_path, index=False)
            print(f"✅ Exported {table} ({len(df)} rows) → {csv_path}")
        
        # Create a summary report
        print("\n📋 DATABASE SUMMARY:")
        print("=" * 50)
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📊 {table}: {count} rows")
            
            # Show sample data
            cursor.execute(f"SELECT * FROM {table} LIMIT 3")
            sample = cursor.fetchall()
            if sample:
                print(f"   Sample: {sample[0]}")
        
    finally:
        conn.close()

def view_database_interactive():
    """Interactive database viewer"""
    
    db_path = Path('billboard.db')
    if not db_path.exists():
        print("❌ Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        while True:
            print("\n🔍 DATABASE VIEWER")
            print("=" * 30)
            print("1. View all tables")
            print("2. View chart_entries (top 10)")
            print("3. View artist_scores (top 10)")
            print("4. Custom SQL query")
            print("5. Export to CSV")
            print("6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print(f"\n📊 Tables: {[t[0] for t in tables]}")
                
            elif choice == '2':
                cursor.execute("SELECT rank, title, artist FROM chart_entries ORDER BY rank LIMIT 10")
                entries = cursor.fetchall()
                print("\n📈 Top 10 Chart Entries:")
                for rank, title, artist in entries:
                    print(f"  {rank:2d}. {title} - {artist}")
                    
            elif choice == '3':
                cursor.execute("SELECT artist, total_score, songs_count FROM artist_scores ORDER BY total_score DESC LIMIT 10")
                artists = cursor.fetchall()
                print("\n🏆 Top 10 Artists:")
                for artist, score, songs in artists:
                    print(f"  {score:3d} pts - {artist} ({songs} songs)")
                    
            elif choice == '4':
                query = input("Enter SQL query: ").strip()
                try:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    print(f"\n📊 Results ({len(results)} rows):")
                    for row in results:
                        print(f"  {row}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    
            elif choice == '5':
                export_database_to_csv()
                
            elif choice == '6':
                break
                
            else:
                print("❌ Invalid choice")
                
    finally:
        conn.close()

if __name__ == "__main__":
    print("🗄️  Billboard Database Viewer")
    print("=" * 40)
    
    # Quick export
    export_database_to_csv()
    
    # Ask if user wants interactive mode
    if input("\n🔍 Open interactive viewer? (y/n): ").lower() == 'y':
        view_database_interactive()
