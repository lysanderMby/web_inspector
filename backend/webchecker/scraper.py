"""
Web scraping module for finding patterns on websites.
"""

import time
import logging
from collections import deque
from typing import List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .patterns import PatternMatcher
from .utils import setup_logging


class WebScraper:
    """Web scraper for finding patterns on websites."""
    
    def __init__(
        self,
        max_pages: int = 50,
        max_depth: int = 3,
        timeout: int = 10,
        user_agent: str = "WebChecker/0.1.0",
        follow_sitemap: bool = False,
        delay: float = 1.0,
        exclude_extensions: Optional[List[str]] = None
    ):
        """
        Initialize the web scraper.
        
        Args:
            max_pages: Maximum number of pages to scrape
            max_depth: Maximum link depth to follow
            timeout: Request timeout in seconds
            user_agent: User agent string for requests
            follow_sitemap: Whether to follow sitemap URLs
            delay: Delay between requests in seconds
            exclude_extensions: File extensions to exclude
        """
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.timeout = timeout
        self.user_agent = user_agent
        self.follow_sitemap = follow_sitemap
        self.delay = delay
        
        # Default excluded extensions (common binary files)
        self.exclude_extensions = exclude_extensions or [
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.rar', '.tar', '.gz', '.7z',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico',
            '.mp3', '.mp4', '.avi', '.mov', '.wmv',
            '.exe', '.dmg', '.pkg', '.deb', '.rpm'
        ]
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Track visited URLs
        self.visited_urls: Set[str] = set()
        
        # Setup logging
        self.logger = setup_logging(verbose=True)

        session = requests.Session()
        session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }

    
    def scrape_site(
        self,
        start_url: str,
        pattern_matcher: PatternMatcher,
        extract_before: bool = False,
        extract_after: bool = False,
        email_mode: bool = False
    ) -> List[str]:
        """
        Scrape a website starting from the given URL and find patterns.
        
        Args:
            start_url: The URL to start scraping from
            pattern_matcher: PatternMatcher instance to use for finding patterns
            extract_before: Whether to extract text before the matched pattern
            extract_after: Whether to extract text after the matched pattern
            email_mode: Whether to use email mode with grouped results
            
        Returns:
            List of found matches (or grouped email results if email_mode=True)
        """
        if email_mode:
            return self._scrape_site_email_mode(start_url, pattern_matcher)
        
        results = []
        base_domain = urlparse(start_url).netloc
        
        # Initialize URL queue with (url, depth) tuples
        url_queue = deque([(start_url, 0)])
        
        # Add sitemap URLs if requested
        if self.follow_sitemap:
            sitemap_urls = self._discover_sitemap_urls(start_url)
            for url in sitemap_urls:
                if url not in self.visited_urls:
                    url_queue.append((url, 0))
        
        while url_queue and len(self.visited_urls) < self.max_pages:
            current_url, depth = url_queue.popleft()
            
            if current_url in self.visited_urls or depth > self.max_depth:
                continue
            
            self.visited_urls.add(current_url)
            self.logger.info(f"Scraping {current_url} (depth: {depth})")
            
            try:
                # Fetch and parse the page
                page_results = self._scrape_page(
                    current_url, pattern_matcher, extract_before, extract_after
                )
                results.extend(page_results)
                
                # Add delay to be respectful
                time.sleep(self.delay)
                
                # Find new links if we haven't reached max depth
                if depth < self.max_depth:
                    new_links = self._extract_links(current_url, base_domain)
                    for link in new_links:
                        if link not in self.visited_urls:
                            url_queue.append((link, depth + 1))
                
            except Exception as e:
                self.logger.warning(f"Error scraping {current_url}: {e}")
                continue
        
        return results
    
    def _scrape_page(
        self,
        url: str,
        pattern_matcher: PatternMatcher,
        extract_before: bool,
        extract_after: bool
    ) -> List[str]:
        """Scrape a single page and find patterns."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Find patterns
            matches = pattern_matcher.find_matches(text, extract_before, extract_after)
            
            # Add URL context to results
            results = []
            for match in matches:
                results.append(f"{url}: {match}")
            
            return results
            
        except requests.RequestException as e:
            self.logger.warning(f"Failed to fetch {url}: {e}")
            return []
    
    def _extract_links(self, url: str, base_domain: str) -> List[str]:
        """Extract links from a page that belong to the same domain."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = str(link['href'])  # type: ignore
                absolute_url = urljoin(url, href)
                
                # Only include links from the same domain and not excluded
                if (urlparse(absolute_url).netloc == base_domain and 
                    not self._should_exclude_url(absolute_url)):
                    links.append(absolute_url)
            
            return links
            
        except requests.RequestException:
            return []
    
    def _discover_sitemap_urls(self, base_url: str) -> List[str]:
        """Discover URLs from sitemap.xml if available."""
        sitemap_urls = []
        
        # Common sitemap locations
        sitemap_locations = [
            urljoin(base_url, '/sitemap.xml'),
            urljoin(base_url, '/sitemap_index.xml'),
            urljoin(base_url, '/robots.txt')
        ]
        
        for location in sitemap_locations:
            try:
                response = self.session.get(location, timeout=self.timeout)
                response.raise_for_status()
                
                if location.endswith('robots.txt'):
                    # Parse robots.txt for sitemap
                    sitemap_urls.extend(self._parse_robots_txt(response.text, base_url))
                else:
                    # Parse sitemap.xml
                    sitemap_urls.extend(self._parse_sitemap_xml(response.text))
                
            except requests.RequestException:
                continue
        
        return sitemap_urls
    
    def _parse_robots_txt(self, content: str, base_url: str) -> List[str]:
        """Parse robots.txt for sitemap entries."""
        urls = []
        for line in content.split('\n'):
            if line.lower().startswith('sitemap:'):
                sitemap_url = line.split(':', 1)[1].strip()
                urls.append(sitemap_url)
        return urls
    
    def _parse_sitemap_xml(self, content: str) -> List[str]:
        """Parse sitemap.xml for URLs."""
        urls = []
        try:
            soup = BeautifulSoup(content, 'xml')
            for url_tag in soup.find_all('url'):
                loc_tag = url_tag.find('loc')  # type: ignore
                if loc_tag:
                    urls.append(str(loc_tag.text).strip())  # type: ignore
        except Exception as e:
            self.logger.warning(f"Error parsing sitemap: {e}")
        
        return urls
    
    def _should_exclude_url(self, url: str) -> bool:
        """
        Check if a URL should be excluded based on file extension.
        
        Args:
            url: The URL to check
            
        Returns:
            True if the URL should be excluded, False otherwise
        """
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        
        # Check if the path ends with any excluded extension
        for ext in self.exclude_extensions:
            if path.endswith(ext):
                return True
        
        # Also check for common binary content types in the URL
        binary_indicators = [
            '/download/', '/files/', '/assets/', '/media/',
            'blob:', 'data:', 'javascript:'
        ]
        
        for indicator in binary_indicators:
            if indicator in url.lower():
                return True
        
        return False
    
    def _scrape_site_email_mode(self, start_url: str, pattern_matcher: PatternMatcher) -> List[str]:
        """
        Scrape site in email mode, returning grouped email results.
        
        Args:
            start_url: The URL to start scraping from
            pattern_matcher: PatternMatcher instance configured for email mode
            
        Returns:
            List of grouped email results
        """
        from collections import defaultdict
        
        # Dictionary to group emails by email address
        email_groups = defaultdict(set)
        base_domain = urlparse(start_url).netloc
        
        # Initialize URL queue with (url, depth) tuples
        url_queue = deque([(start_url, 0)])
        
        # Add sitemap URLs if requested
        if self.follow_sitemap:
            sitemap_urls = self._discover_sitemap_urls(start_url)
            for url in sitemap_urls:
                if url not in self.visited_urls:
                    url_queue.append((url, 0))
        
        while url_queue and len(self.visited_urls) < self.max_pages:
            current_url, depth = url_queue.popleft()
            
            if current_url in self.visited_urls or depth > self.max_depth:
                continue
            
            self.visited_urls.add(current_url)
            self.logger.info(f"Scraping {current_url} (depth: {depth})")
            
            try:
                # Fetch and parse the page
                page_emails = self._scrape_page_email_mode(current_url, pattern_matcher)
                
                # Group emails by email address
                for email, page_url in page_emails:
                    email_groups[email].add(page_url)
                
                # Add delay to be respectful
                time.sleep(self.delay)
                
                # Find new links if we haven't reached max depth
                if depth < self.max_depth:
                    new_links = self._extract_links(current_url, base_domain)
                    for link in new_links:
                        if link not in self.visited_urls:
                            url_queue.append((link, depth + 1))
                
            except Exception as e:
                self.logger.warning(f"Error scraping {current_url}: {e}")
                continue
        
        # Format results as grouped email entries
        results = []
        for email, pages in email_groups.items():
            pages_list = sorted(list(pages))
            results.append(f"{email}: {', '.join(pages_list)}")
        
        return results
    
    def _scrape_page_email_mode(self, url: str, pattern_matcher: PatternMatcher) -> List[Tuple[str, str]]:
        """Scrape a single page in email mode."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Also extract emails from href attributes (mailto: links)
            mailto_emails = []
            for link in soup.find_all('a', href=True):
                href = str(link['href'])  # type: ignore
                if href.startswith('mailto:'):
                    email = href[7:]  # Remove 'mailto:' prefix
                    # Clean the email (remove query parameters, etc.)
                    email = email.split('?')[0].split('#')[0]
                    if pattern_matcher.is_valid_email(email):
                        mailto_emails.append((email, url))
            
            # Find emails in text content
            text_emails = pattern_matcher.find_emails_with_pages(text, url)
            
            # Combine and deduplicate
            all_emails = text_emails + mailto_emails
            unique_emails = []
            seen_emails = set()
            
            for email, page_url in all_emails:
                if email not in seen_emails:
                    unique_emails.append((email, page_url))
                    seen_emails.add(email)
            
            return unique_emails
            
        except requests.RequestException as e:
            self.logger.warning(f"Failed to fetch {url}: {e}")
            return []
    
    def close(self):
        """Close the session."""
        self.session.close() 