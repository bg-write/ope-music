#!/usr/bin/env python3
"""
Markdown to JSON Converter for OPE! Music Reviews
Converts songs.md to structured JSON format for Python backend
"""

import re
import json
import os
from datetime import datetime
from pathlib import Path

def parse_song_review(markdown_text):
    """
    Parse a single song review from markdown format
    Returns a dictionary with structured data
    """
    # Extract song title and artist from the header
    header_match = re.match(r'## (.+?) - "(.+?)"', markdown_text.strip())
    if not header_match:
        return None
    
    artist = header_match.group(1).strip()
    song_title = header_match.group(2).strip()
    
    # Extract other fields using regex patterns
    date_match = re.search(r'\*\*Date:\*\* (.+)', markdown_text)
    rating_match = re.search(r'\*\*Rating:\*\* (.+)', markdown_text)
    description_match = re.search(r'\*\*Description:\*\* (.+)', markdown_text)
    listen_match = re.search(r'\*\*Listen:\*\* (.+)', markdown_text)
    
    # Create the review object with SQL-friendly field names
    review = {
        "song_title": song_title,
        "song_artist": artist,
        "review_date": date_match.group(1).strip() if date_match else "",
        "review_score": rating_match.group(1).strip() if rating_match else "",
        "review_text": description_match.group(1).strip() if description_match else "",
        "song_url": listen_match.group(1).strip() if listen_match else "",
        "review_id": f"{artist.lower().replace(' ', '-')}-{song_title.lower().replace(' ', '-').replace('"', '').replace(',', '')}-song-review"
    }
    
    return review

def convert_songs_md_to_json(md_file_path, output_file_path):
    """
    Convert songs.md file to JSON format
    """
    try:
        # Read the markdown file
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into individual reviews (separated by ## headers)
        reviews = []
        sections = content.split('## ')[1:]  # Skip the first empty section
        
        for section in sections:
            if section.strip():
                # Add back the ## for parsing
                section_with_header = f"## {section.strip()}"
                review = parse_song_review(section_with_header)
                if review:
                    reviews.append(review)
        
        # Create the final JSON structure
        output_data = {
            "metadata": {
                "conversion_date": datetime.now().isoformat(),
                "source_file": "content/songs.md",
                "total_reviews": len(reviews)
            },
            "reviews": reviews
        }
        
        # Write to JSON file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully converted {len(reviews)} reviews to JSON")
        print(f"📁 Output saved to: {output_file_path}")
        
        # Print a sample review for verification
        if reviews:
            print(f"\n📝 Sample review:")
            print(f"   Artist: {reviews[0]['song_artist']}")
            print(f"   Song: {reviews[0]['song_title']}")
            print(f"   ID: {reviews[0]['review_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting markdown to JSON: {e}")
        return False

def main():
    """
    Main function to run the conversion
    """
    # Get the project root directory (two levels up from python_backend/)
    project_root = Path(__file__).parent.parent
    md_file = project_root / "content" / "songs.md"
    output_file = Path(__file__).parent / "data" / "reviews.json"
    
    print("🎵 OPE! Markdown to JSON Converter")
    print("=" * 40)
    print(f"📖 Input file: {md_file}")
    print(f"📤 Output file: {output_file}")
    print()
    
    # Check if input file exists
    if not md_file.exists():
        print(f"❌ Input file not found: {md_file}")
        return
    
    # Convert the file
    success = convert_songs_md_to_json(md_file, output_file)
    
    if success:
        print("\n🎉 Conversion completed successfully!")
        print("🚀 Ready for the next phase: Flask API development")
    else:
        print("\n💥 Conversion failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
