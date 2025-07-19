#!/usr/bin/env python3
"""
Web server launcher for WebChecker.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.webchecker.web_app import main

if __name__ == "__main__":
    main() 