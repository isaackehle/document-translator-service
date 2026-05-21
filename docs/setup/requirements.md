


uv add -r requirements.txt

To update dependencies managed in pyproject.toml using uv, run:

```shell
uv lock --upgrade
```

This updates all dependencies to their latest compatible versions based on constraints in pyproject.toml, then regenerates uv.lock with the new resolved versions. For selective updates, use:

```shell
uv lock --upgrade-package requests
```

To keep requirements.txt in sync with pyproject.toml and uv.lock, treat the .toml and .lock files as the source of truth and generate requirements.txt as needed:

```shell
uv export --format requirements-txt > requirements.txt
```

This exports a pip-compatible requirements.txt from uv.lock, ensuring exact pinned versions are reflected. Use this when required for deployment (e.g., Docker, CI/CD), but do not manually edit or maintain requirements.txt—always regenerate it from the lockfile to stay in sync.
