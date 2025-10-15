import pathlib

from ..log import debug_function, module_logger
from .core import PhoenixSource

_source_registry = {}
_log = module_logger(__name__)


class UnknownSourceError(Exception):
    """Exception raised when an unknown source is requested."""

    def __init__(self, source_name: str):
        super().__init__(f"Unknown source with key: {source_name} - available sources: {list_sources()}")


class SourceRegistrationError(Exception):
    """Exception raised when there is an error in source registration."""

    def __init__(self, key: str):
        super().__init__(f"Source with key '{key}' is already registered.")


@debug_function
def register_source(key: str, cls: type[PhoenixSource]):
    """Register a new source class with a given key."""
    if key in _source_registry:
        _log.error(f"Source with key '{key}' is already registered.")
        raise SourceRegistrationError(key)

    _log.debug(f"Registering source '{key}' with class {cls}")
    _source_registry[key] = cls


def list_sources() -> list[str]:
    """List all registered source keys."""
    return list(_source_registry.keys())


def find_source(name: str) -> type[PhoenixSource]:
    """Get the source class by name."""
    try:
        return _source_registry[name]
    except KeyError:
        _log.error(f"Source with key '{name}' not found.")
        raise UnknownSourceError(name) from None


# TODO: Implement "guess"ing logic based on directory contents
def determine_best_source(path: pathlib.Path) -> type[PhoenixSource] | None:
    """Determine the best matching source class for the given directory path."""
    raise NotImplementedError
