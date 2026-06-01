# Makefile for ai-document-translator
SHELL := /bin/bash
.ONESHELL:
.SHELLFLAGS := -o pipefail -c

# Colors for output
BLUE := \033[94m
GREEN := \033[92m
YELLOW := \033[93m
RED := \033[91m
RESET := \033[0m

.PHONY: help install-dev test lint format fix check-all clean

help:
	@printf "$(BLUE)📌 Available targets:$(RESET)\n"
	@printf "  $(GREEN)make install-dev$(RESET) — Install dev dependencies\n"
	@printf "  $(GREEN)make test$(RESET)      — Run tests with coverage\n"
	@printf "  $(GREEN)make lint$(RESET)     — Check code style & bugs\n"
	@printf "  $(GREEN)make format$(RESET)   — Format code with ruff\n"
	@printf "  $(GREEN)make fix$(RESET)      — Auto-fix linting & formatting issues\n"
	@printf "  $(GREEN)make check-all$(RESET) — Run all checks (lint + test + format check)\n"
	@printf "  $(GREEN)make clean$(RESET)    — Remove cache, coverage, and build artifacts\n"

install-dev:
	@printf "$(BLUE)📦 Installing dev dependencies…$(RESET)\n"
	pip install -e ".[dev]"
	# Optional: if using `uv` instead of `pip`, uncomment below:
	uv sync --extra dev

test:
	@printf "$(BLUE)🧪 Running tests…$(RESET)\n"
	pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml --strict-markers

lint:
	@printf "$(BLUE)🔍 Running linter (ruff)…$(RESET)\n"
	ruff check .

format:
	@printf "$(YELLOW)🎨 Formatting with ruff format…$(RESET)\n"
	ruff format .

fix: format lint
	@printf "$(GREEN)✨ Auto-fixing issues…$(RESET)\n"

check-all: lint test
	@printf "$(GREEN)✅ All checks passed!$(RESET)\n"

clean:
	@printf "$(RED)🧹 Cleaning build artifacts and cache…$(RESET)\n"
	rm -rf .pytest_cache .coverage htmlcov .ruff_cache .mypy_cache .hypothesis build/ dist/ *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

update-requirements:
	@printf "$(BLUE)🔄 Updating requirements.txt…$(RESET)\n"
	uv export --format requirements-txt -o requirements.txt

test-pre-commit:
	@printf "$(BLUE)🧪 Running pre-commit hooks…$(RESET)\n"
	pre-commit run --all-files --show-diff-on-failure
