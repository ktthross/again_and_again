from __future__ import annotations

import pathlib


def normalize_file_path(
    path: str | pathlib.Path, path_should_exist: bool = False, make_parent_path: bool = True
) -> pathlib.Path:
    """
    Normalize a path to a pathlib.Path object.
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
    """
    Normalize a path to a pathlib.Path object.
    """
    if not isinstance(path, str | pathlib.Path):
        raise TypeError(f"Expected str or pathlib.Path, got {type(path)}")

    normalized_path = pathlib.Path(path).resolve()

    if make_path:
        normalized_path.mkdir(parents=True, exist_ok=True)

    return normalized_path


def path_to_string(source: str | pathlib.Path) -> str:
    """
    Convert any type of path to a string
    """
    if isinstance(source, pathlib.Path):
        return str(source.resolve())
    return source
