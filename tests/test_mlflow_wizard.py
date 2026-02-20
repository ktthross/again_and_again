"""Tests for mlflow_wizard module."""

import pytest

from again_and_again import can_connect_to_databricks, experiment_exists, load_mlflow_env

_MLFLOW_CLIENT = "again_and_again.src.mlflow_wizard.MlflowClient"
_MLFLOW_SET_URI = "again_and_again.src.mlflow_wizard.set_tracking_uri"
_MLFLOW_AVAILABLE = "again_and_again.src.mlflow_wizard.MLFLOW_AVAILABLE"


class TestCanConnectToDatabricks:
    """Tests for can_connect_to_databricks function."""

    def test_raises_import_error_without_mlflow(self) -> None:
        """Should raise ImportError when mlflow is not available."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.mlflow_wizard.MLFLOW_AVAILABLE", False),
            pytest.raises(ImportError, match="mlflow is not available"),
        ):
            can_connect_to_databricks()

    def test_returns_true_on_success(self) -> None:
        """Should return True when the tracking server responds."""
        try:
            import mlflow  # noqa: F401
        except ImportError:
            pytest.skip("mlflow not installed")

        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.search_experiments.return_value = []

        with patch(_MLFLOW_CLIENT, return_value=mock_client):
            result = can_connect_to_databricks()

        assert result is True

    def test_sets_tracking_uri_when_provided(self) -> None:
        """Should call mlflow.set_tracking_uri when tracking_uri is given."""
        try:
            import mlflow  # noqa: F401
        except ImportError:
            pytest.skip("mlflow not installed")

        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.search_experiments.return_value = []

        with (
            patch(_MLFLOW_SET_URI) as mock_set_uri,
            patch(_MLFLOW_CLIENT, return_value=mock_client),
        ):
            can_connect_to_databricks("https://myworkspace.azuredatabricks.net")

        mock_set_uri.assert_called_once_with("https://myworkspace.azuredatabricks.net")

    def test_does_not_set_tracking_uri_when_none(self) -> None:
        """Should not call mlflow.set_tracking_uri when tracking_uri is None."""
        try:
            import mlflow  # noqa: F401
        except ImportError:
            pytest.skip("mlflow not installed")

        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.search_experiments.return_value = []

        with (
            patch(_MLFLOW_SET_URI) as mock_set_uri,
            patch(_MLFLOW_CLIENT, return_value=mock_client),
        ):
            can_connect_to_databricks()

        mock_set_uri.assert_not_called()

    def test_propagates_mlflow_exception(self) -> None:
        """Should propagate MlflowException when the connection fails."""
        try:
            from mlflow.exceptions import MlflowException
        except ImportError:
            pytest.skip("mlflow not installed")

        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.search_experiments.side_effect = MlflowException("connection refused")

        with (
            patch(_MLFLOW_CLIENT, return_value=mock_client),
            pytest.raises(MlflowException, match="connection refused"),
        ):
            can_connect_to_databricks()

    def test_import_from_package(self) -> None:
        """Should be importable from the top-level package."""
        from again_and_again import can_connect_to_databricks as fn

        assert callable(fn)


_DOTENV_VALUES = "again_and_again.src.mlflow_wizard.dotenv_values"


class TestLoadMlflowEnv:
    """Tests for load_mlflow_env function."""

    def test_raises_import_error_without_dotenv(self) -> None:
        """Should raise ImportError when python-dotenv is not available."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.mlflow_wizard.DOTENV_AVAILABLE", False),
            pytest.raises(ImportError, match="python-dotenv is not available"),
        ):
            load_mlflow_env()

    def test_returns_dict_with_all_four_keys(self) -> None:
        """Returned dict should always contain all four variable names as keys."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.mlflow_wizard.DOTENV_AVAILABLE", True),
            patch(_DOTENV_VALUES, return_value={}),
        ):
            result = load_mlflow_env()

        assert set(result.keys()) == {
            "DATABRICKS_HOST",
            "DATABRICKS_TOKEN",
            "MLFLOW_TRACKING_URI",
            "MLFLOW_EXPERIMENT_ID",
        }

    def test_returns_none_for_unset_vars(self) -> None:
        """Should return None for vars not present in file or environment."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.mlflow_wizard.DOTENV_AVAILABLE", True),
            patch(_DOTENV_VALUES, return_value={}),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = load_mlflow_env()

        assert all(v is None for v in result.values())

    def test_loads_vars_from_file_into_environment(self) -> None:
        """Should set the four vars in os.environ from the parsed file values."""
        import os
        from unittest.mock import patch

        file_values = {
            "DATABRICKS_HOST": "https://myworkspace.azuredatabricks.net",
            "DATABRICKS_TOKEN": "dapi123",
            "MLFLOW_TRACKING_URI": "databricks",
            "MLFLOW_EXPERIMENT_ID": "42",
            "SOME_OTHER_VAR": "should-be-ignored",
        }

        with (
            patch("again_and_again.src.mlflow_wizard.DOTENV_AVAILABLE", True),
            patch(_DOTENV_VALUES, return_value=file_values),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = load_mlflow_env()
            assert os.environ.get("SOME_OTHER_VAR") is None

        assert result["DATABRICKS_HOST"] == "https://myworkspace.azuredatabricks.net"
        assert result["DATABRICKS_TOKEN"] == "dapi123"
        assert result["MLFLOW_TRACKING_URI"] == "databricks"
        assert result["MLFLOW_EXPERIMENT_ID"] == "42"

    def test_passes_dotenv_path_to_dotenv_values(self) -> None:
        """Should forward the dotenv_path argument to dotenv_values."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.mlflow_wizard.DOTENV_AVAILABLE", True),
            patch(_DOTENV_VALUES, return_value={}) as mock_dv,
        ):
            load_mlflow_env(".env.prod")

        mock_dv.assert_called_once_with(".env.prod")

    def test_uses_none_path_by_default(self) -> None:
        """Should call dotenv_values with None when no path is given."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.mlflow_wizard.DOTENV_AVAILABLE", True),
            patch(_DOTENV_VALUES, return_value={}) as mock_dv,
        ):
            load_mlflow_env()

        mock_dv.assert_called_once_with(None)

    def test_import_from_package(self) -> None:
        """Should be importable from the top-level package."""
        from again_and_again import load_mlflow_env as fn

        assert callable(fn)


