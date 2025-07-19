"""
Test script for URL normalization and validation functionality.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from webchecker.utils import normalize_url, validate_url, extract_domain, is_same_domain


def test_url_normalization():
    """Test URL normalization functionality."""
    print("🧪 Testing URL Normalization")
    print("=" * 50)
    
    test_cases = [
        # Input URL, Expected normalized URL
        ("example.com", "https://example.com"),
        ("www.example.com", "https://www.example.com"),
        ("http://example.com", "http://example.com"),
        ("https://example.com", "https://example.com"),
        ("  example.com  ", "https://example.com"),
        ("subdomain.example.com", "https://subdomain.example.com"),
        ("example.com/path", "https://example.com/path"),
        ("example.com/path?param=value", "https://example.com/path?param=value"),
        ("example.com/path#fragment", "https://example.com/path#fragment"),
    ]
    
    for input_url, expected in test_cases:
        result = normalize_url(input_url)
        status = "✅" if result == expected else "❌"
        print(f"{status} Input: '{input_url}' -> Output: '{result}' (Expected: '{expected}')")
    
    print()


def test_url_validation():
    """Test URL validation functionality."""
    print("🧪 Testing URL Validation")
    print("=" * 50)
    
    test_cases = [
        # URL, Expected validity
        ("https://example.com", True),
        ("http://example.com", True),
        ("https://www.example.com", True),
        ("https://example.com/path", True),
        ("https://example.com/path?param=value", True),
        ("https://subdomain.example.com", True),
        ("example.com", False),  # No protocol
        ("not-a-url", False),
        ("ftp://example.com", True),  # Other protocols are valid
        ("", False),
        ("   ", False),
    ]
    
    for url, expected_valid in test_cases:
        result = validate_url(url)
        status = "✅" if result == expected_valid else "❌"
        print(f"{status} URL: '{url}' -> Valid: {result} (Expected: {expected_valid})")
    
    print()


def test_domain_extraction():
    """Test domain extraction functionality."""
    print("🧪 Testing Domain Extraction")
    print("=" * 50)
    
    test_cases = [
        # URL, Expected domain
        ("https://example.com", "example.com"),
        ("https://www.example.com", "www.example.com"),
        ("http://subdomain.example.com", "subdomain.example.com"),
        ("https://example.com/path", "example.com"),
        ("https://example.com/path?param=value", "example.com"),
        ("https://example.com/path#fragment", "example.com"),
        ("example.com", None),  # Invalid URL
        ("not-a-url", None),
        ("", None),
    ]
    
    for url, expected_domain in test_cases:
        result = extract_domain(url)
        status = "✅" if result == expected_domain else "❌"
        print(f"{status} URL: '{url}' -> Domain: '{result}' (Expected: '{expected_domain}')")
    
    print()


def test_same_domain_check():
    """Test same domain checking functionality."""
    print("🧪 Testing Same Domain Check")
    print("=" * 50)
    
    test_cases = [
        # URL1, URL2, Expected same domain
        ("https://example.com", "https://example.com", True),
        ("https://example.com", "https://www.example.com", False),
        ("https://example.com", "https://subdomain.example.com", False),
        ("https://example.com/path1", "https://example.com/path2", True),
        ("https://example.com", "http://example.com", True),  # Protocol doesn't matter
        ("https://example.com", "https://other.com", False),
        ("example.com", "https://example.com", False),  # Invalid URL
        ("", "https://example.com", False),
    ]
    
    for url1, url2, expected_same in test_cases:
        result = is_same_domain(url1, url2)
        status = "✅" if result == expected_same else "❌"
        print(f"{status} '{url1}' vs '{url2}' -> Same domain: {result} (Expected: {expected_same})")
    
    print()


def test_integration():
    """Test integration of URL functions."""
    print("🧪 Testing URL Functions Integration")
    print("=" * 50)
    
    test_urls = [
        "example.com",
        "www.example.com",
        "https://example.com",
        "http://subdomain.example.com",
    ]
    
    for url in test_urls:
        print(f"\nTesting URL: '{url}'")
        
        # Test normalization
        normalized = normalize_url(url)
        print(f"  Normalized: '{normalized}'")
        
        # Test validation
        is_valid = validate_url(normalized)
        print(f"  Valid: {is_valid}")
        
        # Test domain extraction
        domain = extract_domain(normalized)
        print(f"  Domain: '{domain}'")
        
        # Test same domain check with itself
        same_domain = is_same_domain(normalized, normalized)
        print(f"  Same as itself: {same_domain}")
    
    print()


def main():
    """Run all URL utility tests."""
    print("🔗 WebChecker URL Utility Tests")
    print("=" * 60)
    print()
    
    test_url_normalization()
    test_url_validation()
    test_domain_extraction()
    test_same_domain_check()
    test_integration()
    
    print("✅ All URL utility tests completed!")


if __name__ == "__main__":
    main() 