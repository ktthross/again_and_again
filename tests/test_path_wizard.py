"""Tests for path_wizard module."""

import pathlib

import pytest

from again_and_again import (
    create_unique_path_inside_of_a_git_repo,
    normalize_directory_path,
    normalize_file_path,
    path_to_string,
)


class TestNormalizeFilePath:
    """Tests for normalize_file_path function."""

    def test_returns_path_object(self, tmp_path: pathlib.Path) -> None:
        """Should return a pathlib.Path object."""
        result = normalize_file_path(tmp_path / "test.txt")
        assert isinstance(result, pathlib.Path)

    def test_accepts_string_path(self, tmp_path: pathlib.Path) -> None:
        """Should accept a string path."""
        result = normalize_file_path(str(tmp_path / "test.txt"))
        assert isinstance(result, pathlib.Path)

    def test_accepts_path_object(self, tmp_path: pathlib.Path) -> None:
        """Should accept a pathlib.Path object."""
        result = normalize_file_path(tmp_path / "test.txt")
        assert isinstance(result, pathlib.Path)

    def test_creates_parent_directory_by_default(self, tmp_path: pathlib.Path) -> None:
        """Should create parent directories by default."""
        new_dir = tmp_path / "new_dir" / "subdir"
        normalize_file_path(new_dir / "test.txt")
        assert new_dir.exists()

    def test_does_not_create_parent_when_disabled(self, tmp_path: pathlib.Path) -> None:
        """Should not create parent directory when make_parent_path is False."""
        new_dir = tmp_path / "nonexistent"
        normalize_file_path(new_dir / "test.txt", make_parent_path=False)
        assert not new_dir.exists()

    def test_raises_when_path_should_exist_but_doesnt(self, tmp_path: pathlib.Path) -> None:
        """Should raise FileNotFoundError when path_should_exist=True and path doesn't exist."""
        with pytest.raises(FileNotFoundError):
            normalize_file_path(tmp_path / "nonexistent.txt", path_should_exist=True)

    def test_returns_resolved_path(self, tmp_path: pathlib.Path) -> None:
        """Should return an absolute resolved path."""
        result = normalize_file_path(tmp_path / "test.txt")
        assert result.is_absolute()

    def test_raises_type_error_for_invalid_type(self) -> None:
        """Should raise TypeError for non-string/Path types."""
        with pytest.raises(TypeError, match="Expected str or pathlib.Path"):
            normalize_file_path(123)  # type: ignore[arg-type]


class TestNormalizeDirectoryPath:
    """Tests for normalize_directory_path function."""

    def test_returns_path_object(self, tmp_path: pathlib.Path) -> None:
        """Should return a pathlib.Path object."""
        result = normalize_directory_path(tmp_path / "test_dir")
        assert isinstance(result, pathlib.Path)

    def test_creates_directory_by_default(self, tmp_path: pathlib.Path) -> None:
        """Should create the directory by default."""
        new_dir = tmp_path / "new_directory"
        normalize_directory_path(new_dir)
        assert new_dir.exists()
        assert new_dir.is_dir()

    def test_creates_nested_directories(self, tmp_path: pathlib.Path) -> None:
        """Should create nested directories."""
        new_dir = tmp_path / "level1" / "level2" / "level3"
        normalize_directory_path(new_dir)
        assert new_dir.exists()

    def test_does_not_create_when_disabled(self, tmp_path: pathlib.Path) -> None:
        """Should not create directory when make_path is False."""
        new_dir = tmp_path / "nonexistent_dir"
        normalize_directory_path(new_dir, make_path=False)
        assert not new_dir.exists()

    def test_raises_type_error_for_invalid_type(self) -> None:
        """Should raise TypeError for non-string/Path types."""
        with pytest.raises(TypeError, match="Expected str or pathlib.Path"):
            normalize_directory_path(123)  # type: ignore[arg-type]


class TestPathToString:
    """Tests for path_to_string function."""

    def test_converts_path_to_string(self, tmp_path: pathlib.Path) -> None:
        """Should convert a Path object to a string."""
        result = path_to_string(tmp_path)
        assert isinstance(result, str)

    def test_returns_string_as_is(self) -> None:
        """Should return a string path unchanged."""
        path_str = "/some/path/to/file.txt"
        result = path_to_string(path_str)
        assert result == path_str

    def test_resolves_path_when_converting(self, tmp_path: pathlib.Path) -> None:
        """Should resolve the path when converting to string."""
        result = path_to_string(tmp_path)
        assert pathlib.Path(result).is_absolute()


class TestCreateUniquePathInsideOfAGitRepo:
    """Tests for create_unique_path_inside_of_a_git_repo function."""

    def test_returns_path_object(self) -> None:
        """Should return a pathlib.Path object."""
        result = create_unique_path_inside_of_a_git_repo()
        assert isinstance(result, pathlib.Path)

    def test_creates_directory(self) -> None:
        """Should create the directory."""
        result = create_unique_path_inside_of_a_git_repo()
        assert result.exists()
        assert result.is_dir()

    def test_uses_default_namespace(self) -> None:
        """Should use 'outputs' as default namespace."""
        result = create_unique_path_inside_of_a_git_repo()
        assert "outputs" in str(result)

    def test_uses_custom_namespace(self) -> None:
        """Should use custom namespace when provided."""
        result = create_unique_path_inside_of_a_git_repo(output_namespace="custom_outputs")
        assert "custom_outputs" in str(result)

    def test_contains_commit_hash(self) -> None:
        """Should contain the current commit hash in the path."""
        from again_and_again import get_commit_hash

        result = create_unique_path_inside_of_a_git_repo()
        commit_hash = get_commit_hash()
        assert commit_hash in str(result)

    def test_contains_timestamp_format(self) -> None:
        """Should contain a timestamp in YYYY-MM-DD/HH-MM-SS format."""
        import re

        result = create_unique_path_inside_of_a_git_repo()
        # Check for date pattern in path
        assert re.search(r"\d{4}-\d{2}-\d{2}", str(result))
        # Check for time pattern in path
        assert re.search(r"\d{2}-\d{2}-\d{2}", str(result))

    def test_rejects_path_traversal_with_parent_dirs(self) -> None:
        """Should reject output_namespace that tries to escape git repo with '..'."""
        import pytest

        with pytest.raises(ValueError, match="outside the git repository root"):
            create_unique_path_inside_of_a_git_repo(output_namespace="../../etc")

    def test_rejects_absolute_paths(self) -> None:
        """Should reject absolute paths as output_namespace."""
        import pytest

        with pytest.raises(ValueError, match="outside the git repository root"):
            create_unique_path_inside_of_a_git_repo(output_namespace="/tmp/malicious")

    def test_allows_nested_relative_paths(self) -> None:
        """Should allow nested relative paths that stay within the repo."""
        result = create_unique_path_inside_of_a_git_repo(output_namespace="data/experiments")
        assert "data" in str(result)
        assert "experiments" in str(result)
