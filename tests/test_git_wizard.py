"""Tests for git_wizard module."""

import pathlib
import subprocess
from unittest.mock import patch

import pytest

from again_and_again import get_commit_hash, get_git_repo_root_path


class TestGetGitRepoRootPath:
    """Tests for get_git_repo_root_path function."""

    def test_returns_path_object(self) -> None:
        """Should return a pathlib.Path object."""
        result = get_git_repo_root_path()
        assert isinstance(result, pathlib.Path)

    def test_returns_directory_with_git_folder(self) -> None:
        """Should return a directory containing a .git folder."""
        result = get_git_repo_root_path()
        assert (result / ".git").exists()

    def test_raises_when_not_in_git_repo(self, tmp_path: pathlib.Path) -> None:
        """Should raise FileNotFoundError when not in a git repository."""
        with (
            patch("pathlib.Path.cwd", return_value=tmp_path),
            pytest.raises(FileNotFoundError, match="Could not identify a git repository"),
        ):
            get_git_repo_root_path()


class TestGetCommitHash:
    """Tests for get_commit_hash function."""

    def test_returns_string(self) -> None:
        """Should return a string."""
        result = get_commit_hash()
        assert isinstance(result, str)

    def test_returns_40_character_hex_string(self) -> None:
        """Should return a 40-character hexadecimal string (SHA-1 hash)."""
        result = get_commit_hash()
        assert len(result) == 40
        assert all(c in "0123456789abcdef" for c in result)

    def test_raises_when_git_fails(self) -> None:
        """Should raise RuntimeError when git command fails."""
        with (
            patch(
                "subprocess.check_output",
                side_effect=subprocess.CalledProcessError(1, "git"),
            ),
            pytest.raises(RuntimeError, match="Not in a git repository"),
        ):
            get_commit_hash()
