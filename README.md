# WebChecker - Web Scraper for Patterns

A powerful web scraper that finds specific characters and patterns across websites, with both command-line and web interfaces.

## 🏗️ Project Structure

```
email_scraper/
├── backend/                 # Backend Python code
│   ├── webchecker/         # Core WebChecker package
│   │   ├── __init__.py
│   │   ├── scraper.py      # Web scraping engine
│   │   ├── patterns.py     # Pattern matching logic
│   │   ├── utils.py        # Utility functions
│   │   ├── main.py         # CLI interface
│   │   └── web_app.py      # Flask web application
│   ├── tests/              # Test files
│   │   ├── __init__.py
│   │   ├── test_patterns.py
│   │   └── test_utils.py
│   └── examples/           # Example usage
│       ├── __init__.py
│       └── basic_usage.py
├── frontend/               # Frontend assets
│   ├── templates/          # HTML templates
│   │   └── index.html      # Main web interface
│   └── static/             # Static assets (CSS, JS, images)
├── run_web_server.py       # Web server launcher
├── pyproject.toml          # Project configuration
├── Makefile               # Build and development commands
└── README.md              # This file
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
make install

# Or with development tools
make install-dev
```

### Web Interface

```bash
# Start the web server
make web

# Or directly
poetry run python run_web_server.py
```

The web interface will automatically open in your browser at `http://localhost:8080`.

### Command Line

```bash
# Find trademark symbols
poetry run webchecker https://example.com --pattern "™"

# Find email addresses with context
poetry run webchecker https://example.com --pattern "@" --extract-before --extract-after

# Use email detection mode (recommended for emails)
poetry run webchecker https://example.com --email-mode

# Use custom regex pattern
poetry run webchecker https://example.com --custom-pattern r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
```

## 🔧 Development

### Running Tests

```bash
# Run all tests
make test

# Run specific test suites
make test-extraction
make test-url

# Run with pytest directly
poetry run pytest backend/tests/ -v
```

### Code Quality

```bash
# Lint code
make lint

# Format code
make format

# Clean up
make clean
```

### Examples

```bash
# Run demo examples
make demo
```

## 📖 Usage Examples

### Finding Trademarks

```python
from backend.webchecker.scraper import WebScraper
from backend.webchecker.patterns import PatternMatcher

# Create pattern matcher for trademark symbol
matcher = PatternMatcher(pattern="™")

# Create scraper
scraper = WebScraper(max_pages=10, max_depth=2)

# Scrape website
results = scraper.scrape_site(
    "https://example.com",
    matcher,
    extract_before=True,
    extract_after=True
)

print(f"Found {len(results)} trademark matches")
```

### Finding Email Addresses

```python
# Method 1: Use email detection mode (recommended)
matcher = PatternMatcher(email_mode=True)

# Scrape with email validation and grouping
results = scraper.scrape_site(
    "https://example.com",
    matcher,
    email_mode=True
)

# Method 2: Use @ pattern with context extraction
matcher = PatternMatcher(pattern="@")

# Scrape with context extraction
results = scraper.scrape_site(
    "https://example.com",
    matcher,
    extract_before=True,
    extract_after=True
)
```

### Custom Regex Patterns

```python
# Use custom regex for phone numbers
matcher = PatternMatcher(custom_pattern=r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')

results = scraper.scrape_site("https://example.com", matcher)
```

## 🌐 Web Interface Features

- **Modern UI**: Clean, responsive design
- **Email Detection Mode**: Checkbox to enable specialized email finding with validation
- **Real-time Progress**: Live progress updates during scraping
- **Auto-clear Results**: Previous results automatically clear on new scrape
- **Smart URL Handling**: Automatically adds protocol if missing
- **Export Results**: Download results as text file
- **Error Handling**: Clear error messages and recovery
- **No Results Feedback**: Shows helpful message when no matches found
- **Grouped Results**: Email mode shows emails grouped with page locations

## 🔍 Pattern Matching

WebChecker supports various pattern matching options:

- **Simple Characters**: `™`, `@`, `©`, `®`
- **Email Detection Mode**: Specialized mode with validation and grouping
- **Custom Regex**: Any valid Python regex pattern
- **Context Extraction**: Extract text before/after matches
- **Smart Boundaries**: Intelligent word boundary detection
- **Email Validation**: Built-in email format validation
- **HTML Artifact Cleaning**: Automatic removal of HTML tags and artifacts

## ⚙️ Configuration Options

### Scraping Settings

- `max_pages`: Maximum pages to scrape (default: 50)
- `max_depth`: Maximum link depth (default: 3)
- `timeout`: Request timeout in seconds (default: 10)
- `delay`: Delay between requests (default: 1.0)
- `follow_sitemap`: Follow sitemap URLs (default: False)

### Pattern Settings

- `extract_before`: Extract text before match
- `extract_after`: Extract text after match
- `custom_pattern`: Use custom regex pattern
- `email_mode`: Enable email detection mode with validation

## 🧪 Testing

The project includes comprehensive tests:

- **Pattern Matching**: Tests for text extraction and boundary detection
- **Email Mode**: Tests for email detection and validation
- **Email Extraction Fix**: Tests for HTML artifact cleaning
- **URL Utilities**: Tests for URL normalization and validation
- **Integration**: End-to-end functionality tests

Run tests with:

```bash
make test
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📚 Documentation

- **CLI Usage**: Run `poetry run webchecker --help`
- **Web Interface**: Access via browser at `http://localhost:8080`
- **API Documentation**: See `backend/webchecker/` for module documentation 