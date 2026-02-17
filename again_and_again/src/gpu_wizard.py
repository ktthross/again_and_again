"""GPU device utilities for PyTorch operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    import torch

try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def get_device(override: Literal["cpu", "cuda", "mps"] | None = None) -> torch.device:
    """Get the optimal device for GPU-accelerated operations.

    Automatically detects and returns the best available compute device:
    - Apple Silicon: Returns MPS (Metal Performance Shaders)
    - NVIDIA GPU: Returns CUDA
    - Otherwise: Returns CPU

    Args:
        override: Force a specific device instead of auto-detection.
            Valid values are "cpu", "cuda", or "mps".

    Returns:
        A torch.device object representing the selected compute device.

    Raises:
        ImportError: If PyTorch is not installed. Install with
            `uv add again-and-again[torch]` or `pip install again-and-again[torch]`.
        ValueError: If override is not a valid device name.

    Example:
        >>> device = get_device()  # Auto-detect best device
        >>> device = get_device(override="cpu")  # Force CPU
    """
    if not TORCH_AVAILABLE:
        raise ImportError(
            "torch is not available. Install with `uv add again-and-again[torch]`"
            " or `pip install again-and-again[torch]`"
        )
    if override is not None and override not in ["cpu", "cuda", "mps"]:
        raise ValueError(f"Invalid device: {override}")

    if override is not None:
        return torch.device(override)

    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")
