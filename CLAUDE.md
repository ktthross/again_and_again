# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Install dependencies (uses uv package manager)
uv sync --extra dev

# Run tests
uv run pytest

# Run single test file
uv run pytest tests/test_path_wizard.py

# Run single test
uv run pytest tests/test_path_wizard.py::TestNormalizeFilePath::test_returns_path_object

# Lint and format
uv run ruff check .
uv run ruff format .

# Type checking
uv run mypy again_and_again

# Pre-commit (runs ruff + formatting on staged files)
uv run pre-commit run --all-files
```

## Architecture

This is a utility library with three modules under `again_and_again/src/`:

- **git_wizard.py** - Git repository utilities: finding repo root, getting commit hash
- **gpu_wizard.py** - PyTorch device detection (MPS/CUDA/CPU) with optional torch dependency
- **path_wizard.py** - Path normalization, directory creation, and experiment output paths

All public functions are re-exported from `again_and_again/__init__.py`.

## Code Style

- Line length: 100 characters
- Python 3.10+ (uses union types like `str | Path` instead of `Union`)
- Double quotes for strings
- Ruff handles all linting and formatting with `--unsafe-fixes` enabled
- Type hints required (`py.typed` marker present)

## Optional Dependencies

PyTorch is optional. The `get_device()` function requires installing with:
```bash
pip install again-and-again[torch]
```

The code handles missing torch gracefully with `TORCH_AVAILABLE` flag and `TYPE_CHECKING` imports.
