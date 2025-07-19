"""
Utility functions for the WebChecker application.
"""

import logging
import re
from typing import Optional
from urllib.parse import urlparse


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Setup logging configuration.
    
    Args:
        verbose: Whether to enable verbose logging
        
    Returns:
        Configured logger instance
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set specific logger levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


def validate_url(url: str) -> bool:
    """
    Validate if a string is a proper URL.
    
    Args:
        url: The URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def clean_text(text: str) -> str:
    """
    Clean and normalize text content.
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove common HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL.
    
    Args:
        url: The URL to extract domain from
        
    Returns:
        Domain string or None if invalid
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def is_same_domain(url1: str, url2: str) -> bool:
    """
    Check if two URLs belong to the same domain.
    
    Args:
        url1: First URL
        url2: Second URL
        
    Returns:
        True if same domain, False otherwise
    """
    domain1 = extract_domain(url1)
    domain2 = extract_domain(url2)
    
    return domain1 is not None and domain2 is not None and domain1 == domain2


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename for safe file system usage.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing dots and spaces
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size_float = float(size_bytes)
    while size_float >= 1024 and i < len(size_names) - 1:
        size_float = size_float / 1024.0
        i += 1
    
    return f"{size_float:.1f}{size_names[i]}"


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    Create a simple progress bar string.
    
    Args:
        current: Current progress value
        total: Total value
        width: Width of the progress bar
        
    Returns:
        Progress bar string
    """
    if total == 0:
        return "[" + " " * width + "] 0%"
    
    progress = int((current / total) * width)
    percentage = int((current / total) * 100)
    
    bar = "[" + "=" * progress + " " * (width - progress) + "]"
    return f"{bar} {percentage}%" 