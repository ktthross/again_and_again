# again-and-again

A personal utility library for things I do again and again.

[![CI](https://github.com/ktthross/again_and_again/actions/workflows/ci.yml/badge.svg)](https://github.com/ktthross/again_and_again/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/again-and-again.svg)](https://badge.fury.io/py/again-and-again)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Installation

```bash
# Using uv (recommended)
uv add again-and-again

# Using pip
pip install again-and-again
```

For optional features:

```bash
# GPU device detection (requires PyTorch)
uv add again-and-again[torch]
# pip install again-and-again[torch]

# Hydra configuration utilities
uv add again-and-again[hydra]
# pip install again-and-again[hydra]

# Logging setup with loguru
uv add again-and-again[logging]
# pip install again-and-again[logging]

# MLflow + Databricks utilities
uv add ts-hadean-zircon[mlflow]
# pip install ts-hadean-zircon[mlflow]
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

### Logging Utilities

Set up structured logging with loguru:

```python
from again_and_again import logging_setup
from loguru import logger

# Set up logging to stdout and a file
logging_setup("logs/app.log", log_level="DEBUG")

# Automatically intercepts torch and hydra logging
logger.info("Application started")

# Intercept specific loggers
logging_setup(
    "logs/app.log",
    intercept_loggers=["torch", "transformers", "matplotlib"]
)

# Intercept all standard logging
logging_setup("logs/app.log", intercept_loggers=[])
```

### Hydra Configuration Utilities

Load Hydra configurations:

```python
from again_and_again import load_hydra_config, get_the_hydra_config_path

# Get the config directory path
config_path = get_the_hydra_config_path()  # Returns {repo_root}/conf

# Load a Hydra config as a dictionary
config = load_hydra_config("train_config")

# Load with overrides
config = load_hydra_config(
    "train_config",
    overrides=["batch_size=32", "learning_rate=0.001"]
)

# Load from custom directory
config = load_hydra_config(
    "my_config",
    config_dir="/path/to/configs"
)
```

### MLflow Utilities

Load MLflow/Databricks environment variables from a `.env` file:

```python
from ts_hadean_zircon import load_mlflow_env

# Load from default location
env = load_mlflow_env()

# Load from a specific path
env = load_mlflow_env(".env.databricks")
# Returns dict with keys: DATABRICKS_HOST, DATABRICKS_TOKEN,
#                         MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_ID
```

**Test connectivity** to a Databricks MLflow tracking server:

```python
from ts_hadean_zircon import can_connect_to_databricks

# Uses MLFLOW_TRACKING_URI env var
connected = can_connect_to_databricks()

# Or provide the URI directly
connected = can_connect_to_databricks(tracking_uri="https://my-workspace.azuredatabricks.net")
```

**Check whether an MLflow experiment exists**:

```python
from ts_hadean_zircon import experiment_exists

# Look up by name
exists = experiment_exists(experiment_name="my-experiment")

# Look up by ID
exists = experiment_exists(experiment_id="123456789")
```

## API Reference

| Function | Description |
| -------- | ----------- |
| `normalize_file_path(path, path_should_exist=False, make_parent_path=True)` | Normalize and resolve a file path |
| `normalize_directory_path(path, make_path=True)` | Normalize and resolve a directory path |
| `path_to_string(source)` | Convert a Path to string |
| `get_git_repo_root_path()` | Get the git repository root |
| `get_commit_hash()` | Get current HEAD commit hash |
| `create_unique_path_inside_of_a_git_repo(output_namespace=None)` | Create timestamped output directory |
| `get_device(override=None)` | Get optimal PyTorch device |
| `logging_setup(log_file, log_level, intercept_standard_logging, intercept_loggers)` | Configure loguru logging |
| `reset_logging()` | Reset logging configuration |
| `get_the_hydra_config_path()` | Get path to Hydra config directory |
| `load_hydra_config(config_name, overrides, config_dir)` | Load Hydra config as dictionary |
| `load_mlflow_env(dotenv_path=None)` | Load MLflow/Databricks env vars from a .env file |
| `can_connect_to_databricks(tracking_uri=None)` | Test connectivity to a Databricks MLflow server |
| `experiment_exists(experiment_name=None, experiment_id=None)` | Check whether an MLflow experiment exists |

## Development

```bash
# Clone the repository
git clone https://github.com/ktthross/again_and_again.git
cd again_and_again

# Install with dev dependencies
uv sync --extra dev
# pip install -e ".[dev]"

# Run tests
uv run pytest
# pytest

# Run linter
uv run ruff check .
# ruff check .

# Run formatter
uv run ruff format .
# ruff format .

# Run type checker
uv run mypy again_and_again
# mypy again_and_again
```

## License

MIT License - see [LICENSE](LICENSE) for details.
