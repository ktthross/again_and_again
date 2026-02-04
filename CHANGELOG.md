# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with pytest
- GitHub Actions CI workflow for linting, type checking, and testing
- mypy configuration for type checking
- Improved documentation with detailed docstrings

### Changed
- Improved error handling in `get_commit_hash()` with better error messages
- Fixed type annotations for `get_device()` to work when torch is not installed

## [0.7.3] - 2024

### Added
- Type hints support with `py.typed` marker (PR #12)

## [0.7.2] - 2024

### Changed
- Made PyTorch an optional dependency (PR #11)
- Install with `pip install again-and-again[torch]` for GPU support

## [0.7.1] - 2024

### Added
- `create_unique_path_inside_of_a_git_repo()` for experiment tracking (PR #10)

## [0.7.0] - 2024

### Added
- `path_to_string()` function for path conversion (PR #9)

## [0.6.0] - 2024

### Fixed
- Corrected top-level namespace imports (PR #8)

## [0.5.0] - 2024

### Added
- Namespace import support (PR #7)

## [0.4.0] - 2024

### Added
- `normalize_directory_path()` function (PR #6)

## [0.3.0] - 2024

### Changed
- Minor updates and improvements (PR #5)

## [0.2.0] - 2024

### Added
- `get_device()` function for GPU device detection (PR #4)
- Support for MPS (Apple Silicon), CUDA, and CPU devices

## [0.1.0] - 2024

### Added
- Initial release
- `get_git_repo_root_path()` function (PR #3)
- `get_commit_hash()` function
- `normalize_file_path()` function
