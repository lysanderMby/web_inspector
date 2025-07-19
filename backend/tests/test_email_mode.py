"""
Test for email detection mode functionality.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.patterns import PatternMatcher
from webchecker.scraper import WebScraper


def test_email_mode_initialization():
    """Test email mode initialization."""
    print("🧪 Testing Email Mode Initialization")
    print("=" * 50)
    
    # Test email mode initialization
    matcher = PatternMatcher(email_mode=True)
    
    print(f"Email mode: {matcher.email_mode}")
    print(f"Pattern: {matcher.pattern}")
    
    # Should use email regex pattern
    expected_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if matcher.email_mode and matcher.pattern == expected_pattern:
        print("✅ Email mode initialization successful")
        return True
    else:
        print("❌ Email mode initialization failed")
        return False


def test_email_validation():
    """Test email validation functionality."""
    print("\n🧪 Testing Email Validation")
    print("=" * 50)
    
    matcher = PatternMatcher(email_mode=True)
    
    # Test cases: (email, expected_validity)
    test_cases = [
        ("test@example.com", True),
        ("user.name@domain.co.uk", True),
        ("support@voda.co", True),
        ("invalid-email", False),
        ("@example.com", False),
        ("test@", False),
        ("test..test@example.com", False),
        ("test@.example.com", False),
        ("test@example.", False),
        ("", False),
        ("test@example.com.", False),
        ("test@example.com..", False),
    ]
    
    passed = 0
    total = len(test_cases)
    
    for email, expected_valid in test_cases:
        is_valid = matcher.is_valid_email(email)
        status = "✅" if is_valid == expected_valid else "❌"
        print(f"{status} '{email}' -> Valid: {is_valid} (Expected: {expected_valid})")
        
        if is_valid == expected_valid:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    return passed == total


def test_email_extraction_with_validation():
    """Test email extraction with validation."""
    print("\n🧪 Testing Email Extraction with Validation")
    print("=" * 50)
    
    matcher = PatternMatcher(email_mode=True)
    
    # Test text with various email scenarios
    test_text = """
    Contact us at support@voda.co for help.
    Sales: sales@company.com
    Invalid: not-an-email
    Another: user@domain.org
    Bad: @example.com
    Good: admin@test.net
    """
    
    emails = matcher.find_emails_with_pages(test_text, "https://example.com")
    
    print("Found emails:")
    for email, page_url in emails:
        print(f"  - {email} (from {page_url})")
    
    # Should find valid emails only
    expected_emails = {"support@voda.co", "sales@company.com", "user@domain.org", "admin@test.net"}
    found_emails = {email for email, _ in emails}
    
    if found_emails == expected_emails:
        print(f"✅ Email extraction successful: {len(emails)} valid emails found")
        return True
    else:
        print(f"❌ Email extraction failed. Expected: {expected_emails}, Got: {found_emails}")
        return False


def test_html_cleaning_in_email_mode():
    """Test HTML cleaning in email mode."""
    print("\n🧪 Testing HTML Cleaning in Email Mode")
    print("=" * 50)
    
    matcher = PatternMatcher(email_mode=True)
    
    # Test cases with HTML artifacts
    test_cases = [
        ('<strong>support@voda.co</strong>', 'support@voda.co'),
        ('support@voda.co</a>', 'support@voda.co'),
        ('support@voda.co&nbsp;', 'support@voda.co'),
        ('support@voda.co‍', 'support@voda.co'),  # Zero-width space
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_text, expected_email in test_cases:
        emails = matcher.find_emails_with_pages(test_text, "https://example.com")
        actual_email = emails[0][0] if emails else "No results"
        
        status = "✅" if actual_email == expected_email else "❌"
        print(f"{status} Input: '{test_text}' -> '{actual_email}' (Expected: '{expected_email}')")
        
        if actual_email == expected_email:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    return passed == total


def test_email_mode_vs_regular_mode():
    """Test email mode vs regular pattern matching."""
    print("\n🧪 Testing Email Mode vs Regular Mode")
    print("=" * 50)
    
    test_text = "Contact support@voda.co and sales@company.com"
    
    # Email mode
    email_matcher = PatternMatcher(email_mode=True)
    email_results = email_matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    # Regular @ pattern mode
    regular_matcher = PatternMatcher(pattern="@")
    regular_results = regular_matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print("Email mode results:")
    for result in email_results:
        print(f"  - {result}")
    
    print("\nRegular @ pattern mode results:")
    for result in regular_results:
        print(f"  - {result}")
    
    # Email mode should find complete emails, regular mode should find @ symbols with context
    if len(email_results) == 2 and len(regular_results) == 2:
        print("✅ Both modes working correctly")
        return True
    else:
        print("❌ Mode comparison failed")
        return False


def main():
    """Run all email mode tests."""
    print("📧 Email Detection Mode Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_email_mode_initialization,
        test_email_validation,
        test_email_extraction_with_validation,
        test_html_cleaning_in_email_mode,
        test_email_mode_vs_regular_mode,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 Overall Results: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All email mode tests passed!")
        return 0
    else:
        print("❌ Some email mode tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 