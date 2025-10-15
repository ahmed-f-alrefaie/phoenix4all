import functools
import logging

logger = logging.getLogger("phoenix4all")
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.WARNING)


def module_logger(name: str) -> logging.Logger:
    """Create and return a logger for the given module name.
    Args:
        name: The name of the module.
    Returns:
        A configured logger instance.
    """
    log = logging.getLogger(name)

    return log


def create_logger(subname: str) -> logging.Logger:
    """Create and return a logger for the given subname.
    Args:
        subname: The subname to append to the base logger name.
    Returns:
        A configured logger instance.
    """
    log = logging.getLogger(f"phoenix4all.{subname}")
    return log


def debug_function(f):
    """Decorator to log function entry, exit, and exceptions."""
    logger = logging.getLogger(f"{f.__module__}.{f.__name__}")

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        logger.debug(f"Entering with args={args}, kwargs={kwargs}")
        try:
            result = f(*args, **kwargs)
        except Exception:
            logger.exception(f"Exception in {f.__name__}")
            raise
        else:
            logger.debug(f"Exiting with result={result}")
            return result

    return wrapper
