#!/usr/bin/env python3
"""
Markdown to JSON Converter for OPE! Music Reviews
Converts songs.md to structured JSON format for Python backend and Netlify Functions
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
    Convert songs.md file to JSON format for Python backend
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
        
        return reviews
        
    except Exception as e:
        print(f"❌ Error converting markdown to JSON: {e}")
        return None

def generate_netlify_function_data(reviews):
    """
    Generate the exact data structure needed for Netlify Functions
    """
    return {
        "reviews": reviews,
        "pagination": {
            "page": 1,
            "per_page": len(reviews),
            "total": len(reviews),
            "pages": 1
        }
    }

def update_netlify_function(reviews, function_file_path):
    """
    Update the Netlify Function with new review data
    """
    try:
        # Read the current function file
        with open(function_file_path, 'r', encoding='utf-8') as f:
            function_content = f.read()
        
        # Generate the new data
        new_data = generate_netlify_function_data(reviews)
        
        # Convert to JavaScript format
        js_data = json.dumps(new_data, indent=2, ensure_ascii=False)
        
        # Find and replace the reviewsData section
        # Look for the pattern: const reviewsData = { ... };
        pattern = r'(const reviewsData = )\{[^}]*\};'
        replacement = f'\\1{js_data};'
        
        new_function_content = re.sub(pattern, replacement, function_content, flags=re.DOTALL)
        
        if new_function_content == function_content:
            # If no replacement was made, try a different approach
            # Look for the start of the reviewsData object
            start_pattern = r'(const reviewsData = )\{'
            if re.search(start_pattern, function_content):
                # Find the start and end of the object
                start_match = re.search(start_pattern, function_content)
                start_pos = start_match.start()
                
                # Find the closing brace and semicolon
                brace_count = 0
                end_pos = start_pos
                for i, char in enumerate(function_content[start_pos:], start_pos):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            end_pos = i + 1  # Include the semicolon
                            break
                
                # Replace the entire object
                new_function_content = (
                    function_content[:start_pos] + 
                    f'const reviewsData = {js_data};' +
                    function_content[end_pos:]
                )
        
        # Write the updated function
        with open(function_file_path, 'w', encoding='utf-8') as f:
            f.write(new_function_content)
        
        print(f"✅ Successfully updated Netlify Function: {function_file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating Netlify Function: {e}")
        return False

def main():
    """
    Main function to run the conversion
    """
    # Get the project root directory (two levels up from python_backend/)
    project_root = Path(__file__).parent.parent
    md_file = project_root / "content" / "songs.md"
    output_file = Path(__file__).parent / "data" / "reviews.json"
    netlify_function_file = project_root / "netlify_functions" / "reviews.js"
    
    print("🎵 OPE! Markdown to JSON Converter")
    print("=" * 40)
    print(f"📖 Input file: {md_file}")
    print(f"📤 Output file: {output_file}")
    print(f"🚀 Netlify Function: {netlify_function_file}")
    print()
    
    # Check if input file exists
    if not md_file.exists():
        print(f"❌ Input file not found: {md_file}")
        return
    
    # Convert the file
    reviews = convert_songs_md_to_json(md_file, output_file)
    
    if reviews:
        print("\n🎉 Conversion completed successfully!")
        
        # Update Netlify Function if it exists
        if netlify_function_file.exists():
            print("\n🚀 Updating Netlify Function...")
            if update_netlify_function(reviews, netlify_function_file):
                print("✅ Netlify Function updated successfully!")
                print("📝 Next steps:")
                print("   1. git add netlify_functions/reviews.js")
                print("   2. git commit -m 'Update reviews from Markdown'")
                print("   3. git push")
                print("   4. Wait 2-5 minutes for deployment")
            else:
                print("❌ Failed to update Netlify Function")
        else:
            print(f"⚠️  Netlify Function not found: {netlify_function_file}")
            print("   The JSON file is ready for manual integration")
    else:
        print("\n💥 Conversion failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
