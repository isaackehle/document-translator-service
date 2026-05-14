# Contributing to AI Document Translator

Thanks for your interest in contributing! 🙌 This guide covers everything you need to set up, develop, test, and submit changes.

## 📦 Dependency Management & Setup

### ✅ First-time setup

```bash
# Install in editable mode (creates dev environment)
pip install -e ".[dev]"  # if you have optional dev dependencies

# Or just core dependencies:
pip install -e .
```

> ⚠️ Important: Your pyproject.toml currently uses setuptools as the build backend (not Hatch). Make sure it has this block at the top:

```shell
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
```

### 🔄 Keeping requirements.txt in sync

Since we use `pyproject.toml` as the source of truth, regenerate `requirements.txt` after changing dependencies:

1. Install or sync environment (ensures exact versions resolved)

```shell
   pip install -e .
```

2. Export current install to requirements.txt (pins exact versions)

```shell
   pip freeze > requirements.txt
```

> 💡 Tip: Run git diff requirements.txt to see what changed — useful for auditing.

### ❌ Avoid

- Don’t run `pip install -r requirements.txt` in development — it bypasses `pyproject.toml`’s resolution and can cause version conflicts.
- Don’t manually edit `requirements.txt` unless you know exactly what you’re doing.

### 🔧 Tools We Use

| Tool                    | Purpose                                                    | Docs            |
| ----------------------- | ---------------------------------------------------------- | --------------- |
| setuptools              | Build backend (described in pyproject.toml [build-system]) | PEP 621         |
| ruff                    | Fast Python linter + formatter                             | ruff docs       |
| pyright                 | Type checking                                              | pyright docs    |
| pytest + pytest-asyncio | Testing (async support)                                    | pytest docs     |
| localstack              | Local AWS-compatible services (S3, etc.)                   | LocalStack docs |

## 🚀 Contributing Workflow

1. Create a branch: `git checkout -b feat/add-s3-upload`
2. Update `pyproject.toml` if adding deps (e.g., boto3 for S3)
3. Run:

```shell
pip install -e .
pip freeze > requirements.txt
```

4. Add tests in `tests/`
5. Lint & test:

```shell
ruff check . && ruff format . --diff  # preview formatting
pytest
```

6. Commit with conventional message (e.g., `feat(s3): add localstack-based upload`)

## 🐳 LocalStack + S3 Testing Setup

To test S3 uploads without hitting AWS, we use LocalStack (a local AWS emulator).

### Option A: Use Docker Compose (recommended)

1. Create docker-compose.yml:

```yaml
version: '3.8'
services:
  localstack:
    container_name: ai-doc-translator-localstack
    image: localstack/localstack:latest
    ports:
      - '4566:4566' # LocalStack gateway
      - '4510-4559:4510-4559' # external services port range
    environment:
      - AWS_DEFAULT_REGION=us-east-2
      - DEBUG=1
      - DOCKER_ENDPOINT=unix:///var/run/docker.sock
    volumes:
      - '${TMPDIR:-/tmp/localstack}:/var/lib/localstack'
      - './.localstack/init-scripts:/docker-entrypoint-initaws.d'
    init: true
```

2. Create init script: `.localstack/init-scripts/01-create-bucket.sh`

```shell
#!/bin/bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://ai-doc-translator
```

> Make it executable: `chmod +x .localstack/init-scripts/01-create-bucket.sh`

3. Start LocalStack:

```shell
docker-compose up -d
```

4. Verify:

```shell
aws --endpoint-url=http://localhost:4566 s3 ls
# Should show: ai-doc-translator
```

### Option B: Use localstack CLI (if installed)

```shell
# Install (if needed)
pip install localstack

# Start
localstack start
```

> ⚠️ CLI mode requires DOCKER_ENDPOINT and Docker access — Docker Compose is simpler for most devs.

## 📋 Use in code

When writing S3 tests or code, always use:

```python
import boto3
from botocore.client import Config
import os

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-2"),
        config=Config(signature_version="s3v4"),
    )
```

### 🧹 Pre-commit Hooks & Makefile

We use pre-commit to enforce formatting, linting, and safety checks before commits.

1. Install pre-commit

```shell
pip install pre-commit
pre-commit install
```

2. Add `.pre-commit-config.yaml` to root:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: [--maxkb=1024]
```

3. Makefile (optional but helpful)

```makefile
.PHONY: setup test lint format docker-up docker-down

setup:
	pip install -e ".[dev]"
	pip install pre-commit
	pre-commit install

test:
	pytest -ra

lint:
	ruff check .

format:
	ruff format .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down --remove-orphans
```

Then run:

```shell
make setup       # install everything once
make test        # run tests
make lint        # check linting
make format      # auto-format
make docker-up   # start LocalStack
```

## Style Guide

- Commit messages: Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- Code style: `ruff format` (Black-compatible)
- Type hints: Required for public APIs (checked by `pyright`)
- Tests: Use `pytest`, async tests with `pytest-asyncio`, and mock S3 with LocalStack

## 🤝 Questions?

Open an issue or tag [@isaackehle](https://github.com/isaackehle) in your PR. We’ll help you get unstuck!

🛠️ EOF
