from __future__ import annotations

import pathlib


def normalize_file_path(path: str | pathlib.Path, path_should_exist: bool = False) -> pathlib.Path:
    """
    Normalize a path to a pathlib.Path object.
    """
    if not isinstance(path, str | pathlib.Path):
        raise TypeError(f"Expected str or pathlib.Path, got {type(path)}")

    normalized_path = pathlib.Path(path).resolve()

    if path_should_exist and not normalized_path.exists():
        raise FileNotFoundError(f"Path {normalized_path} does not exist")

    return normalized_path
