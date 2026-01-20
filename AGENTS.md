# AGENTS.md

This file provides guidelines for AI agents working in this repository.

## Project Overview

GitHub Proxy Switch - A Windows desktop application for managing Git CLI proxy settings using CustomTkinter.

**Tech Stack**: Python 3.10+, CustomTkinter, CTkMessagebox, Pillow
**Main File**: main.py (~360 lines)

## Build / Lint / Test Commands

### Python Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Lint with ruff (if installed)
ruff check .

# Type check with mypy (if installed)
mypy .
```

### Note on Tests
This project currently has no test suite. When adding tests:
```bash
# Run all tests
pytest

# Run single test
pytest tests/test_file.py::TestClass::test_method
```

## Code Style Guidelines

### General Principles
- Write clean, self-documenting code
- Keep functions small and focused (single responsibility)
- Use meaningful variable and function names
- Avoid deep nesting (max 3-4 levels)
- Extract magic numbers into constants

### Imports (Python)
```python
# Standard library imports first
import subprocess
import re
import json
import os

# Third-party imports
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox

# Local imports
# (none in this project)
```

### Types
- Use explicit types for function parameters and return values
- Use `typing` module (Optional, Tuple, Dict, etc.) where appropriate
- Avoid `Any` type; use specific types or `Unknown` instead

### Naming Conventions (Python)
- **Variables/functions**: snake_case
- **Constants**: SCREAMING_SNAKE_CASE (e.g., `HISTORY_FILE`, `MAX_HISTORY`)
- **Classes**: PascalCase (e.g., `ProxySwitchApp`)
- **Private members**: prefix with underscore (e.g., `_action_type`)
- **Files**: lowercase with underscores (e.g., `main.py`, `history.json`)

### Error Handling
- Never swallow errors silently
- Use try-catch blocks only where error recovery is possible
- Return (success, message) tuples or typed errors from functions
- Log errors with sufficient context for debugging
- Show user-friendly messages via CTkMessagebox

### Formatting
- Use 4 spaces for indentation
- Keep line length under 120 characters
- Add blank lines between function definitions
- Use trailing commas in multi-line structures

### Comments
- Comment why, not what (code should be self-explanatory)
- Document public APIs with docstrings
- Add TODO comments with brief descriptions
- Remove commented-out code

### Testing
- Write tests for new functionality
- Use descriptive test names: `test_<function>_<scenario>`
- Follow Arrange-Act-Assert pattern
- Mock external dependencies (git commands, registry access)

## Project-Specific Notes

### Quick Commands
- Run `python main.py` to start the application
- App follows system dark/light theme automatically
- Images are theme-aware: `run-dark.png`, `run-light.png`, etc.

### Key Functions
- `get_git_proxy()` - Read global git proxy config
- `set_git_proxy(proxy_url)` - Set global git proxy
- `unset_git_proxy()` - Remove global git proxy
- `get_system_proxy()` - Read Windows system proxy settings

### UI Components
- Uses CustomTkinter CTk (modern Tkinter wrapper)
- CTkMessagebox for dialogs (not standard messagebox)
- Images loaded via CTkImage with theme suffix support

### Adding New Features
- Follow existing error handling pattern (return tuples)
- Update history.json for address history
- Add theme-aware images if adding new buttons
- Use CTkMessagebox for all user notifications

### Windows-Specific Code
- Uses `winreg` for system proxy access
- Uses `subprocess` for git CLI commands
- Batch files (.bat) use `chcp 65001` for UTF-8

### History File
- Location: `history.json`
- Format: Array of objects with `addr` and `protocol` fields
- Max entries: 10 (defined by `MAX_HISTORY` constant)
- New entries are added to the top, duplicates are removed

### Git Commands Used
- `git config --global --get http.proxy` - Get current proxy
- `git config --global http.proxy <url>` - Set HTTP/HTTPS proxy
- `git config --global https.proxy <url>` - Set HTTPS proxy
- `git config --global --unset http.proxy` - Remove proxy
- `git ls-remote` - Test proxy connectivity

## Cursor Rules
No custom Cursor rules found.

## Copilot Instructions
No custom Copilot instructions found.
