"""Databricks session utilities for working with Spark."""

from __future__ import annotations

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

    This function will try to initialize a spark sessions presuming that it is
    running inside a Databricks notebook. If it is not, it will try to
    initialize a Databricks session using the Databricks Connect API.

    Returns:
        A spark session.

    Raises:
        ImportError: If databricks-connect is not installed. Install with
            `uv add again-and-again[databricks]` or `pip install again-and-again[databricks]`.
    """
    try:
        # This works if you're inside a Databricks notebook
        from pyspark.sql import SparkSession

        return SparkSession.builder.getOrCreate()
    except ImportError:
        pass

    if not DATABRICKS_AVAILABLE:
        raise ImportError(
            "databricks-connect is not available. Install with"
            " `uv add again-and-again[databricks]`"
            " or `pip install again-and-again[databricks]`"
        )

    # This works for local development using Databricks Connect
    return DatabricksSession.builder.getOrCreate()
