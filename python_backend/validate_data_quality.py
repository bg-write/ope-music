#!/usr/bin/env python3
"""
Billboard Scraper Validation Test Suite

This test suite validates the quality and accuracy of scraped Billboard Hot 100 data.
Run this after scraping to ensure data quality meets standards.

Usage:
    python test_billboard_validation.py
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

class BillboardDataValidator:
    """Validates Billboard scraped data for quality and accuracy."""
    
    def __init__(self, data_file='data_output/billboard_chart_data.json'):
        """Initialize validator with data file path."""
        self.data_file = data_file
        self.data = None
        self.chart_entries = []
        self.test_results = []
        
    def load_data(self):
        """Load the scraped Billboard data."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.chart_entries = self.data.get('chart_entries', [])
            return True
        except FileNotFoundError:
            print(f"❌ Data file not found: {self.data_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in data file: {e}")
            return False
    
    def run_test(self, test_name, test_func):
        """Run a single test and record results."""
        try:
            result = test_func()
            self.test_results.append((test_name, result))
            status = "✅" if result else "❌"
            print(f"{status} {test_name}")
            return result
        except Exception as e:
            print(f"❌ {test_name} - Error: {e}")
            self.test_results.append((test_name, False))
            return False
    
    def test_data_completeness(self):
        """Test 1: Verify data completeness."""
        print("\n📊 TEST 1: DATA COMPLETENESS")
        print("-" * 40)
        
        # Check total entries
        total_entries = len(self.chart_entries)
        test1a = self.run_test("Total entries = 100", lambda: total_entries == 100)
        
        # Check required fields
        required_fields = ['rank', 'title', 'artist', 'chart_date', 'scraped_at']
        missing_fields = 0
        
        for entry in self.chart_entries:
            for field in required_fields:
                if field not in entry or not entry[field]:
                    missing_fields += 1
        
        test1b = self.run_test("All required fields present", lambda: missing_fields == 0)
        
        return test1a and test1b
    
    def test_rank_validation(self):
        """Test 2: Validate rank structure."""
        print("\n🏆 TEST 2: RANK VALIDATION")
        print("-" * 40)
        
        ranks = [entry['rank'] for entry in self.chart_entries]
        expected_ranks = list(range(1, 101))
        
        # Check all ranks present
        test2a = self.run_test("All ranks 1-100 present", lambda: sorted(ranks) == expected_ranks)
        
        # Check no duplicate ranks
        duplicate_ranks = [r for r in ranks if ranks.count(r) > 1]
        test2b = self.run_test("No duplicate ranks", lambda: len(duplicate_ranks) == 0)
        
        return test2a and test2b
    
    def test_data_quality(self):
        """Test 3: Check data quality."""
        print("\n📝 TEST 3: DATA QUALITY")
        print("-" * 40)
        
        # Check for empty values
        empty_titles = [e for e in self.chart_entries if not e.get('title', '').strip()]
        empty_artists = [e for e in self.chart_entries if not e.get('artist', '').strip()]
        
        test3a = self.run_test("No empty titles", lambda: len(empty_titles) == 0)
        test3b = self.run_test("No empty artists", lambda: len(empty_artists) == 0)
        
        # Check for HTML artifacts
        html_patterns = [
            r'<[^>]+>',  # HTML tags
            r'&[a-z]+;',  # HTML entities
            r'billboard hot 100™?',  # Billboard text
            r'expand|menu|search|login',  # Navigation elements
            r'share chart|facebook|twitter|instagram'  # Social media elements
        ]
        
        artifacts_found = 0
        for entry in self.chart_entries:
            title = entry.get('title', '')
            artist = entry.get('artist', '')
            
            for pattern in html_patterns:
                if re.search(pattern, title, re.IGNORECASE) or re.search(pattern, artist, re.IGNORECASE):
                    artifacts_found += 1
                    break
        
        test3c = self.run_test("No HTML artifacts", lambda: artifacts_found == 0)
        
        return test3a and test3b and test3c
    
    def test_artist_patterns(self):
        """Test 4: Validate artist name patterns."""
        print("\n🎤 TEST 4: ARTIST NAME PATTERNS")
        print("-" * 40)
        
        # Count collaboration patterns
        featuring_count = len([e for e in self.chart_entries if 'featuring' in e.get('artist', '').lower()])
        and_count = len([e for e in self.chart_entries if ' & ' in e.get('artist', '')])
        with_count = len([e for e in self.chart_entries if ' with ' in e.get('artist', '').lower()])
        
        # Check for reasonable collaboration counts
        test4a = self.run_test("Reasonable featuring count (5-15)", lambda: 5 <= featuring_count <= 15)
        test4b = self.run_test("Reasonable collaboration count (10-30)", lambda: 10 <= and_count <= 30)
        
        # Check for known major artists
        known_artists = [
            'Morgan Wallen', 'Justin Bieber', 'Billie Eilish', 'Drake', 'Taylor Swift',
            'Post Malone', 'SZA', 'Kendrick Lamar', 'Bruno Mars', 'Lady Gaga'
        ]
        
        found_artists = []
        for artist in known_artists:
            if any(artist.lower() in entry.get('artist', '').lower() for entry in self.chart_entries):
                found_artists.append(artist)
        
        test4c = self.run_test(f"Found {len(found_artists)}/{len(known_artists)} major artists", lambda: len(found_artists) >= 5)
        
        return test4a and test4b and test4c
    
    def test_date_consistency(self):
        """Test 5: Check date consistency."""
        print("\n📅 TEST 5: DATE CONSISTENCY")
        print("-" * 40)
        
        chart_dates = [entry.get('chart_date', '') for entry in self.chart_entries]
        unique_dates = set(chart_dates)
        
        test5a = self.run_test("Consistent chart date", lambda: len(unique_dates) == 1)
        
        # Check date format
        date_format_valid = True
        for date_str in unique_dates:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                date_format_valid = False
                break
        
        test5b = self.run_test("Valid date format", lambda: date_format_valid)
        
        return test5a and test5b
    
    def test_data_distribution(self):
        """Test 6: Check data distribution."""
        print("\n📈 TEST 6: DATA DISTRIBUTION")
        print("-" * 40)
        
        # Check title lengths
        title_lengths = [len(entry.get('title', '')) for entry in self.chart_entries]
        avg_title_length = sum(title_lengths) / len(title_lengths)
        
        test6a = self.run_test("Reasonable title length (5-25)", lambda: 5 <= avg_title_length <= 25)
        
        # Check artist lengths
        artist_lengths = [len(entry.get('artist', '')) for entry in self.chart_entries]
        avg_artist_length = sum(artist_lengths) / len(artist_lengths)
        
        test6b = self.run_test("Reasonable artist length (10-40)", lambda: 10 <= avg_artist_length <= 40)
        
        return test6a and test6b
    
    def run_all_tests(self):
        """Run all validation tests."""
        print("🧪 BILLBOARD DATA VALIDATION SUITE")
        print("=" * 60)
        
        if not self.load_data():
            return False
        
        print(f"📁 Data file: {self.data_file}")
        print(f"📊 Chart entries: {len(self.chart_entries)}")
        
        # Run all tests
        tests = [
            self.test_data_completeness,
            self.test_rank_validation,
            self.test_data_quality,
            self.test_artist_patterns,
            self.test_date_consistency,
            self.test_data_distribution
        ]
        
        for test in tests:
            test()
        
        # Summary
        print("\n" + "=" * 60)
        print("📋 VALIDATION SUMMARY")
        print("=" * 60)
        
        passed_tests = sum(1 for _, result in self.test_results if result)
        total_tests = len(self.test_results)
        success_rate = (passed_tests / total_tests) * 100
        
        print(f"\nTests Passed: {passed_tests}/{total_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! Data quality is excellent!")
            return True
        else:
            print(f"\n⚠️  {total_tests - passed_tests} tests failed. Review the details above.")
            return False

def main():
    """Main function to run validation tests."""
    validator = BillboardDataValidator()
    success = validator.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
