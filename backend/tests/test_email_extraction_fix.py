"""
Test for email extraction fix to handle HTML artifacts properly.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.patterns import PatternMatcher


def test_problematic_email_case():
    """Test the specific problematic case reported by the user."""
    print("🧪 Testing Problematic Email Case")
    print("=" * 50)
    
    # The exact problematic text from the user
    test_text = 'This section of html should have been parsed as an email only _new"><strong>support@voda.co</strong></a>.</p><p>‍</p><h5><strong>Lodging a Complaint</strong'
    
    print(f"Input text: {test_text}")
    print()
    
    # Create pattern matcher for @ symbol
    matcher = PatternMatcher(pattern="@")
    
    # Test with both extract_before and extract_after
    results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
    
    print("Results:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result}")
    
    print()
    expected = "support@voda.co"
    actual = results[0] if results else "No results"
    
    if actual == expected:
        print(f"✅ SUCCESS: Got '{actual}' as expected")
        return True
    else:
        print(f"❌ FAILED: Expected '{expected}', got '{actual}'")
        return False


def test_various_html_scenarios():
    """Test various HTML scenarios that should be handled properly."""
    print("\n🧪 Testing Various HTML Scenarios")
    print("=" * 50)
    
    test_cases = [
        # Test case, expected result
        ('<strong>support@voda.co</strong>', 'support@voda.co'),
        ('support@voda.co</strong></a>', 'support@voda.co'),
        ('email: support@voda.co.', 'support@voda.co'),
        ('Contact support@voda.co for help', 'support@voda.co'),
        ('support@voda.co‍Lodging', 'support@voda.co'),  # Zero-width space
        ('support@voda.co.</p><p>‍</p><h5>', 'support@voda.co'),
        ('<a href="mailto:support@voda.co">support@voda.co</a>', 'support@voda.co'),
        ('support@voda.co&nbsp;', 'support@voda.co'),
        ('support@voda.co&amp;', 'support@voda.co'),
    ]
    
    matcher = PatternMatcher(pattern="@")
    passed = 0
    total = len(test_cases)
    
    for test_text, expected in test_cases:
        results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
        actual = results[0] if results else "No results"
        status = "✅" if actual == expected else "❌"
        print(f"{status} Input: '{test_text}' -> '{actual}' (Expected: '{expected}')")
        
        if actual == expected:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    return passed == total


def test_html_artifact_cleaning():
    """Test the HTML artifact cleaning functionality."""
    print("\n🧪 Testing HTML Artifact Cleaning")
    print("=" * 50)
    
    matcher = PatternMatcher(pattern="@")
    
    # Test cases with various HTML artifacts
    test_cases = [
        ('support@voda.co<strong>', 'support@voda.co'),
        ('<em>support@voda.co</em>', 'support@voda.co'),
        ('support@voda.co&nbsp;', 'support@voda.co'),
        ('support@voda.co&amp;', 'support@voda.co'),
        ('support@voda.co‍', 'support@voda.co'),  # Zero-width space
        ('support@voda.co\u200B', 'support@voda.co'),  # Zero-width space (unicode)
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_text, expected in test_cases:
        results = matcher.find_matches(test_text, extract_before=True, extract_after=True)
        actual = results[0] if results else "No results"
        status = "✅" if actual == expected else "❌"
        print(f"{status} Input: '{test_text}' -> '{actual}' (Expected: '{expected}')")
        
        if actual == expected:
            passed += 1
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    return passed == total


def main():
    """Run all email extraction fix tests."""
    print("🔧 Email Extraction Fix Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_problematic_email_case,
        test_various_html_scenarios,
        test_html_artifact_cleaning,
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
        print("🎉 All email extraction fix tests passed!")
        return 0
    else:
        print("❌ Some email extraction fix tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 