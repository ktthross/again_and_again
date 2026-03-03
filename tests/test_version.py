"""Tests for package version."""

import re

import again_and_again

# Strict SemVer: X.Y.Z with optional -pre.release and optional +build.metadata
# Per spec (semver.org):
#   - pre-release MUST be prefixed by "-" (e.g. 1.2.3-alpha.1, 1.2.3-rc.1)
#   - build metadata MUST be prefixed by "+" (e.g. 1.2.3+build.42)
#   - bare suffixes like "1.2.3rc1" are NOT valid SemVer
_SEMVER_PATTERN = re.compile(
    r"^\d+\.\d+\.\d+"
    r"(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?"  # optional pre-release
    r"(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$"  # optional build metadata
)


class TestVersion:
    """Tests for package version."""

    def test_version_is_available(self) -> None:
        """Should expose __version__ at package level."""
        assert hasattr(again_and_again, "__version__")

    def test_version_is_string(self) -> None:
        """Should return version as a string."""
        assert isinstance(again_and_again.__version__, str)

    def test_version_matches_semver_format(self) -> None:
        """Should follow strict semantic versioning format (semver.org)."""
        assert _SEMVER_PATTERN.match(again_and_again.__version__), (
            f"Version {again_and_again.__version__!r} does not match SemVer "
            "(expected X.Y.Z, X.Y.Z-pre.1, or X.Y.Z+build)"
        )

    def test_version_pre_release_requires_dash(self) -> None:
        """Pre-release identifiers must be separated from patch by '-'."""
        # Versions like "1.2.3rc1" or "1.2.3alpha" are NOT valid SemVer
        non_semver_variants = ["1.2.3rc1", "1.2.3alpha", "1.2.3b2", "1.2.3.post1"]
        for bad in non_semver_variants:
            assert not _SEMVER_PATTERN.match(bad), f"{bad!r} should not match the SemVer pattern"
