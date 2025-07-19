"""
Pattern matching module for finding specific characters and patterns in text.
"""

import re
from typing import List, Optional, Dict, Tuple


class PatternMatcher:
    """Class for finding patterns in text, including trademark symbols."""
    
    def __init__(self, pattern: Optional[str] = None, custom_pattern: Optional[str] = None, email_mode: bool = False):
        """
        Initialize the pattern matcher.
        
        Args:
            pattern: Unicode character or string to search for (e.g., '™', '®', '©')
            custom_pattern: Custom regex pattern to search for
            email_mode: Enable email detection mode with validation
        """
        self.email_mode = email_mode
        
        if email_mode:
            # Use comprehensive email regex pattern
            self.pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            self.regex = re.compile(self.pattern, re.UNICODE | re.IGNORECASE)
        elif custom_pattern:
            self.pattern = custom_pattern
            self.regex = re.compile(custom_pattern, re.UNICODE | re.IGNORECASE)
        elif pattern:
            self.pattern = re.escape(pattern)
            self.regex = re.compile(self.pattern, re.UNICODE)
        else:
            raise ValueError("Either pattern, custom_pattern, or email_mode must be provided")
    
    def find_matches(self, text: str, extract_before: bool = False, extract_after: bool = False) -> List[str]:
        """
        Find all matches of the pattern in the given text.
        
        Args:
            text: The text to search in
            extract_before: Whether to extract text before the matched pattern
            extract_after: Whether to extract text after the matched pattern
            
        Returns:
            List of found matches
        """
        matches = []
        
        if extract_before and extract_after:
            matches = self._find_matches_with_context_both(text)
        elif extract_before:
            matches = self._find_matches_with_context(text, extract_before=True)
        elif extract_after:
            matches = self._find_matches_with_context(text, extract_after=True)
        else:
            # Find all matches
            for match in self.regex.finditer(text):
                matches.append(match.group())
        
        return matches
    
    def _find_matches_with_context(self, text: str, extract_before: bool = True, extract_after: bool = False) -> List[str]:
        """
        Find matches and extract text before/after them with smart boundary detection.
        
        Args:
            text: The text to search in
            extract_before: Whether to extract text before the match
            extract_after: Whether to extract text after the match
            
        Returns:
            List of extracted text with context
        """
        matches = []
        
        for match in self.regex.finditer(text):
            match_start = match.start()
            match_end = match.end()
            match_text = match.group()
            
            if extract_before:
                # Find the start of the word (previous boundary or start of text)
                word_start = match_start
                while word_start > 0:
                    char = text[word_start - 1]
                    # Stop at whitespace, line breaks, HTML tags, or control characters
                    if (char.isspace() or char in '\n\r\t' or 
                        char in '()[]{}<>"' or ord(char) < 32 or
                        char in '‍'):  # Zero-width space
                        break
                    word_start -= 1
                
                # Extract the word (text from word_start to match_end)
                word = text[word_start:match_end]
            elif extract_after:
                # Find the end of the word (next boundary or end of text)
                word_end = match_end
                while word_end < len(text):
                    char = text[word_end]
                    # Stop at whitespace, line breaks, HTML tags, or control characters
                    if (char.isspace() or char in '\n\r\t' or 
                        char in '()[]{}<>"' or ord(char) < 32 or
                        char in '‍'):  # Zero-width space
                        break
                    word_end += 1
                
                # Extract the word (text from match_start to word_end)
                word = text[match_start:word_end]
            else:
                word = match_text
            
            # Clean up the word (remove extra whitespace and trailing punctuation)
            word = word.strip()
            # Remove trailing punctuation but preserve email structure
            word = self._clean_trailing_punctuation(word)
            
            # Additional cleanup for HTML artifacts
            word = self._clean_html_artifacts(word)
            
            if word:
                matches.append(word)
        
        return matches
    
    def _find_matches_with_context_both(self, text: str) -> List[str]:
        """
        Find matches and extract text both before and after them with smart boundary detection.
        
        Args:
            text: The text to search in
            
        Returns:
            List of extracted text with context (before + match + after)
        """
        matches = []
        
        for match in self.regex.finditer(text):
            match_start = match.start()
            match_end = match.end()
            match_text = match.group()
            
            # Find the start of the word (previous boundary or start of text)
            word_start = match_start
            while word_start > 0:
                char = text[word_start - 1]
                # Stop at whitespace, line breaks, HTML tags, or control characters
                if (char.isspace() or char in '\n\r\t' or 
                    char in '()[]{}<>"' or ord(char) < 32 or
                    char in '‍'):  # Zero-width space
                    break
                word_start -= 1
            
            # Find the end of the word (next boundary or end of text)
            word_end = match_end
            while word_end < len(text):
                char = text[word_end]
                # Stop at whitespace, line breaks, HTML tags, or control characters
                if (char.isspace() or char in '\n\r\t' or 
                    char in '()[]{}<>"' or ord(char) < 32 or
                    char in '‍'):  # Zero-width space
                    break
                word_end += 1
            
            # Extract the complete word (text from word_start to word_end)
            word = text[word_start:word_end]
            
            # Clean up the word (remove extra whitespace and trailing punctuation)
            word = word.strip()
            # Remove trailing punctuation but preserve email structure
            word = self._clean_trailing_punctuation(word)
            
            # Additional cleanup for HTML artifacts
            word = self._clean_html_artifacts(word)
            
            if word:
                matches.append(word)
        
        return matches
    
    def _clean_trailing_punctuation(self, word: str) -> str:
        """
        Clean trailing punctuation while preserving email structure.
        
        Args:
            word: The word to clean
            
        Returns:
            Cleaned word
        """
        # If it looks like an email address, be more careful with punctuation
        if '@' in word and '.' in word.split('@')[1]:
            # For emails, only remove punctuation at the very end
            # but preserve dots in the domain
            return word.rstrip(',;:!?')
        else:
            # For other patterns, remove trailing punctuation more aggressively
            return word.rstrip('.,;:!?')
    
    def _clean_html_artifacts(self, word: str) -> str:
        """
        Clean HTML artifacts and other unwanted characters from extracted text.
        
        Args:
            word: The word to clean
            
        Returns:
            Cleaned word
        """
        import re
        
        # Remove HTML tags
        word = re.sub(r'<[^>]+>', '', word)
        
        # Remove zero-width spaces and other invisible characters
        word = re.sub(r'[\u200B-\u200D\uFEFF]', '', word)
        
        # Remove common HTML entities that might have been missed
        word = word.replace('&nbsp;', ' ')
        word = word.replace('&amp;', '&')
        word = word.replace('&lt;', '<')
        word = word.replace('&gt;', '>')
        word = word.replace('&quot;', '"')
        word = word.replace('&apos;', "'")
        
        # Remove Framer-specific artifacts
        word = re.sub(r'<!--\$-->.*?<!--/\$-->', '', word, flags=re.DOTALL)
        word = re.sub(r'data-framer-[^=]*="[^"]*"', '', word)
        word = re.sub(r'framer-[a-zA-Z0-9-]+', '', word)
        
        # Remove extra whitespace
        word = re.sub(r'\s+', ' ', word)
        
        # Strip leading/trailing whitespace
        word = word.strip()
        
        return word
    
    def find_trademark_matches(self, text: str) -> List[str]:
        """
        Specialized method for finding trademark-related patterns.
        
        Args:
            text: The text to search in
            
        Returns:
            List of trademark matches with context
        """
        # Common trademark patterns
        trademark_patterns = [
            r'\b\w+\s*™\b',  # Word followed by TM symbol
            r'\b\w+\s*®\b',  # Word followed by R symbol
            r'\b\w+\s*©\b',  # Word followed by copyright symbol
            r'\b\w+\s*\(TM\)\b',  # Word followed by (TM)
            r'\b\w+\s*\(R\)\b',   # Word followed by (R)
            r'\b\w+\s*\(C\)\b',   # Word followed by (C)
        ]
        
        matches = []
        for pattern in trademark_patterns:
            regex = re.compile(pattern, re.UNICODE | re.IGNORECASE)
            for match in regex.finditer(text):
                matches.append(match.group())
        
        return matches
    
    def find_common_symbols(self, text: str) -> Dict[str, List[str]]:
        """
        Find common special symbols and their context.
        
        Args:
            text: The text to search in
            
        Returns:
            Dictionary mapping symbol types to lists of matches
        """
        symbol_patterns = {
            'trademark': r'\b\w+\s*™\b',
            'registered': r'\b\w+\s*®\b',
            'copyright': r'\b\w+\s*©\b',
            'degree': r'\d+\s*°',
            'currency': r'[\$€£¥]\s*\d+',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        }
        
        results = {}
        for symbol_type, pattern in symbol_patterns.items():
            regex = re.compile(pattern, re.UNICODE | re.IGNORECASE)
            matches = [match.group() for match in regex.finditer(text)]
            if matches:
                results[symbol_type] = matches
        
        return results
    
    def is_valid_email(self, email: str) -> bool:
        """
        Validate email address format and common patterns.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email is valid, False otherwise
        """
        # Basic format check
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
            return False
        
        # Check for common invalid patterns
        invalid_patterns = [
            r'\.\.',  # Double dots
            r'@\.',   # @ followed by dot
            r'\.@',   # Dot followed by @
            r'^\.',   # Starts with dot
            r'\.$',   # Ends with dot
            r'@$',    # Ends with @
            r'^@',    # Starts with @
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, email):
                return False
        
        # Check domain length
        parts = email.split('@')
        if len(parts) != 2:
            return False
        
        local_part, domain = parts
        
        # Local part checks
        if len(local_part) > 64 or len(local_part) == 0:
            return False
        
        # Domain checks
        if len(domain) > 253 or len(domain) == 0:
            return False
        
        # Check for valid TLD (at least 2 characters)
        domain_parts = domain.split('.')
        if len(domain_parts) < 2:
            return False
        
        tld = domain_parts[-1]
        if len(tld) < 2:
            return False
        
        return True
    
    def find_emails_with_pages(self, text: str, page_url: str) -> List[Tuple[str, str]]:
        """
        Find valid email addresses in text and return with page URL.
        
        Args:
            text: The text to search in
            page_url: The URL of the page being searched
            
        Returns:
            List of tuples (email, page_url) for valid emails
        """
        if not self.email_mode:
            raise ValueError("This method requires email_mode=True")
        
        emails = []
        
        # Find all potential email matches
        for match in self.regex.finditer(text):
            email = match.group().strip()
            
            # Clean HTML artifacts
            email = self._clean_html_artifacts(email)
            
            # Validate email
            if self.is_valid_email(email):
                emails.append((email, page_url))
        
        return emails 