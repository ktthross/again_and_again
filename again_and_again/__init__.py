"""again-and-again: Personal utility library for things I do again and again."""

from importlib.metadata import version

from again_and_again.src.git_wizard import get_commit_hash, get_git_repo_root_path
from again_and_again.src.gpu_wizard import get_device
from again_and_again.src.hydra_wizard import get_the_hydra_config_path, load_hydra_config
from again_and_again.src.log_wizard import logging_setup, reset_logging
from again_and_again.src.mlflow_wizard import (
    can_connect_to_databricks,
    experiment_exists,
    load_mlflow_env,
)
from again_and_again.src.path_wizard import (
    create_unique_path_inside_of_a_git_repo,
    normalize_directory_path,
    normalize_file_path,
    path_to_string,
)

__version__ = version("again-and-again")

__all__ = [
    "__version__",
    "normalize_file_path",
    "normalize_directory_path",
    "get_git_repo_root_path",
    "get_commit_hash",
    "get_device",
    "path_to_string",
    "create_unique_path_inside_of_a_git_repo",
    "get_the_hydra_config_path",
    "load_hydra_config",
    "logging_setup",
    "reset_logging",
    "can_connect_to_databricks",
    "experiment_exists",
    "load_mlflow_env",
]
