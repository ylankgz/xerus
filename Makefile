# Xerus Makefile
# Convenient shortcuts for uv-based development workflow

.PHONY: help install dev test lint format build publish clean migrate

# Default target
help:
	@echo "Xerus Development Commands (using uv)"
	@echo "====================================="
	@echo "install     - Install dependencies"
	@echo "dev         - Install with dev dependencies"
	@echo "test        - Run tests"
	@echo "lint        - Run linters"
	@echo "format      - Format code"
	@echo "build       - Build package"
	@echo "publish     - Build and publish (with validation)"
	@echo "publish-test - Publish to Test PyPI"
	@echo "clean       - Clean build artifacts"
	@echo ""
	@echo "Example: make dev && make test && make build"

# Install dependencies
install:
	uv sync

# Install with development dependencies
dev:
	uv sync --dev

# Run tests
test:
	uv run pytest

# Run linters
lint:
	uv run black --check .
	uv run flake8 .

# Format code
format:
	uv run black .

# Build package
build:
	uv build

# Clean build artifacts
clean:
	rm -rf dist/ build/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Build and publish with validation
publish: clean dev test build
	python scripts/build_and_publish.py

# Publish to Test PyPI
publish-test: clean dev test build
	python scripts/build_and_publish.py --test-pypi


# Development workflow - install, test, and format
dev-setup: dev test format
	@echo "✅ Development environment ready!"
