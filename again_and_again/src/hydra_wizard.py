"""Hydra configuration utilities for managing experiment configs."""

from __future__ import annotations

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


def get_the_hydra_config_path() -> pathlib.Path:
    """
    Get the path to the directory where Hydra stores the configuration files.

    Returns:
        Path to the conf directory in the git repository root.
    """
    return pathlib.Path(get_git_repo_root_path() / "conf")


def load_hydra_config(
    config_name: str = "development_config",
    overrides: list[str] | None = None,
    config_dir: pathlib.Path | str | None = None,
) -> dict[str, Any]:
    """
    Load and return a Hydra configuration as a dictionary.

    Args:
        config_name: Name of the config file to load (without .yaml extension).
            Default is "development_config".
        overrides: List of Hydra override strings (e.g., ["param=value"]).
        config_dir: Path to the directory containing config files.
            If None, uses get_the_hydra_config_path().

    Returns:
        Dictionary containing the resolved configuration.

    Raises:
        ImportError: If Hydra is not installed. Install with
            `pip install again-and-again[hydra]`.
        TypeError: If OmegaConf.to_container doesn't return a dict.

    Example:
        >>> config = load_hydra_config("train_config", overrides=["batch_size=32"])
    """
    if not HYDRA_AVAILABLE:
        raise ImportError(
            "hydra-core is not available. Install with `pip install again-and-again[hydra]`"
        )

    if config_dir is None:
        hydra_config_path = get_the_hydra_config_path()
    else:
        hydra_config_path = pathlib.Path(config_dir)

    with hydra.initialize_config_dir(version_base=None, config_dir=str(hydra_config_path)):
        dict_cfg: DictConfig = hydra.compose(config_name=config_name, overrides=overrides)
        raw_hydra_config_dictionary = OmegaConf.to_container(dict_cfg, resolve=True)
        if not isinstance(raw_hydra_config_dictionary, dict):
            msg = "Expected a dictionary from OmegaConf.to_container"
            raise TypeError(msg)
        return raw_hydra_config_dictionary
