import pathlib
import subprocess


def get_git_repo_root_path() -> pathlib.Path:
    """
    Get the root path of the current git repository.
    """
    current_path = pathlib.Path.cwd()
    for parent in [current_path, *current_path.parents]:
        if (parent / ".git").exists():
            return parent
    raise FileNotFoundError(f"Could not identify a git repository starting from {current_path}")


def get_commit_hash() -> str:
    """
    Get the current commit hash.
    """
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