class TestExperimentExists:
    """Tests for experiment_exists function."""

    def test_raises_import_error_without_mlflow(self) -> None:
        """Should raise ImportError when mlflow is not available."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.mlflow_wizard.MLFLOW_AVAILABLE", False),
            pytest.raises(ImportError, match="mlflow is not available"),
        ):
            experiment_exists(experiment_name="test")

    def test_raises_value_error_if_neither_provided(self) -> None:
        """Should raise ValueError when no identifier is given."""
        from unittest.mock import patch

        with (
            patch(_MLFLOW_AVAILABLE, True),
            pytest.raises(ValueError, match="One of experiment_name or experiment_id"),
        ):
            experiment_exists()

    def test_raises_value_error_if_both_provided(self) -> None:
        """Should raise ValueError when both identifiers are given."""
        from unittest.mock import patch

        with (
            patch(_MLFLOW_AVAILABLE, True),
            pytest.raises(ValueError, match="only one"),
        ):
            experiment_exists(experiment_name="foo", experiment_id="123")

    def test_returns_true_when_found_by_name(self) -> None:
        """Should return True when get_experiment_by_name finds the experiment."""
        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.get_experiment_by_name.return_value = MagicMock()  # non-None

        with (
            patch(_MLFLOW_AVAILABLE, True),
            patch(_MLFLOW_CLIENT, return_value=mock_client),
        ):
            result = experiment_exists(experiment_name="my-experiment")

        assert result is True
        mock_client.get_experiment_by_name.assert_called_once_with("my-experiment")

    def test_returns_false_when_not_found_by_name(self) -> None:
        """Should return False when get_experiment_by_name returns None."""
        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.get_experiment_by_name.return_value = None

        with (
            patch(_MLFLOW_AVAILABLE, True),
            patch(_MLFLOW_CLIENT, return_value=mock_client),
        ):
            result = experiment_exists(experiment_name="missing")

        assert result is False

    def test_returns_true_when_found_by_id(self) -> None:
        """Should return True when get_experiment succeeds."""
        from unittest.mock import MagicMock, patch

        mock_client = MagicMock()
        mock_client.get_experiment.return_value = MagicMock()

        with (
            patch(_MLFLOW_AVAILABLE, True),
            patch(_MLFLOW_CLIENT, return_value=mock_client),
        ):
            result = experiment_exists(experiment_id="42")

        assert result is True
        mock_client.get_experiment.assert_called_once_with("42")

    def test_returns_false_when_not_found_by_id(self) -> None:
        """Should return False when get_experiment raises RESOURCE_DOES_NOT_EXIST."""
        from unittest.mock import MagicMock, patch

        try:
            from mlflow.exceptions import MlflowException
        except ImportError:
            pytest.skip("mlflow not installed")

        not_found = MlflowException("not found", error_code="RESOURCE_DOES_NOT_EXIST")
        mock_client = MagicMock()
        mock_client.get_experiment.side_effect = not_found

        with patch(_MLFLOW_CLIENT, return_value=mock_client):
            result = experiment_exists(experiment_id="99")

        assert result is False

    def test_propagates_other_mlflow_exception_by_id(self) -> None:
        """Should re-raise MlflowException for errors other than not-found."""
        from unittest.mock import MagicMock, patch

        try:
            from mlflow.exceptions import MlflowException
        except ImportError:
            pytest.skip("mlflow not installed")

        auth_error = MlflowException("permission denied", error_code="PERMISSION_DENIED")
        mock_client = MagicMock()
        mock_client.get_experiment.side_effect = auth_error

        with (
            patch(_MLFLOW_CLIENT, return_value=mock_client),
            pytest.raises(MlflowException, match="permission denied"),
        ):
            experiment_exists(experiment_id="42")

    def test_import_from_package(self) -> None:
        """Should be importable from the top-level package."""
        from again_and_again import experiment_exists as fn

        assert callable(fn)
