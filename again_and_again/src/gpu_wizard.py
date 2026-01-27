from typing import Literal

try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


def get_device(override: Literal["cpu", "cuda", "mps"] | None = None) -> str:
    """
    Get the device to use for GPU operations.
    """
    if not TORCH_AVAILABLE:
        raise ImportError("torch is not available. Install with `again-and-again[torch]`")
    if override is not None and override not in ["cpu", "cuda", "mps"]:
        raise ValueError(f"Invalid device: {override}")

    if override is not None:
        return torch.device(override)

    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")
