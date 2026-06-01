# Agent Instructions - Document Translator Service

This file defines universal instructions for any AI coding agent working in this codebase.

Treat this file as the canonical source of behavior. If mirrored rule files differ, follow this file.

## Project Overview

Document Translator Service is a Python/FastAPI-based document translation and localization service. It provides APIs for translating documents between languages and managing localization workflows.

## Repository Structure

Files should be organized according to Python project best practices and existing conventions:

- `src/` — Application source code
- `tests/` — Test suite
- `docs/` — Documentation
- `config/` — Configuration files
- `migrations/` — Database migrations (if using ORM)

## Agent Skills

Agents working in this codebase should automatically load and use all skills located in the `.agents/skills/` directory. These skills provide specialized instructions and workflows for:

- Conventional commits
- FastAPI development
- Python code style
- Python design patterns
- Python testing patterns
- Docker containerization
- Ollama model maintenance
- Skill discovery

## Coding Standards

### Python Style

- Follow PEP 8 conventions
- Use type hints on all function signatures
- Include docstrings using Google or NumPy style
- Keep functions focused (SRP)
- Prefer composition over inheritance

### FastAPI Patterns

- Use dependency injection for cross-cutting concerns
- Implement async/await for I/O operations
- Use Pydantic models for request/response validation
- Implement comprehensive error handling with custom exceptions
- Use Pydantic settings to manage configuration

### Testing

- Write tests following test-driven development principles
- Use pytest with appropriate fixtures
- Mock external dependencies
- Aim for high test coverage, especially for critical paths

## Git Commits

- Use conventional commit messages in XML format
- Format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore, ci, perf, build
- Keep messages concise (50 chars maximum)
- Include scope to indicate affected component
- Never add Co-Authored-By trailers
- Never run destructive git commands unless explicitly requested

## Docker Best Practices

- Use multi-stage builds for smaller images
- Implement security hardening (non-root users, minimal base images)
- Use .dockerignore for clean layer builds
- Define clear healthcheck instructions

## Ollama Model Management

When working with Ollama-related code:

- Verify model names against current installation
- Use exact model names (e.g., `llama3.2`, `qwen3.2-coder:7b`)
- Document model dependencies in appropriate config files
- Ensure consistency across API responses and documentation

## Markdown Files

- Use YAML frontmatter for metadata
- Follow existing documentation patterns
- Include links using Obsidian wikilinks where applicable
- Run markdown linting after creating/editing markdown files

## Project Type

This is a **Python/FastAPI application** with an API-first architecture. All agents must prioritize:

1. Clean, type-safe code
2. Proper async/await usage
3. Comprehensive validation
4. Error handling
5. Documentation (API docs, type hints, docstrings)
