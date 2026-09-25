# Shared fragment: Databricks Unity Gateway CLI (ug) + coding-agent installs.
#
# Targets
#   make direnv              install direnv (brew on macOS, apt on Linux/WSL) and hook the login shell
#   make ug                  install the Unity Gateway CLI (ug) as a uv tool in .uvtools (isolated from .venv)
#   make install_claudecode  install ug + the Claude Code CLI (signed, per-OS)
#   make install_codex       install ug + the Codex CLI (npm)
#   make install_cursorcli   install ug + the Cursor CLI
#   make install_pi          install ug + the Pi CLI (npm)
#   make install_gemini      install ug + the Gemini CLI (brew on macOS, npm on Linux/WSL)
#   make install_opencode    install ug + the OpenCode CLI (brew tap on macOS, npm on Linux/WSL)
#   make install_copilot     install ug + the GitHub Copilot CLI (brew cask on macOS, npm on Linux/WSL)
#   make ug-clean            remove .uvtools
#
# Launch (direnv puts .uvtools/bin on PATH; first run configures the agent against the workspace)
#   ug claude | codex | gemini | opencode | copilot | pi | cursor
#   Cursor is MCP-only: ug registers Databricks MCP servers; models run on your Cursor account.
#   Docs: https://docs.databricks.com/aws/en/ai-gateway/coding-agent-ug-cli
#
# Required software
#   Always:              make, uv (direnv is installed by `make direnv` / `make ug`)
#   macOS install_*:     Homebrew (brew)
#   Linux/WSL install_*: apt (direnv, Claude Code), npm (Codex, Pi, Gemini, OpenCode, Copilot), curl (Cursor CLI)
#
# How to integrate into a project Makefile
#   1. Copy this file next to that Makefile.
#   2. In the project's Makefile, add near the top:  include Makefile.ug.mk
#   3. Gitignore `.uvtools/`.
#   4. Must put `.uvtools/bin` on PATH or `ug` will not run in-repo.
#      In `.envrc`:  PATH_add .uvtools/bin
#      Then once:    direnv allow
#   Standalone (no include):  make -f Makefile.ug.mk ug

MAKEFILE_UG := $(abspath $(lastword $(MAKEFILE_LIST)))

# ANSI colors for progress banners (printf interprets the escapes).
BOLD ?= \033[1m
CYAN ?= \033[36m
GREEN ?= \033[32m
RESET ?= \033[0m
# Sub-step tag: "name i/n".
sub ?= $(1) $(2)/$(3)

# Unity Gateway CLI. Installed into .uvtools (not .venv) so its deps stay isolated from the project.
UG_SPEC ?= git+https://github.com/databricks/unity-gateway
UG_TOOL_DIR ?= .uvtools

.PHONY: direnv _direnv-install-macos _direnv-install-apt \
	ug ug-clean \
	install_claudecode _claudecode-install _claudecode-install-macos _claudecode-install-apt \
	install_codex _codex-install install_cursorcli _cursorcli-install install_pi _pi-install \
	install_gemini _gemini-install install_opencode _opencode-install install_copilot _copilot-install

# ---------------------------------------------------------------------------
# direnv (loads .envrc; puts .uvtools/bin on PATH so `ug ...` works in-repo)
# ---------------------------------------------------------------------------
direnv:
	@printf '$(BOLD)$(CYAN)==> direnv: installing direnv and hooking the login shell...$(RESET)\n'
	@printf '$(CYAN)--> $(call sub,direnv,1,2): ensuring direnv is installed...$(RESET)\n'
	@if command -v direnv >/dev/null; then \
		printf '    already on PATH, skipping package install.\n'; \
	else \
		case "$$(uname -s)" in \
		  Darwin) $(MAKE) -f $(MAKEFILE_UG) _direnv-install-macos ;; \
		  Linux) $(MAKE) -f $(MAKEFILE_UG) _direnv-install-apt ;; \
		  *) echo "ERROR: unsupported OS (need macOS or Linux/WSL with apt)"; exit 1 ;; \
		esac; \
	fi
	@printf '$(CYAN)--> $(call sub,direnv,2,2): hooking the login shell...$(RESET)\n'
	@shell_name=$$(basename "$${SHELL:-}"); \
	case "$$shell_name" in \
	  zsh) rc="$$HOME/.zshrc"; hook=zsh ;; \
	  bash) rc="$$HOME/.bashrc"; hook=bash ;; \
	  *) \
	    if [ "$$(uname -s)" = Darwin ]; then rc="$$HOME/.zshrc"; hook=zsh; \
	    else rc="$$HOME/.bashrc"; hook=bash; fi ;; \
	esac; \
	if grep -qs 'direnv hook' "$$rc" 2>/dev/null; then \
		printf '    hook already in %s.\n' "$$rc"; \
	else \
		printf '\neval "$$(direnv hook %s)"\n' "$$hook" >> "$$rc"; \
		printf '    added hook to %s — start a new shell (or: exec %s) so it loads.\n' "$$rc" "$$hook"; \
	fi
	@if echo " $(MAKECMDGOALS) " | grep -q ' direnv '; then \
		printf '\n$(BOLD)$(GREEN)==> direnv ready.$(RESET)\n'; \
		printf '  Next: open a new shell (so the hook is active), then $(BOLD)direnv allow$(RESET) in the repo.\n\n'; \
	fi

