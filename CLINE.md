---
tags: [ai, llm, local, continue, cline]
---

# <img src="https://github.com/continue-dev.png" width="24" style="vertical-align: middle; border-radius: 4px;" /> Cline AI Assistant

Cline is an AI coding assistant that works with local LLMs. It's designed to be a more lightweight alternative to Continue.

## Installation

```shell
brew install cline
```

## Configuration

Cline configuration is typically stored in `~/.cline/config.yaml` or can be managed through the application's settings UI.

## Start / Usage

```shell
# Start Cline server
cline start

# Or launch from the application UI if installed as a GUI app
```

## References

- [Cline GitHub Repository](https://github.com/continue-dev/cline)
- [Cline Documentation](https://docs.cline.ai)

## Related Documentation

For configuration and setup information, see:

- [[AI Tools Configuration (Continue, Cline, OpenCode)]]
- [[Local LLM Setup for AI Coding Assistants (Ollama + LM Studio)]]

## Configuration Example

```yaml
# Example Cline configuration (may vary by version)
models:
  - name: "qwen2.5-coder:7b"
    provider: "lmstudio"
    endpoint: "http://localhost:1234/v1"
```
