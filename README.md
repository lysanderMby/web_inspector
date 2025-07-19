# WebChecker

A comprehensive web scraper that finds specific characters and patterns on websites. Perfect for finding trademark symbols (™, ®, ©), custom patterns, and other special characters across entire websites.

## Features

- **Pattern Matching**: Find specific Unicode characters (™, ®, ©) or custom regex patterns
- **Context Extraction**: Extract text before, after, or both around matched patterns (e.g., "BrandName™", "@example.com", "john@example.com")
- **Sitemap Support**: Automatically discover and follow sitemap.xml files
- **Respectful Crawling**: Configurable delays and user agent strings
- **Flexible Output**: Print to console or save to file
- **File Type Filtering**: Exclude PDFs, images, and other binary files
- **Comprehensive Logging**: Verbose logging for debugging

## Installation

This project uses Poetry for dependency management. Make sure you have Poetry installed, then:

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Usage

### Basic Usage

Find trademark symbols (™) on a website:
```bash
python -m webchecker.main https://example.com --pattern "™" --extract-before
```

Find registered trademarks (®):
```bash
python -m webchecker.main https://example.com --pattern "®" --extract-before
```

Find email addresses (extract after @ symbol):
```bash
python -m webchecker.main https://example.com --pattern "@" --extract-after
```

Find complete email addresses (extract both before and after):
```bash
python -m webchecker.main https://example.com --pattern "@" --extract-before --extract-after
```

### Advanced Usage

Use custom regex patterns:
```bash
python -m webchecker.main https://example.com --custom-pattern "\\b\\w+\\s*™\\b" --verbose
```

Follow sitemap and limit pages:
```bash
python -m webchecker.main https://example.com --pattern "™" --follow-sitemap --max-pages 100
```

Save results to file:
```bash
python -m webchecker.main https://example.com --pattern "™" --output results.txt
```

Exclude specific file types (PDFs, documents):
```bash
python -m webchecker.main https://example.com --pattern "@" --exclude-extensions .pdf .doc .docx
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `url` | Starting URL to scrape | Required |
| `--pattern` | Unicode character to search for | None |
| `--custom-pattern` | Custom regex pattern | None |
| `--extract-before` | Extract text before pattern | False |
| `--extract-after` | Extract text after pattern | False |
| `--exclude-extensions` | File extensions to exclude (e.g., .pdf .doc) | Common binary files |
| `--max-pages` | Maximum pages to scrape | 50 |
| `--max-depth` | Maximum link depth | 3 |
| `--timeout` | Request timeout (seconds) | 10 |
| `--user-agent` | User agent string | WebChecker/0.1.0 |
| `--verbose` | Enable verbose output | False |
| `--output` | Output file path | stdout |
| `--follow-sitemap` | Follow sitemap.xml | False |

## Examples

### Finding Trademark Symbols

```bash
# Find all trademark symbols and extract the brand names
python -m webchecker.main https://company.com --pattern "™" --extract-before --verbose

# Output example:
# https://company.com: BrandName™
# https://company.com/products: ProductName™
```

### Finding Email Addresses

```bash
# Find email addresses and extract the domain part
python -m webchecker.main https://company.com --pattern "@" --extract-after

# Output example:
# https://company.com: @example.com
# https://company.com/contact: @company.org

# Find complete email addresses
python -m webchecker.main https://company.com --pattern "@" --extract-before --extract-after

# Output example:
# https://company.com: john@example.com
# https://company.com/contact: jane@company.org
```

### Finding Copyright Notices

```bash
# Find copyright symbols
python -m webchecker.main https://example.com --pattern "©" --extract-before
```

### Custom Pattern Matching

```bash
# Find email addresses
python -m webchecker.main https://example.com --custom-pattern "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b"

# Find phone numbers
python -m webchecker.main https://example.com --custom-pattern "\\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b"
```

## Project Structure

```
webchecker/
├── __init__.py          # Package initialization
├── main.py             # Command line interface
├── scraper.py          # Web scraping logic
├── patterns.py         # Pattern matching
└── utils.py            # Utility functions
```

## Development

### Setting Up Development Environment

1. Clone the repository
2. Install Poetry if not already installed:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=webchecker
```

### Code Quality

```bash
# Run linting
poetry run flake8 webchecker/

# Run type checking
poetry run mypy webchecker/
```

## Next Steps for Development

### 1. Enhanced Pattern Matching
- Add support for more symbol types (currency, mathematical symbols)
- Implement fuzzy matching for similar characters
- Add support for HTML entities (e.g., `&trade;`, `&reg;`)

### 2. Performance Improvements
- Implement concurrent scraping with asyncio
- Add caching for visited URLs
- Implement rate limiting per domain

### 3. Advanced Features
- Add support for JavaScript-rendered content (Selenium integration)
- Implement content filtering (ignore navigation, footers)
- Add export formats (JSON, CSV, XML)
- Implement database storage for results

### 4. Configuration
- Add configuration file support (YAML/JSON)
- Implement user-defined rules and filters
- Add support for robots.txt compliance

### 5. Monitoring and Analytics
- Add scraping statistics and metrics
- Implement progress bars for long-running scrapes
- Add support for resuming interrupted scrapes

### 6. Testing and Quality
- Add comprehensive unit tests
- Implement integration tests with mock servers
- Add performance benchmarks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Technical Notes

### Type Annotations
The project uses type annotations for better code quality. Some BeautifulSoup-related type warnings may appear in IDEs but don't affect functionality. The code includes `# type: ignore` comments where necessary to suppress false positive warnings.

### Dependencies
- **requests**: HTTP library for web requests
- **beautifulsoup4**: HTML/XML parsing
- **lxml**: Fast XML/HTML parser
- **urllib3**: HTTP client library

## Disclaimer

This tool is for educational and legitimate research purposes only. Always respect website terms of service and robots.txt files. Be mindful of rate limiting and server resources when scraping websites. 