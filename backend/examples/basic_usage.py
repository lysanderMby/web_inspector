"""
Basic usage example for WebChecker.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.scraper import WebScraper
from webchecker.patterns import PatternMatcher
from webchecker.utils import setup_logging


def example_find_trademarks():
    """Example: Find trademark symbols on a website."""
    print("🔍 Example: Finding Trademark Symbols")
    print("=" * 50)
    
    # Create pattern matcher for trademark symbol
    matcher = PatternMatcher(pattern="™")
    
    # Create scraper
    scraper = WebScraper(
        max_pages=10,
        max_depth=2,
        timeout=10,
        follow_sitemap=False
    )
    
    try:
        # Scrape website for trademarks
        results = scraper.scrape_site(
            "https://example.com",  # Replace with actual website
            matcher,
            extract_before=True,
            extract_after=True
        )
        
        print(f"Found {len(results)} trademark matches:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()


def example_find_emails():
    """Example: Find email addresses on a website."""
    print("\n📧 Example: Finding Email Addresses")
    print("=" * 50)
    
    # Create pattern matcher for @ symbol
    matcher = PatternMatcher(pattern="@")
    
    # Create scraper
    scraper = WebScraper(
        max_pages=15,
        max_depth=2,
        timeout=10,
        follow_sitemap=True
    )
    
    try:
        # Scrape website for emails
        results = scraper.scrape_site(
            "https://example.com",  # Replace with actual website
            matcher,
            extract_before=True,
            extract_after=True
        )
        
        print(f"Found {len(results)} email matches:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()


def example_custom_regex():
    """Example: Use custom regex pattern."""
    print("\n🎯 Example: Custom Regex Pattern")
    print("=" * 50)
    
    # Create pattern matcher with custom regex for phone numbers
    matcher = PatternMatcher(custom_pattern=r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    
    # Create scraper
    scraper = WebScraper(
        max_pages=5,
        max_depth=1,
        timeout=10,
        follow_sitemap=False
    )
    
    try:
        # Scrape website for phone numbers
        results = scraper.scrape_site(
            "https://example.com",  # Replace with actual website
            matcher,
            extract_before=True,
            extract_after=True
        )
        
        print(f"Found {len(results)} phone number matches:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()


def example_save_results():
    """Example: Save results to file."""
    print("\n💾 Example: Saving Results to File")
    print("=" * 50)
    
    # Create pattern matcher for copyright symbols
    matcher = PatternMatcher(pattern="©")
    
    # Create scraper
    scraper = WebScraper(
        max_pages=20,
        max_depth=2,
        timeout=10,
        follow_sitemap=True
    )
    
    try:
        # Scrape website for copyright symbols
        results = scraper.scrape_site(
            "https://example.com",  # Replace with actual website
            matcher,
            extract_before=True,
            extract_after=True
        )
        
        # Save results to file
        if results:
            filename = "copyright_results.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(result + '\n')
            print(f"Saved {len(results)} results to {filename}")
        else:
            print("No results found")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scraper.close()


def main():
    """Run all examples."""
    print("🚀 WebChecker Basic Usage Examples")
    print("=" * 60)
    print()
    
    # Setup logging
    logger = setup_logging(verbose=False)
    
    example_find_trademarks()
    example_find_emails()
    example_custom_regex()
    example_save_results()
    
    print("\n✅ All examples completed!")
    print("\nNote: Replace 'https://example.com' with actual websites to test.")


if __name__ == "__main__":
    main() 