"""Pytest configuration and shared fixtures."""

import pathlib
import subprocess

import pytest


@pytest.fixture
def fake_git_repo(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    """
    Create a temporary fake git repository for testing.

    This fixture:
    1. Creates a temporary directory with a .git folder
    2. Initializes a real git repo with a commit
    3. Monkeypatches git_wizard functions to use this temp repo
    4. Returns the path to the fake repo

    Args:
        tmp_path: pytest's temporary directory fixture
        monkeypatch: pytest's monkeypatch fixture

    Returns:
        Path to the fake git repository root
    """
    # Create a fake git repo directory
    fake_repo = tmp_path / "fake_repo"
    fake_repo.mkdir()

    # Initialize a real git repository (lightweight)
    subprocess.run(["git", "init"], cwd=fake_repo, check=True, capture_output=True, text=True)

    # Configure git user for commits
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=fake_repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=fake_repo,
        check=True,
        capture_output=True,
    )

    # Create a dummy file and make an initial commit
    dummy_file = fake_repo / "README.md"
    dummy_file.write_text("# Test Repository\n")

    subprocess.run(["git", "add", "README.md"], cwd=fake_repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "Initial commit"],
        cwd=fake_repo,
        check=True,
        capture_output=True,
    )

    # Get the actual commit hash from this repo
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=fake_repo,
        check=True,
        capture_output=True,
        text=True,
    )
    commit_hash = result.stdout.strip()

    # Monkeypatch the git_wizard functions to use our fake repo

    def mock_get_git_repo_root_path() -> pathlib.Path:
        """Return the fake repo path."""
        return fake_repo

    def mock_get_commit_hash() -> str:
        """Return the commit hash from the fake repo."""
        return commit_hash

    # Apply monkeypatches to all import locations
    # 1. Patch the source modules
    monkeypatch.setattr(
        "again_and_again.src.git_wizard.get_git_repo_root_path",
        mock_get_git_repo_root_path,
    )
    monkeypatch.setattr("again_and_again.src.git_wizard.get_commit_hash", mock_get_commit_hash)

    # 2. Patch the imports in path_wizard (it imports from git_wizard)
    monkeypatch.setattr(
        "again_and_again.src.path_wizard.get_git_repo_root_path",
        mock_get_git_repo_root_path,
    )
    monkeypatch.setattr("again_and_again.src.path_wizard.get_commit_hash", mock_get_commit_hash)

    # 3. Patch the main package exports (from __init__.py)
    monkeypatch.setattr("again_and_again.get_git_repo_root_path", mock_get_git_repo_root_path)
    monkeypatch.setattr("again_and_again.get_commit_hash", mock_get_commit_hash)

    return fake_repo