_direnv-install-macos:
	brew install direnv

_direnv-install-apt:
	sudo apt-get update
	sudo apt-get install -y direnv

# ---------------------------------------------------------------------------
# ug (Unity Gateway CLI)
# ---------------------------------------------------------------------------
# Isolated uv tool. UV_TOOL_DIR/UV_TOOL_BIN_DIR keep the environment and its launcher
# inside the repo (.uvtools), so nothing lands in .venv or a user-global uv tool dir.
ug: direnv
	@printf '$(BOLD)$(CYAN)==> ug: installing the Unity Gateway CLI into $(UG_TOOL_DIR)...$(RESET)\n'
	UV_TOOL_DIR="$(abspath $(UG_TOOL_DIR))" UV_TOOL_BIN_DIR="$(abspath $(UG_TOOL_DIR))/bin" uv tool install --force "$(UG_SPEC)"

ug-clean:
	rm -rf $(UG_TOOL_DIR)

# ---------------------------------------------------------------------------
# Claude Code
# ---------------------------------------------------------------------------
install_claudecode: ug _claudecode-install
	@printf '\n$(BOLD)$(GREEN)==> Claude Code ready.$(RESET)\n'
	@printf '  Installed: ug ($(UG_TOOL_DIR)/) + the Claude Code CLI.\n'
	@printf '  Next: launch inside the repo with $(BOLD)ug claude$(RESET) (ug configures it against the workspace on first run).\n\n'

_claudecode-install:
	@printf '$(BOLD)$(CYAN)==> Installing the Claude Code CLI (signed OS package)...$(RESET)\n'
	@case "$$(uname -s)" in \
	  Darwin) $(MAKE) -f $(MAKEFILE_UG) _claudecode-install-macos ;; \
	  Linux) $(MAKE) -f $(MAKEFILE_UG) _claudecode-install-apt ;; \
	  *) echo "ERROR: unsupported OS (need macOS or Linux/WSL with apt)"; exit 1 ;; \
	esac

_claudecode-install-macos:
	brew install --cask claude-code

_claudecode-install-apt:
	sudo install -d -m 0755 /etc/apt/keyrings
	curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | sudo tee /etc/apt/keyrings/claude-code.asc >/dev/null
	echo 'deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main' | sudo tee /etc/apt/sources.list.d/claude-code.list >/dev/null
	sudo apt-get update
	sudo apt-get install -y claude-code

# ---------------------------------------------------------------------------
# Codex CLI
# ---------------------------------------------------------------------------
install_codex: ug _codex-install
	@printf '\n$(BOLD)$(GREEN)==> Codex ready.$(RESET)\n'
	@printf '  Installed: ug ($(UG_TOOL_DIR)/) + the Codex CLI.\n'
	@printf '  Next: launch inside the repo with $(BOLD)ug codex$(RESET) (ug configures it against the workspace on first run).\n\n'

_codex-install:
	@printf '$(BOLD)$(CYAN)==> Installing the Codex CLI (npm)...$(RESET)\n'
	npm install -g @openai/codex

