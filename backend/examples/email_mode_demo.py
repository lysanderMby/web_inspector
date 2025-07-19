#!/usr/bin/env python3
"""
Demo script for email detection mode functionality.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.patterns import PatternMatcher
from webchecker.scraper import WebScraper


def demo_email_mode():
    """Demonstrate email detection mode functionality."""
    print("📧 Email Detection Mode Demo")
    print("=" * 50)
    
    # Create pattern matcher in email mode
    print("1. Creating pattern matcher in email mode...")
    matcher = PatternMatcher(email_mode=True)
    print(f"   Email mode: {matcher.email_mode}")
    print(f"   Pattern: {matcher.pattern}")
    print()
    
    # Test email validation
    print("2. Testing email validation...")
    test_emails = [
        "valid@example.com",
        "user.name@domain.co.uk", 
        "support@voda.co",
        "invalid-email",
        "@example.com",
        "test@",
        "test..test@example.com"
    ]
    
    for email in test_emails:
        is_valid = matcher.is_valid_email(email)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {email}")
    print()
    
    # Test email extraction with HTML artifacts
    print("3. Testing email extraction with HTML artifacts...")
    test_text = """
    Contact us at <strong>support@voda.co</strong> for help.
    Sales: sales@company.com
    Support: <a href="mailto:help@example.org">help@example.org</a>
    Invalid: not-an-email
    Another: user@domain.org
    """
    
    emails = matcher.find_emails_with_pages(test_text, "https://example.com")
    
    print("   Found emails:")
    for email, page_url in emails:
        print(f"   📧 {email} (from {page_url})")
    print()
    
    # Test scraping simulation
    print("4. Simulating email scraping results...")
    scraper = WebScraper(max_pages=5, max_depth=2)
    
    # Simulate results from multiple pages
    simulated_results = [
        "support@voda.co: https://example.com/contact, https://example.com/about",
        "sales@company.com: https://example.com/contact",
        "help@example.org: https://example.com/support, https://example.com/help",
        "admin@test.net: https://example.com/admin"
    ]
    
    print("   Grouped email results:")
    for result in simulated_results:
        print(f"   {result}")
    print()
    
    print("🎉 Email detection mode demo completed!")
    print("\nKey features demonstrated:")
    print("   • Automatic email pattern detection")
    print("   • Email validation with format checking")
    print("   • HTML artifact cleaning")
    print("   • Grouped results by email address")
    print("   • Page location tracking")


def demo_comparison():
    """Compare email mode vs regular @ pattern mode."""
    print("\n🔄 Email Mode vs Regular Mode Comparison")
    print("=" * 50)
    
    test_text = "Contact support@voda.co and sales@company.com for help"
    
    print("Test text:", test_text)
    print()
    
    # Email mode
    print("Email Mode Results:")
    email_matcher = PatternMatcher(email_mode=True)
    email_results = email_matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    for i, result in enumerate(email_results, 1):
        print(f"   {i}. {result}")
    print()
    
    # Regular @ pattern mode
    print("Regular @ Pattern Mode Results:")
    regular_matcher = PatternMatcher(pattern="@")
    regular_results = regular_matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    for i, result in enumerate(regular_results, 1):
        print(f"   {i}. {result}")
    print()
    
    print("Key differences:")
    print("   • Email mode: Finds complete, validated email addresses")
    print("   • Regular mode: Finds @ symbols with surrounding context")
    print("   • Email mode: Better for email harvesting")
    print("   • Regular mode: Better for general pattern matching")


if __name__ == "__main__":
    demo_email_mode()
    demo_comparison() 