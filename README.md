# WebChecker - Regex-enabled Web Scraper

Web scraper that finds regex patterns across websites. CLI && front-end available. 
Package management using poetry

## Project Structure

```
email_scraper/
├── backend/                 # Backend Python
│   ├── webchecker/         # Checks web content
│   │   ├── __init__.py
│   │   ├── scraper.py      # Web scraping engine
│   │   ├── patterns.py     # Pattern matching logic with data retrieval
│   │   ├── utils.py        # utils
│   │   ├── main.py         # CLI interface
│   │   └── web_app.py      # Flask web app
│   ├── tests/              # Tests
│   │   ├── __init__.py
│   │   ├── test_patterns.py # Pattern matching unit test
│   │   └── test_utils.py    # Test utils
│   └── examples/           # example usages - start here if unsure
│       ├── __init__.py
│       └── basic_usage.py
├── frontend/               # Frontend assets
│   ├── templates/          # HTML
│   │   └── index.html      # index.html
│   └── static/             # static assets
├── run_web_server.py       # CLI launch of web server
├── pyproject.toml          # config
├── Makefile               # Makefile
└── README.md              # This file
```

## Quick Start

### Installation

```bash
# Create venv
python3 -m venv venv
source ./venv/bin/activate

# Install poetry (skip if poetry is already available)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
make install

# Or with development tools
make install-dev
```

### Web Interface

```bash
# Start the web server
make web

# Or directly from CLI
poetry run python run_web_server.py
```

The web interface will automatically open in your browser at the firt available port from `http://localhost:8080` to `http://localhost:8090`
Note - If all posts between 8080 and 8090 are in use, this 

### Command Line

```bash
# Find trademark symbols with context
poetry run webchecker https://example.com --pattern "™" --extract-before --extract-after

# Use custom regex pattern
poetry run webchecker https://example.com --custom-pattern r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
```

## Dev Checks

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
# Lint code using Flake8 (only backend)
make lint

# Format code
make format

# Clean up (deleting dev files)
make clean

# See all relevant commands
make help
```

### Examples

```bash
# Run demo examples
make demo
```

## Examples

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

### Custom Regex Patterns

```python
# Use custom regex for phone numbers
matcher = PatternMatcher(custom_pattern=r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')

results = scraper.scrape_site("https://example.com", matcher)
```
## Configuration Options

### Scraping Settings

Please ensure that when scraping you obey robots.txt and web rate limit requests.
This repo **will not do this for you**.

- `max_pages`: Maximum pages to scrape (default: 50)
- `max_depth`: Maximum link depth (default: 3)
- `timeout`: Request timeout in seconds (default: 10)
- `delay`: Delay between requests (default: 1.0)
- `follow_sitemap`: Follow sitemap URLs (default: False)

follow_sitemap will lead to scraping all URLs in sitemap.xml.
By default, this will search for links on the landing page and scrape all pages accessible from there (up to max_depth)

### Pattern Settings

- `extract_before`: Extract text before match
- `extract_after`: Extract text after match
- `custom_pattern`: Use custom regex pattern

## Testing

- **Pattern Matching**: Tests for text extraction and boundary detection
- **URL Utilities**: Tests for URL normalization and validation
- **Integration**: End-to-end functionality tests

Run tests with:

```bash
make test
```

## License

Do what you want with this. 

## Documentation

- **CLI Usage**: Run `poetry run webchecker --help`
- **Web Interface**: Access via browser, using port 8080 by default
