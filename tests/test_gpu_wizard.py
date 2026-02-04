"""Tests for gpu_wizard module."""

import pytest

from again_and_again import get_device


class TestGetDevice:
    """Tests for get_device function."""

    def test_returns_device_object(self) -> None:
        """Should return a torch.device object."""
        # This test requires torch to be installed
        try:
            import torch

            result = get_device()
            assert isinstance(result, torch.device)
        except ImportError:
            pytest.skip("torch not installed")

    def test_override_cpu(self) -> None:
        """Should return CPU device when override is 'cpu'."""
        try:
            import torch

            result = get_device(override="cpu")
            assert result == torch.device("cpu")
        except ImportError:
            pytest.skip("torch not installed")

    def test_invalid_override_raises_value_error(self) -> None:
        """Should raise ValueError for invalid override values."""
        try:
            import torch  # noqa: F401

            with pytest.raises(ValueError, match="Invalid device"):
                get_device(override="invalid")  # type: ignore[arg-type]
        except ImportError:
            pytest.skip("torch not installed")

    def test_raises_import_error_without_torch(self) -> None:
        """Should raise ImportError when torch is not available."""
        from unittest.mock import patch

        with (
            patch("again_and_again.src.gpu_wizard.TORCH_AVAILABLE", False),
            pytest.raises(ImportError, match="torch is not available"),
        ):
            get_device()
