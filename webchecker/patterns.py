"""
Pattern matching module for finding specific characters and patterns in text.
"""

import re
from typing import List, Optional, Dict


class PatternMatcher:
    """Class for finding patterns in text, including trademark symbols."""
    
    def __init__(self, pattern: Optional[str] = None, custom_pattern: Optional[str] = None):
        """
        Initialize the pattern matcher.
        
        Args:
            pattern: Unicode character or string to search for (e.g., '™', '®', '©')
            custom_pattern: Custom regex pattern to search for
        """
        if custom_pattern:
            self.pattern = custom_pattern
            self.regex = re.compile(custom_pattern, re.UNICODE | re.IGNORECASE)
        elif pattern:
            self.pattern = re.escape(pattern)
            self.regex = re.compile(self.pattern, re.UNICODE)
        else:
            raise ValueError("Either pattern or custom_pattern must be provided")
    
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
        Find matches and extract text before/after them (up to the next/previous space).
        
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
                # Find the start of the word (previous space or start of text)
                word_start = match_start
                while word_start > 0 and not text[word_start - 1].isspace():
                    word_start -= 1
                
                # Extract the word (text from word_start to match_end)
                word = text[word_start:match_end]
            elif extract_after:
                # Find the end of the word (next space or end of text)
                word_end = match_end
                while word_end < len(text) and not text[word_end].isspace():
                    word_end += 1
                
                # Extract the word (text from match_start to word_end)
                word = text[match_start:word_end]
            else:
                word = match_text
            
            # Clean up the word (remove extra whitespace)
            word = word.strip()
            
            if word:
                matches.append(word)
        
        return matches
    
    def _find_matches_with_context_both(self, text: str) -> List[str]:
        """
        Find matches and extract text both before and after them.
        
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
            
            # Find the start of the word (previous space or start of text)
            word_start = match_start
            while word_start > 0 and not text[word_start - 1].isspace():
                word_start -= 1
            
            # Find the end of the word (next space or end of text)
            word_end = match_end
            while word_end < len(text) and not text[word_end].isspace():
                word_end += 1
            
            # Extract the complete word (text from word_start to word_end)
            word = text[word_start:word_end]
            
            # Clean up the word (remove extra whitespace)
            word = word.strip()
            
            if word:
                matches.append(word)
        
        return matches
    
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