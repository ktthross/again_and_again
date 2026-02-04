"""Git utilities for repository information and operations."""

import pathlib
import subprocess


def get_git_repo_root_path() -> pathlib.Path:
    """Get the root path of the current git repository.

    Searches upward from the current working directory to find a directory
    containing a .git folder.

    Returns:
        The absolute path to the git repository root.

    Raises:
        FileNotFoundError: If no git repository is found in the current
            directory or any of its parents.
    """
    current_path = pathlib.Path.cwd()
    for parent in [current_path, *current_path.parents]:
        if (parent / ".git").exists():
            return parent
    raise FileNotFoundError(f"Could not identify a git repository starting from {current_path}")


def get_commit_hash() -> str:
    """Get the current HEAD commit hash.

    Returns:
        The 40-character SHA-1 hash of the current HEAD commit.

    Raises:
        subprocess.CalledProcessError: If the git command fails (e.g., not in
            a git repository or git is not installed).
        RuntimeError: If not in a git repository or git is not installed.
    """
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode("utf-8")
            .strip()
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError("Not in a git repository or git is not installed") from e
