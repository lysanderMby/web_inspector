# WebChecker Makefile

.PHONY: help install install-dev test test-extraction test-url web demo clean lint format

# Default target
help:
	@echo "WebChecker - Web Scraper for Patterns"
	@echo "====================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run all tests"
	@echo "  test-extraction - Run text extraction tests"
	@echo "  test-url     - Run URL utility tests"
	@echo "  test-email-fix - Run email extraction fix tests"
	@echo "  test-email-mode - Run email mode tests"
	@echo "  web          - Start web server"
	@echo "  demo         - Run demo examples"
	@echo "  demo-email   - Run email mode demo"
	@echo "  clean        - Clean up generated files"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"

# Install dependencies
install:
	poetry install

# Install development dependencies
install-dev:
	poetry install --with test

# Run all tests
test:
	poetry run python -m pytest backend/tests/ -v

# Run text extraction tests
test-extraction:
	poetry run python backend/tests/test_patterns.py

# Run URL utility tests
test-url:
	poetry run python backend/tests/test_utils.py

# Run email extraction fix tests
test-email-fix:
	poetry run python backend/tests/test_email_extraction_fix.py

# Run email mode tests
test-email-mode:
	poetry run python backend/tests/test_email_mode.py

# Start web server
web:
	poetry run python run_web_server.py

# Run demo examples
demo:
	poetry run python backend/examples/basic_usage.py

# Run email mode demo
demo-email:
	poetry run python backend/examples/email_mode_demo.py

# Clean up generated files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -f webchecker.log
	rm -f *.txt
	rm -f *.log

# Run linting
lint:
	poetry run flake8 backend/ --max-line-length=100 --ignore=E501,W503

# Format code
format:
	poetry run black backend/ --line-length=100
	poetry run isort backend/

# Development server with auto-reload
dev:
	poetry run python run_web_server.py

# Quick test of CLI
cli-test:
	poetry run webchecker --help

# Quick test of web interface
web-test:
	poetry run webchecker-web --help 