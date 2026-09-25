# Coding agents

[Genie Code](https://docs.databricks.com/aws/en/genie-code/use-genie-code) uses
[Agent Skills](https://docs.databricks.com/aws/en/genie-code/skills) installed
in the Databricks user or workspace folders. Compatible external coding agents
can connect through [Unity Gateway](https://docs.databricks.com/aws/en/ai-gateway/coding-agent-quickstart)
(`ug`).

## Install once

```bash
make install_claudecode
make install_codex
make install_cursorcli
```

Targets are also available for Gemini, OpenCode, Copilot, and Pi:
`install_gemini`, `install_opencode`, `install_copilot`, and `install_pi`.

Unity Gateway is installed in `.uvtools`, separate from `.venv`.

## Launch

```bash
ug claude
ug codex
ug cursor
```

See the [Unity Gateway documentation](https://docs.databricks.com/aws/en/ai-gateway/coding-agent-ug-cli).
