"""Path manipulation and normalization utilities."""

from __future__ import annotations

import pathlib
from datetime import datetime

from again_and_again.src.git_wizard import get_commit_hash, get_git_repo_root_path


def normalize_file_path(
    path: str | pathlib.Path, path_should_exist: bool = False, make_parent_path: bool = True
) -> pathlib.Path:
    """Normalize a file path to a resolved pathlib.Path object.

    Converts strings or Path objects to absolute, resolved paths with optional
    parent directory creation.

    Args:
        path: The file path as a string or pathlib.Path.
        path_should_exist: If True, raises FileNotFoundError when the path
            doesn't exist. Defaults to False.
        make_parent_path: If True, creates parent directories if they don't
            exist. Defaults to True.

    Returns:
        A resolved absolute pathlib.Path object.

    Raises:
        TypeError: If path is not a string or pathlib.Path.
        FileNotFoundError: If path_should_exist is True and the path doesn't exist.

    Example:
        >>> path = normalize_file_path("data/output.txt")
        >>> path = normalize_file_path("/absolute/path.txt", path_should_exist=True)
    """
    if not isinstance(path, str | pathlib.Path):
        raise TypeError(f"Expected str or pathlib.Path, got {type(path)}")

    normalized_path = pathlib.Path(path).resolve()

    if make_parent_path:
        normalized_path.parent.mkdir(parents=True, exist_ok=True)

    if path_should_exist and not normalized_path.exists():
        raise FileNotFoundError(f"Path {normalized_path} does not exist")

    return normalized_path


def normalize_directory_path(path: str | pathlib.Path, make_path: bool = True) -> pathlib.Path:
    """Normalize a directory path to a resolved pathlib.Path object.

    Converts strings or Path objects to absolute, resolved paths with optional
    directory creation.

    Args:
        path: The directory path as a string or pathlib.Path.
        make_path: If True, creates the directory (and parents) if they don't
            exist. Defaults to True.

    Returns:
        A resolved absolute pathlib.Path object.

    Raises:
        TypeError: If path is not a string or pathlib.Path.

    Example:
        >>> dir_path = normalize_directory_path("data/processed")
        >>> dir_path = normalize_directory_path("existing/dir", make_path=False)
    """
    if not isinstance(path, str | pathlib.Path):
        raise TypeError(f"Expected str or pathlib.Path, got {type(path)}")

    normalized_path = pathlib.Path(path).resolve()

    if make_path:
        normalized_path.mkdir(parents=True, exist_ok=True)

    return normalized_path


def path_to_string(source: str | pathlib.Path) -> str:
    """Convert a path to its string representation.

    Converts pathlib.Path objects to resolved absolute path strings.
    String paths are returned unchanged.

    Args:
        source: The path as a string or pathlib.Path object.

    Returns:
        The path as a string. If source was a Path object, returns the
        resolved absolute path string.

    Example:
        >>> path_to_string(Path("./data"))
        '/absolute/path/to/data'
        >>> path_to_string("/some/path")
        '/some/path'
    """
    if isinstance(source, pathlib.Path):
        return str(source.resolve())
    return source


def create_unique_path_inside_of_a_git_repo(
    output_namespace: str | pathlib.Path | None = None,
) -> pathlib.Path:
    """Create a unique, timestamped directory path within a git repository.

    Generates a directory path structure useful for experiment tracking and
    reproducible outputs. The path format is:
    `{git_root}/{namespace}/{YYYY-MM-DD}/{HH-MM-SS}/{commit_hash}/`

    Args:
        output_namespace: Subdirectory from git root for outputs.
            Defaults to "outputs". Must be a relative path that stays within
            the git repository (no "..", no absolute paths).

    Returns:
        A pathlib.Path to the created unique directory.

    Raises:
        FileNotFoundError: If not in a git repository.
        RuntimeError: If unable to get the current commit hash.
        ValueError: If output_namespace tries to escape the git repository.

    Note:
        The timestamp uses local time (not UTC). This is intentional for
        human-readable directory names on the local machine.

    Example:
        >>> path = create_unique_path_inside_of_a_git_repo()
        # Returns: /repo/outputs/2024-01-15/14-30-45/abc123.../
        >>> path = create_unique_path_inside_of_a_git_repo("experiments")
        # Returns: /repo/experiments/2024-01-15/14-30-45/abc123.../
    """

    if output_namespace is None:
        output_namespace = "outputs"

    # Get the git repo root for validation
    git_root = get_git_repo_root_path()

    # Resolve the namespace path and check it stays within git root
    namespace_path = (git_root / output_namespace).resolve()

    # Security check: ensure the resolved path is inside the git repo
    try:
        namespace_path.relative_to(git_root)
    except ValueError as e:
        msg = (
            f"Invalid output_namespace: '{output_namespace}' would create "
            f"directories outside the git repository root ({git_root}). "
            "Use relative paths without '..' to stay within the repository."
        )
        raise ValueError(msg) from e

    timestamp = datetime.now().strftime("%Y-%m-%d/%H-%M-%S")

    return normalize_directory_path(
        namespace_path / timestamp / f"{get_commit_hash()}",
        make_path=True,
    )
