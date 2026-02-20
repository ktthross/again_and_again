"""Logging utilities with loguru integration and standard logging interception."""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

from again_and_again.src.path_wizard import normalize_file_path

if TYPE_CHECKING:
    import pathlib

try:
    from loguru import logger

    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    logger = None  # type: ignore[assignment]


# Track whether logging has been configured
_LOGGING_CONFIGURED = False


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging messages and redirect them to loguru.

    This allows libraries using standard logging (like PyTorch, Hydra, etc.)
    to have their logs handled by loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:  # noqa: PLR6301
        """Emit a log record by passing it to loguru."""
        # Get corresponding Loguru level if it exists
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logged message originated
        try:
            frame, depth = sys._getframe(6), 6  # noqa: SLF001
        except ValueError:
            # Stack is too shallow, fall back to a smaller depth
            frame, depth = sys._getframe(1), 1  # noqa: SLF001

        while frame and frame.f_code.co_filename == logging.__file__:
            if frame.f_back is None:
                break
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def logging_setup(
    log_file: str | pathlib.Path | None = None,
    log_level: str = "INFO",
    intercept_standard_logging: bool = True,
    intercept_loggers: list[str] | None = None,
) -> None:
    """
    Set up logging to stdout and a file in an idempotent manner.

    This function can be called multiple times safely - it will only configure
    logging once. Subsequent calls will be no-ops.

    Args:
        log_file: Path to the log file. Parent directories will be created
            if they don't exist.
        log_level: Logging level (e.g., "DEBUG", "INFO", "WARNING", "ERROR").
            Default is "INFO".
        intercept_standard_logging: If True, intercept standard library
            logging and redirect it to loguru. This is useful for libraries
            that use the standard logging module. Default is True.
        intercept_loggers: List of specific logger names to intercept.
            If None, defaults to ["torch", "hydra"] when
            intercept_standard_logging is True. To intercept all loggers,
            pass an empty list []. Common logger names: "torch" (PyTorch),
            "hydra" (Hydra), "transformers" (HuggingFace), "matplotlib",
            "PIL" (Pillow).

    Raises:
        ImportError: If loguru is not installed. Install with
            `uv add again-and-again[logging]` or `pip install again-and-again[logging]`.

    Example:
        >>> from again_and_again import logging_setup
        >>> # Default: intercept torch and hydra
        >>> logging_setup("logs/app.log", log_level="DEBUG")
        >>> # Intercept specific loggers
        >>> logging_setup(
        ...     "logs/app.log", intercept_loggers=["torch", "transformers"]
        ... )
        >>> # Intercept all loggers
        >>> logging_setup("logs/app.log", intercept_loggers=[])
        >>> logger.info("This will log to both stdout and logs/app.log")
    """
    if not LOGURU_AVAILABLE:
        raise ImportError(
            "loguru is not available. Install with `uv add again-and-again[logging]`"
            " or `pip install again-and-again[logging]`"
        )

    global _LOGGING_CONFIGURED  # noqa: PLW0603

    # If already configured, do nothing (idempotent behavior)
    if _LOGGING_CONFIGURED:
        return

    # Normalize the log file path
    if log_file is not None:
        log_file_path = normalize_file_path(
            log_file, path_should_exist=False, make_parent_path=True
        )

    # Remove default handler (loguru adds one by default)
    logger.remove()

    # Add stdout handler with colorized output
    logger.add(
        sys.stdout,
        level=log_level,
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    # Add file handler with rotation
    if log_file is not None:
        logger.add(
            log_file_path,
            level=log_level,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}"
            ),
            rotation="500 MB",
            retention="10 days",
            compression="zip",
            enqueue=True,
            encoding="utf-8",
        )

    # Intercept standard library logging if requested
    if intercept_standard_logging:
        # Set default loggers to intercept if not specified
        if intercept_loggers is None:
            loggers_to_intercept = ["torch", "hydra"]
        else:
            loggers_to_intercept = intercept_loggers

        # Configure basic logging with InterceptHandler
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        # If empty list, intercept all loggers
        if len(loggers_to_intercept) == 0:
            for logger_name in logging.root.manager.loggerDict:
                logging.getLogger(logger_name).handlers = [InterceptHandler()]
                logging.getLogger(logger_name).propagate = False
            logger.info("Intercepting all standard library loggers")
        else:
            # Intercept only specified loggers
            for logger_name in loggers_to_intercept:
                logging.getLogger(logger_name).handlers = [InterceptHandler()]
                logging.getLogger(logger_name).propagate = False
            logger.info(f"Intercepting loggers: {', '.join(loggers_to_intercept)}")

    # Silence noisy third-party loggers
    noisy_loggers = [
        "alembic.runtime.migration",
        "databricks.sdk",
        "urllib3",
        "urllib3.connectionpool",
        "requests",
        "httpx",
        "httpcore",
        "azure",
        "botocore",
        "boto3",
        "s3transfer",
        "google",
        "filelock",
        "git.cmd",
        "git.util",
    ]
    for noisy_logger in noisy_loggers:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    # Mark as configured
    _LOGGING_CONFIGURED = True

    if log_file is not None:
        logger.info(f"Logging configured: stdout + {log_file_path}")


def reset_logging() -> None:
    """
    Reset the logging configuration state.

    This is primarily useful for testing, allowing you to reconfigure
    logging after it has been set up.

    Raises:
        ImportError: If loguru is not installed. Install with
            `uv add again-and-again[logging]` or `pip install again-and-again[logging]`.
    """
    if not LOGURU_AVAILABLE:
        raise ImportError(
            "loguru is not available. Install with `uv add again-and-again[logging]`"
            " or `pip install again-and-again[logging]`"
        )

    global _LOGGING_CONFIGURED  # noqa: PLW0603
    _LOGGING_CONFIGURED = False
    logger.remove()