# ---------------------------------------------------------------------------
# Cursor CLI
# ---------------------------------------------------------------------------
install_cursorcli: ug _cursorcli-install
	@printf '\n$(BOLD)$(GREEN)==> Cursor CLI ready.$(RESET)\n'
	@printf '  Installed: ug ($(UG_TOOL_DIR)/) + the Cursor CLI.\n'
	@printf '  Next: launch inside the repo with $(BOLD)ug cursor$(RESET) (MCP-only: ug registers Databricks MCP servers; models run on your Cursor account).\n\n'

_cursorcli-install:
	@printf '$(BOLD)$(CYAN)==> Installing the Cursor CLI...$(RESET)\n'
	@case "$$(uname -s)" in \
	  Darwin) brew install --cask cursor-cli ;; \
	  Linux) curl https://cursor.com/install -fsS | bash ;; \
	  *) echo "ERROR: unsupported OS (need macOS or Linux/WSL)"; exit 1 ;; \
	esac

# ---------------------------------------------------------------------------
# Pi CLI
# ---------------------------------------------------------------------------
install_pi: ug _pi-install
	@printf '\n$(BOLD)$(GREEN)==> Pi ready.$(RESET)\n'
	@printf '  Installed: ug ($(UG_TOOL_DIR)/) + the Pi CLI.\n'
	@printf '  Next: launch inside the repo with $(BOLD)ug pi$(RESET) (ug configures it against the workspace on first run).\n\n'

_pi-install:
	@printf '$(BOLD)$(CYAN)==> Installing the Pi CLI (npm)...$(RESET)\n'
	npm install -g @earendil-works/pi-coding-agent

# ---------------------------------------------------------------------------
# Gemini CLI
# ---------------------------------------------------------------------------
install_gemini: ug _gemini-install
	@printf '\n$(BOLD)$(GREEN)==> Gemini CLI ready.$(RESET)\n'
	@printf '  Installed: ug ($(UG_TOOL_DIR)/) + the Gemini CLI.\n'
	@printf '  Next: launch inside the repo with $(BOLD)ug gemini$(RESET) (ug configures it against the workspace on first run).\n\n'

_gemini-install:
	@printf '$(BOLD)$(CYAN)==> Installing the Gemini CLI...$(RESET)\n'
	@case "$$(uname -s)" in \
	  Darwin) brew install gemini-cli ;; \
	  Linux) npm install -g @google/gemini-cli ;; \
	  *) echo "ERROR: unsupported OS (need macOS or Linux/WSL)"; exit 1 ;; \
	esac

# ---------------------------------------------------------------------------
# OpenCode CLI
# ---------------------------------------------------------------------------
install_opencode: ug _opencode-install
	@printf '\n$(BOLD)$(GREEN)==> OpenCode ready.$(RESET)\n'
	@printf '  Installed: ug ($(UG_TOOL_DIR)/) + the OpenCode CLI.\n'
	@printf '  Next: launch inside the repo with $(BOLD)ug opencode$(RESET) (ug configures it against the workspace on first run).\n\n'

_opencode-install:
	@printf '$(BOLD)$(CYAN)==> Installing the OpenCode CLI...$(RESET)\n'
	@case "$$(uname -s)" in \
	  Darwin) brew install anomalyco/tap/opencode ;; \
	  Linux) npm install -g opencode-ai@1 ;; \
	  *) echo "ERROR: unsupported OS (need macOS or Linux/WSL)"; exit 1 ;; \
	esac

# ---------------------------------------------------------------------------
# GitHub Copilot CLI
# ---------------------------------------------------------------------------
install_copilot: ug _copilot-install
	@printf '\n$(BOLD)$(GREEN)==> GitHub Copilot CLI ready.$(RESET)\n'
	@printf '  Installed: ug ($(UG_TOOL_DIR)/) + the GitHub Copilot CLI.\n'
	@printf '  Next: launch inside the repo with $(BOLD)ug copilot$(RESET) (ug configures it against the workspace on first run).\n\n'

_copilot-install:
	@printf '$(BOLD)$(CYAN)==> Installing the GitHub Copilot CLI...$(RESET)\n'
	@case "$$(uname -s)" in \
	  Darwin) brew install --cask copilot-cli ;; \
	  Linux) npm install -g @github/copilot ;; \
	  *) echo "ERROR: unsupported OS (need macOS or Linux/WSL)"; exit 1 ;; \
	esac
