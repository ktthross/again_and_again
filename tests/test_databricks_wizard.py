"""Tests for databricks_wizard module."""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

from again_and_again import get_spark

_DATABRICKS_AVAILABLE = "again_and_again.src.databricks_wizard.DATABRICKS_AVAILABLE"
_DATABRICKS_SESSION = "again_and_again.src.databricks_wizard.DatabricksSession"


class TestGetSpark:
    """Tests for get_spark function."""

    def test_raises_import_error_without_databricks_connect(self) -> None:
        """Should raise ImportError when databricks-connect is not available
        and not in a notebook.
        """
        env = {k: v for k, v in os.environ.items() if k != "DATABRICKS_RUNTIME_VERSION"}
        with (
            patch.dict("os.environ", env, clear=True),
            patch(_DATABRICKS_AVAILABLE, False),
            pytest.raises(ImportError, match="databricks-connect is not available"),
        ):
            get_spark()

    def test_uses_databricks_connect_when_available(self) -> None:
        """Should call DatabricksSession.builder.getOrCreate() for local dev (not in a notebook)."""
        try:
            from databricks.connect import DatabricksSession  # noqa: F401
        except ImportError:
            pytest.skip("databricks-connect not installed")

        mock_session = MagicMock()
        mock_builder = MagicMock()
        mock_builder.getOrCreate.return_value = mock_session

        env = {k: v for k, v in os.environ.items() if k != "DATABRICKS_RUNTIME_VERSION"}
        with (
            patch.dict("os.environ", env, clear=True),
            patch(_DATABRICKS_SESSION) as mock_cls,
        ):
            mock_cls.builder = mock_builder
            result = get_spark()

        mock_builder.getOrCreate.assert_called_once()
        assert result is mock_session

    def test_uses_spark_session_inside_databricks_notebook(self) -> None:
        """Should call SparkSession.builder.getOrCreate() when DATABRICKS_RUNTIME_VERSION is set."""
        mock_session = MagicMock()
        mock_spark_cls = MagicMock()
        mock_spark_cls.builder.getOrCreate.return_value = mock_session

        # Inject a mock pyspark.sql module so the local import inside get_spark succeeds
        mock_pyspark_sql = MagicMock()
        mock_pyspark_sql.SparkSession = mock_spark_cls

        with (
            patch.dict("os.environ", {"DATABRICKS_RUNTIME_VERSION": "14.3"}),
            patch.dict(sys.modules, {"pyspark": MagicMock(), "pyspark.sql": mock_pyspark_sql}),
        ):
            result = get_spark()

        mock_spark_cls.builder.getOrCreate.assert_called_once()
        assert result is mock_session
