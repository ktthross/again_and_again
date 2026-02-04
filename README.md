# again-and-again

A personal utility library for things I do again and again.

[![CI](https://github.com/ktthross/again_and_again/actions/workflows/ci.yml/badge.svg)](https://github.com/ktthross/again_and_again/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/again-and-again.svg)](https://badge.fury.io/py/again-and-again)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Installation

```bash
pip install again-and-again
```

For GPU device detection (requires PyTorch):

```bash
pip install again-and-again[torch]
```

## Features

### Path Utilities

**Normalize file paths** with automatic parent directory creation:

```python
from again_and_again import normalize_file_path

# Creates parent directories and returns resolved Path
path = normalize_file_path("data/output/results.json")

# Validate that a file exists
path = normalize_file_path("config.yaml", path_should_exist=True)
```

**Normalize directory paths**:

```python
from again_and_again import normalize_directory_path

# Creates the directory if it doesn't exist
output_dir = normalize_directory_path("data/processed")
```

**Convert paths to strings**:

```python
from again_and_again import path_to_string
from pathlib import Path

path_str = path_to_string(Path("./data"))  # Returns absolute path string
```

### Git Utilities

**Get the repository root**:

```python
from again_and_again import get_git_repo_root_path

repo_root = get_git_repo_root_path()  # Returns Path to git repo root
```

**Get the current commit hash**:

```python
from again_and_again import get_commit_hash

commit = get_commit_hash()  # Returns 40-character SHA-1 hash
```

**Create unique output directories** for experiment tracking:

```python
from again_and_again import create_unique_path_inside_of_a_git_repo

# Creates: {repo}/outputs/2024-01-15/14-30-45/{commit_hash}/
output_path = create_unique_path_inside_of_a_git_repo()

# Custom namespace
output_path = create_unique_path_inside_of_a_git_repo("experiments")
```

### GPU Device Detection

Automatically select the best available compute device:

```python
from again_and_again import get_device

# Auto-detect: MPS (Apple Silicon) > CUDA > CPU
device = get_device()

# Force a specific device
device = get_device(override="cpu")
device = get_device(override="cuda")
device = get_device(override="mps")
```

## API Reference

| Function | Description |
|----------|-------------|
| `normalize_file_path(path, path_should_exist=False, make_parent_path=True)` | Normalize and resolve a file path |
| `normalize_directory_path(path, make_path=True)` | Normalize and resolve a directory path |
| `path_to_string(source)` | Convert a Path to string |
| `get_git_repo_root_path()` | Get the git repository root |
| `get_commit_hash()` | Get current HEAD commit hash |
| `create_unique_path_inside_of_a_git_repo(output_namespace=None)` | Create timestamped output directory |
| `get_device(override=None)` | Get optimal PyTorch device |

## Development

```bash
# Clone the repository
git clone https://github.com/ktthross/again_and_again.git
cd again_and_again

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check .

# Run formatter
ruff format .

# Run type checker
mypy again_and_again
```

## License

MIT License - see [LICENSE](LICENSE) for details.
