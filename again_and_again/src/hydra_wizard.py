"""Hydra configuration utilities for managing experiment configs."""

from __future__ import annotations

import argparse
import pathlib
from typing import TYPE_CHECKING, Any

from again_and_again.src.git_wizard import get_git_repo_root_path

if TYPE_CHECKING:
    import hydra
    from omegaconf import DictConfig

try:
    import hydra
    from omegaconf import DictConfig, OmegaConf

    HYDRA_AVAILABLE = True
except ImportError:
    HYDRA_AVAILABLE = False


def _parse_hydra_argv(argv: list[str]) -> tuple[str | None, list[str], str | None]:
    """Parse Hydra-style CLI args from a list of strings.

    Recognizes --config-name / --config_name / -cn and --config-dir / --config_dir / -cd.
    All remaining arguments are returned as Hydra overrides.

    Args:
        argv: Argument list to parse (e.g. sys.argv[1:]).

    Returns:
        Tuple of (config_name, overrides, config_dir), where any unrecognized
        arguments are collected into overrides.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config-name", "--config_name", "-cn", dest="config_name", default=None)
    parser.add_argument("--config-dir", "--config_dir", "-cd", dest="config_dir", default=None)
    namespace, overrides = parser.parse_known_args(argv)
    return namespace.config_name, overrides, namespace.config_dir


def get_the_hydra_config_path() -> pathlib.Path:
    """
    Get the path to the directory where Hydra stores the configuration files.

    Returns:
        Path to the conf directory in the git repository root.
    """
    return pathlib.Path(get_git_repo_root_path() / "conf")


def load_hydra_config(
    config_name: str | None,
    overrides: list[str] | None = None,
    config_dir: pathlib.Path | str | None = None,
    argv: list[str] | None = None,
) -> dict[str, Any]:
    """
    Load and return a Hydra configuration as a dictionary.

    Args:
        config_name: Name of the config file to load (without .yaml extension).
            Required; may be supplied via argv instead (--config-name / -cn).
        overrides: List of Hydra override strings (e.g., ["param=value"]).
        config_dir: Path to the directory containing config files.
            If None, uses get_the_hydra_config_path().
        argv: Argument list to parse for CLI flags (e.g. sys.argv[1:]).
            Supports --config-name / -cn and --config-dir / -cd; remaining
            arguments are treated as Hydra overrides and prepended to `overrides`.
            Explicit kwargs take precedence over values parsed from argv.

    Returns:
        Dictionary containing the resolved configuration.

    Raises:
        ImportError: If Hydra is not installed. Install with
            `uv add again-and-again[hydra]`.
        TypeError: If OmegaConf.to_container doesn't return a dict.

    Example:
        >>> config = load_hydra_config("train_config", overrides=["batch_size=32"])
        >>> # Read config name and overrides from the command line:
        >>> import sys
        >>> config = load_hydra_config(argv=sys.argv[1:])
    """
    if not HYDRA_AVAILABLE:
        raise ImportError(
            "hydra-core is not available. Install with `uv add again-and-again[hydra]`"
        )

    cli_config_name: str | None = None
    cli_overrides: list[str] = []
    cli_config_dir: str | None = None
    if argv is not None:
        cli_config_name, cli_overrides, cli_config_dir = _parse_hydra_argv(argv)

    resolved_config_name = config_name or cli_config_name
    resolved_overrides = cli_overrides + (overrides or [])
    resolved_config_dir = config_dir or (pathlib.Path(cli_config_dir) if cli_config_dir else None)

    if resolved_config_dir is None:
        hydra_config_path = get_the_hydra_config_path()
    else:
        hydra_config_path = pathlib.Path(resolved_config_dir)

    with hydra.initialize_config_dir(version_base=None, config_dir=str(hydra_config_path)):
        dict_cfg: DictConfig = hydra.compose(
            config_name=resolved_config_name, overrides=resolved_overrides or None
        )
        raw_hydra_config_dictionary = OmegaConf.to_container(dict_cfg, resolve=True)
        if not isinstance(raw_hydra_config_dictionary, dict):
            msg = "Expected a dictionary from OmegaConf.to_container"
            raise TypeError(msg)
        return raw_hydra_config_dictionary
