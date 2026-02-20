"""MLflow utilities with Databricks integration."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pathlib

try:
    from mlflow import set_tracking_uri
    from mlflow.exceptions import MlflowException
    from mlflow.tracking import MlflowClient

    MLFLOW_AVAILABLE = True
except ImportError:
    set_tracking_uri = None  # type: ignore[assignment]
    MlflowClient = None  # type: ignore[assignment]
    MlflowException = None  # type: ignore[assignment]
    MLFLOW_AVAILABLE = False

try:
    from dotenv import dotenv_values

    DOTENV_AVAILABLE = True
except ImportError:
    dotenv_values = None  # type: ignore[assignment]
    DOTENV_AVAILABLE = False

_MLFLOW_ENV_VARS = [
    "DATABRICKS_HOST",
    "DATABRICKS_TOKEN",
    "MLFLOW_TRACKING_URI",
    "MLFLOW_EXPERIMENT_ID",
]


def _ensure_mlflow_is_available() -> None:
    """Ensure that mlflow is available."""
    if not MLFLOW_AVAILABLE:
        raise ImportError(
            "mlflow is not available. Install with `uv add again-and-again[mlflow]`"
            " or `pip install again-and-again[mlflow]`"
        )


def load_mlflow_env(dotenv_path: str | pathlib.Path | None = None) -> dict[str, str | None]:
    """
    Load MLflow/Databricks environment variables from a .env file.

    Only DATABRICKS_HOST, DATABRICKS_TOKEN, MLFLOW_TRACKING_URI, and
    MLFLOW_EXPERIMENT_ID are read into the process environment — all other
    variables in the file are ignored.

    Args:
        dotenv_path: Path to the .env file. If None, python-dotenv searches
            upward from the current working directory for a .env file.

    Returns:
        Dict mapping each variable name to its value after loading
        (or None if not present in the file or environment).

    Raises:
        ImportError: If python-dotenv is not installed. Install with
            `uv add again-and-again[mlflow]` or `pip install again-and-again[mlflow]`.

    Example:
        >>> from again_and_again import load_mlflow_env
        >>> env = load_mlflow_env()
        >>> env["DATABRICKS_HOST"]
        'https://myworkspace.azuredatabricks.net'
        >>> env = load_mlflow_env(".env.prod")
    """
    if not DOTENV_AVAILABLE:
        raise ImportError(
            "python-dotenv is not available. Install with `uv add again-and-again[mlflow]`"
            " or `pip install again-and-again[mlflow]`"
        )
    file_values = dotenv_values(dotenv_path)
    for var in _MLFLOW_ENV_VARS:
        if var in file_values and file_values[var] is not None:
            os.environ[var] = file_values[var]  # type: ignore[assignment]
    return {var: os.environ.get(var) for var in _MLFLOW_ENV_VARS}


def _experiment_exists_input_checking(
    experiment_name: str | None = None, experiment_id: str | None = None
) -> tuple[str | None, str | None]:
    """
    Perform checking to ensure that the function is called with valid arguments.
    """
    _ensure_mlflow_is_available()
    if experiment_name is None and experiment_id is None:
        raise ValueError("One of experiment_name or experiment_id must be provided.")
    if experiment_name is not None and experiment_id is not None:
        raise ValueError("Provide only one of experiment_name or experiment_id, not both.")
    return experiment_name, experiment_id


def experiment_exists(
    experiment_name: str | None = None,
    experiment_id: str | None = None,
) -> bool:
    """
    Check whether an MLflow experiment exists on the tracking server.

    This is a read-only check — no runs are created or modified.
    Exactly one of experiment_name or experiment_id must be provided.

    Args:
        experiment_name: Name of the experiment to look up.
        experiment_id: ID of the experiment to look up.

    Returns:
        True if the experiment exists, False if it does not.

    Raises:
        ImportError: If mlflow is not installed. Install with
            `uv add again-and-again[mlflow]` or `pip install again-and-again[mlflow]`.
        ValueError: If neither or both of experiment_name/experiment_id are provided.
        mlflow.exceptions.MlflowException: If the lookup fails for any reason
            other than the experiment not existing (e.g. auth failure).

    Example:
        >>> from again_and_again import experiment_exists
        >>> experiment_exists(experiment_name="my-training-run")
        True
        >>> experiment_exists(experiment_id="123456789")
        False
    """
    experiment_name, experiment_id = _experiment_exists_input_checking(
        experiment_name, experiment_id
    )
    client = MlflowClient()

    if experiment_name is not None:
        return client.get_experiment_by_name(experiment_name) is not None

    try:
        client.get_experiment(experiment_id)
        return True
    except MlflowException as e:
        if e.error_code == "RESOURCE_DOES_NOT_EXIST":
            return False
        raise


def can_connect_to_databricks(tracking_uri: str | None = None) -> bool:
    """
    Test whether a connection to a Databricks MLflow tracking server can be established.

    Uses the provided tracking_uri, or falls back to the MLFLOW_TRACKING_URI
    environment variable / mlflow's configured default.

    Args:
        tracking_uri: Databricks workspace URL, e.g. "databricks" or
            "https://<workspace>.azuredatabricks.net". If None, uses the
            currently configured tracking URI.

    Returns:
        True if the connection succeeds.

    Raises:
        ImportError: If mlflow is not installed. Install with
            `uv add again-and-again[mlflow]` or `pip install again-and-again[mlflow]`.
        mlflow.exceptions.MlflowException: If the connection fails.

    Example:
        >>> from again_and_again import can_connect_to_databricks
        >>> can_connect_to_databricks()
        True
        >>> can_connect_to_databricks("https://myworkspace.azuredatabricks.net")
        True
    """
    _ensure_mlflow_is_available()
    if tracking_uri is not None:
        set_tracking_uri(tracking_uri)

    client = MlflowClient()
    client.search_experiments(max_results=1)
    return True
