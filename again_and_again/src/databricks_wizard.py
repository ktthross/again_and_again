"""Databricks session utilities for working with Spark."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyspark.sql import SparkSession

try:
    from databricks.connect import DatabricksSession

    DATABRICKS_AVAILABLE = True
except ImportError:
    DATABRICKS_AVAILABLE = False


def get_spark() -> SparkSession:
    """
    Get a spark session for working with data in Databricks.

    When running inside a Databricks notebook (detected via the
    DATABRICKS_RUNTIME_VERSION environment variable), returns the active
    notebook SparkSession. Otherwise, uses Databricks Connect for local
    development.

    Returns:
        A spark session.

    Raises:
        ImportError: If databricks-connect is not installed. Install with
            `uv add ts-hadean-zircon[databricks]` or `pip install ts-hadean-zircon[databricks]`.
    """
    if os.environ.get("DATABRICKS_RUNTIME_VERSION"):
        # Inside a Databricks notebook — use the active session
        from pyspark.sql import SparkSession

        return SparkSession.builder.getOrCreate()

    if not DATABRICKS_AVAILABLE:
        raise ImportError(
            "databricks-connect is not available. Install with"
            " `uv add ts-hadean-zircon[databricks]`"
            " or `pip install ts-hadean-zircon[databricks]`"
        )

    # Local development using Databricks Connect
    return DatabricksSession.builder.getOrCreate()
