"""
Test script for improved text extraction functionality.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.patterns import PatternMatcher


def test_email_extraction():
    """Test email address extraction with context."""
    print("🧪 Testing Email Address Extraction")
    print("=" * 50)
    
    # Test text with various email scenarios
    test_text = """
    Contact us at john.doe@example.com for more information.
    Support email: support@company.co.uk
    Sales: sales@business.com.
    Invalid email: not-an-email
    Another one: user@domain.org,
    And this: admin@test.net!
    """
    
    # Create pattern matcher for @ symbol
    matcher = PatternMatcher(pattern="@")
    
    # Test with both extract_before and extract_after
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print("Found email addresses:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
    
    print(f"\nTotal: {len(results)} email addresses found")
    print()


def test_trademark_extraction():
    """Test trademark symbol extraction with context."""
    print("🧪 Testing Trademark Symbol Extraction")
    print("=" * 50)
    
    # Test text with various trademark scenarios
    test_text = """
    Our product is called SuperWidget™ and it's amazing.
    The brand name is MegaCorp® and it's registered.
    Copyright © 2024 by Example Company.
    Another trademark: CoolBrand™.
    Invalid: Just some text.
    Another one: TestBrand®.
    """
    
    # Create pattern matcher for trademark symbols
    matcher = PatternMatcher(pattern="™")
    
    # Test with both extract_before and extract_after
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print("Found trademark symbols:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
    
    print(f"\nTotal: {len(results)} trademark symbols found")
    print()


def test_copyright_extraction():
    """Test copyright symbol extraction with context."""
    print("🧪 Testing Copyright Symbol Extraction")
    print("=" * 50)
    
    # Test text with copyright scenarios
    test_text = """
    Copyright © 2024 Example Company. All rights reserved.
    © 2024 Another Company.
    This is some text with © symbol.
    Copyright © 2024 by Test Corp.
    """
    
    # Create pattern matcher for copyright symbol
    matcher = PatternMatcher(pattern="©")
    
    # Test with both extract_before and extract_after
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print("Found copyright symbols:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
    
    print(f"\nTotal: {len(results)} copyright symbols found")
    print()


def test_custom_pattern():
    """Test custom regex pattern matching."""
    print("🧪 Testing Custom Regex Pattern")
    print("=" * 50)
    
    # Test text with phone numbers
    test_text = """
    Call us at 555-123-4567 for support.
    Alternative: (555) 987-6543
    International: +1-555-123-4567
    """
    
    # Create pattern matcher for phone numbers
    matcher = PatternMatcher(custom_pattern=r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    
    # Test with context extraction
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print("Found phone numbers:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
    
    print(f"\nTotal: {len(results)} phone numbers found")
    print()


def test_boundary_detection():
    """Test smart boundary detection."""
    print("🧪 Testing Smart Boundary Detection")
    print("=" * 50)
    
    # Test text with various boundary scenarios
    test_text = """
    Email: test@example.com
    Another: user@domain.org.
    Third: admin@test.net!
    Fourth: support@company.co.uk,
    Fifth: sales@business.com
    """
    
    # Create pattern matcher for @ symbol
    matcher = PatternMatcher(pattern="@")
    
    # Test with both extract_before and extract_after
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print("Found email addresses with smart boundaries:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
    
    print(f"\nTotal: {len(results)} email addresses found")
    print()


def main():
    """Run all tests."""
    print("🔍 WebChecker Text Extraction Tests")
    print("=" * 60)
    print()
    
    test_email_extraction()
    test_trademark_extraction()
    test_copyright_extraction()
    test_custom_pattern()
    test_boundary_detection()
    
    print("✅ All tests completed!")


if __name__ == "__main__":
    main() 