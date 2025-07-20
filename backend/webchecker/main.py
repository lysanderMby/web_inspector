"""
Command-line interface for WebChecker.
"""

import argparse
import sys
from .scraper import WebScraper
from .patterns import PatternMatcher
from .utils import setup_logging, validate_url, normalize_url


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="WebChecker - Find specific characters and patterns on websites",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Find trademark symbols on a website
  webchecker https://example.com --pattern "™"

  # Find email addresses
  webchecker https://example.com --pattern "@" --extract-before --extract-after

  # Use custom regex pattern
  webchecker https://example.com --custom-pattern r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b'

  # Limit pages and depth
  webchecker https://example.com --pattern "©" --max-pages 10 --max-depth 2

  # Exclude certain file types
  webchecker https://example.com --pattern "®" --exclude-extensions .pdf .doc

  # Save results to file
  webchecker https://example.com --pattern "™" --output results.txt
        """
    )
    
    # Required arguments
    parser.add_argument(
        'url',
        help='URL of the website to scrape'
    )
    
    # Pattern arguments (mutually exclusive)
    pattern_group = parser.add_mutually_exclusive_group(required=True)
    pattern_group.add_argument(
        '--pattern',
        help='Character or string to search for (e.g., "™", "@", "©")'
    )
    pattern_group.add_argument(
        '--custom-pattern',
        help='Custom regex pattern to search for'
    )
    pattern_group.add_argument(
        '--email-mode',
        action='store_true',
        help='Enable email detection mode with validation and grouping'
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        help='Output file to save results (default: print to console)'
    )
    
    # Extraction options
    parser.add_argument(
        '--extract-before',
        action='store_true',
        help='Extract text before the matched pattern'
    )
    parser.add_argument(
        '--extract-after',
        action='store_true',
        help='Extract text after the matched pattern'
    )
    
    # Scraping options
    parser.add_argument(
        '--max-pages',
        type=int,
        default=50,
        help='Maximum number of pages to scrape (default: 50)'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum link depth to follow (default: 3)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds (default: 1.0)'
    )
    
    # Sitemap options
    parser.add_argument(
        '--follow-sitemap',
        action='store_true',
        help='Follow sitemap URLs for more comprehensive scraping'
    )
    parser.add_argument(
        '--no-sitemap',
        action='store_true',
        help='Disable sitemap following (default behavior)'
    )
    
    # File filtering
    parser.add_argument(
        '--exclude-extensions',
        nargs='+',
        help='File extensions to exclude (e.g., .pdf .doc .jpg)'
    )
    
    # Verbosity
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging(verbose=args.verbose)
    
    try:
        # Normalize URL
        url = normalize_url(args.url)
        
        # Validate URL
        if not validate_url(url):
            logger.error(f"Invalid URL: {args.url}")
            sys.exit(1)
        
        # Create pattern matcher
        if args.email_mode:
            pattern_matcher = PatternMatcher(email_mode=True)
        elif args.custom_pattern:
            pattern_matcher = PatternMatcher(custom_pattern=args.custom_pattern)
        else:
            pattern_matcher = PatternMatcher(pattern=args.pattern)
        
        # Create scraper
        scraper = WebScraper(
            max_pages=args.max_pages,
            max_depth=args.max_depth,
            timeout=args.timeout,
            delay=args.delay,
            follow_sitemap=args.follow_sitemap and not args.no_sitemap,
            exclude_extensions=args.exclude_extensions
        )
        
        logger.info(f"Starting scrape of {url}")
        if args.email_mode:
            logger.info("Email detection mode enabled")
        else:
            logger.info(f"Pattern: {pattern_matcher.pattern}")
        logger.info(f"Max pages: {args.max_pages}, Max depth: {args.max_depth}")
        
        # Perform scraping
        results = scraper.scrape_site(
            url,
            pattern_matcher,
            extract_before=args.extract_before,
            extract_after=args.extract_after,
            email_mode=args.email_mode
        )
        
        # Output results
        if results:
            logger.info(f"Found {len(results)} matches")
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    for result in results:
                        f.write(result + '\n')
                logger.info(f"Results saved to {args.output}")
            else:
                for result in results:
                    print(result)
        else:
            logger.info("No matches found")
        
        scraper.close()
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 