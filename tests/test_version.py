"""Tests for package version."""

from packaging.version import InvalidVersion, Version

import again_and_again


class TestVersion:
    """Tests for package version."""

    def test_version_is_available(self) -> None:
        """Should expose __version__ at package level."""
        assert hasattr(again_and_again, "__version__")

    def test_version_is_string(self) -> None:
        """Should return version as a string."""
        assert isinstance(again_and_again.__version__, str)

    def test_version_is_valid_pep440(self) -> None:
        """Should be a valid PEP 440 version (the format hatchling publishes)."""
        try:
            Version(again_and_again.__version__)
        except InvalidVersion as err:
            raise AssertionError(
                f"Version {again_and_again.__version__!r} is not a valid PEP 440 version"
            ) from err
